import asyncio
from .const import DOMAIN
from homeassistant.components.lock import LockEntity
from homeassistant.const import (
    STATE_JAMMED,
    STATE_LOCKED,
    STATE_LOCKING,
    STATE_UNLOCKED,
    STATE_UNLOCKING,
)
from homeassistant.helpers.entity import DeviceInfo
from bluecon import BlueConAPI

LOCK_UNLOCK_DELAY = 5

async def async_setup_entry(hass, config, async_add_entities):
    bluecon = hass.data[DOMAIN][config.entry_id]

    pairings = await bluecon.getPairings()

    locks = []

    for pairing in pairings:
        deviceInfo = await bluecon.getDeviceInfo(pairing.deviceId)
        for accessDoorName, accessDoor in pairing.accessDoorMap.items():
            locks.append(
                BlueConLock(
                    bluecon,
                    pairing.deviceId,
                    accessDoorName,
                    accessDoor,
                    deviceInfo
                )
            )
    
    async_add_entities(locks)

class BlueConLock(LockEntity):
    _attr_should_poll = False

    def __init__(self, bluecon: BlueConAPI, deviceId, accessDoorName, accessDoor, deviceInfo):
        self.bluecon = bluecon
        self.lockId = f'{deviceId}_{accessDoorName}'
        self.deviceId = deviceId
        self.accessDoorName = accessDoorName
        self.accessDoor = accessDoor
        self._attr_unique_id = f'{self.lockId}_door_lock'.lower()
        self.entity_id = f'{DOMAIN}.{self._attr_unique_id}'.lower()
        self._state = STATE_LOCKED
        self.__model = f'{deviceInfo.type} {deviceInfo.subType} {deviceInfo.family}'
    
    @property
    def is_locking(self) -> bool:
        """Return true if lock is locking."""
        return self._state == STATE_LOCKING

    @property
    def is_unlocking(self) -> bool:
        """Return true if lock is unlocking."""
        return self._state == STATE_UNLOCKING

    @property
    def is_jammed(self) -> bool:
        """Return true if lock is jammed."""
        return self._state == STATE_JAMMED

    @property
    def is_locked(self) -> bool:
        """Return true if lock is locked."""
        return self._state == STATE_LOCKED

    async def async_lock(self) -> None:
        pass

    async def async_unlock(self) -> None:
        """Unlock the device."""
        self._state = STATE_UNLOCKING
        self.async_schedule_update_ha_state(True)
        await self.bluecon.openDoor(self.deviceId, self.accessDoor)
        self._state = STATE_UNLOCKED
        self.async_schedule_update_ha_state(True)
        await asyncio.sleep(LOCK_UNLOCK_DELAY)
        self._state = STATE_LOCKED
        self.async_schedule_update_ha_state(True)

    async def async_open(self) -> None:
        pass
    
    @property
    def device_info(self) -> DeviceInfo | None:
        return DeviceInfo(
            identifiers = {
                (DOMAIN, self.deviceId)
            },
            name = f'{self.__model} {self.deviceId}',
            manufacturer = 'Fermax',
            model = self.__model,
            sw_version = '0.0.1'
        )
