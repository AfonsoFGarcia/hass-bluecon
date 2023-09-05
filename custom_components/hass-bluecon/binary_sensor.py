from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity
from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import DeviceInfo
from bluecon import BlueConAPI

from .const import DOMAIN, SIGNAL_CALL_ENDED, SIGNAL_CALL_STARTED

STATE_CONNECTED = "Connected"

async def async_setup_platform(hass, config, async_add_entities, discovery_info = None):
    bluecon: BlueConAPI = hass.data[DOMAIN]["bluecon"]

    pairings = await bluecon.getPairings()

    sensors = []

    for pairing in pairings:
        deviceInfo = await bluecon.getDeviceInfo(pairing.deviceId)

        sensors.append(
            BlueConConnectionStatusBinarySensor(
                bluecon,
                pairing.deviceId,
                deviceInfo
            )
        )

        for accessDoorName, accessDoor in pairing.accessDoorMap.items():
            sensors.append(
                BlueConCallStatusBinarySensor(
                    pairing.deviceId,
                    accessDoorName,
                    accessDoor.block,
                    accessDoor.subBlock,
                    accessDoor.number,
                    deviceInfo
                )
            )
    
    async_add_entities(sensors)

class BlueConCallStatusBinarySensor(BinarySensorEntity):
    _attr_should_poll = False

    def __init__(self, deviceId, accessDoorName, block, subBlock, number, deviceInfo):
        self.lockId = f'{deviceId}_{accessDoorName}'
        self.deviceId = deviceId
        self.accessDoorName = accessDoorName
        self.block = block
        self.subBlock = subBlock
        self.number = number
        self._attr_unique_id = f'{self.lockId}_call_status'.lower()
        self.entity_id = f'{DOMAIN}.{self._attr_unique_id}'.lower()
        self._attr_is_on = False
        self.__model = f'{deviceInfo.type} {deviceInfo.subType} {deviceInfo.family}'
    
    @property
    def unique_id(self) -> str | None:
        return self.entity_id
    
    @property
    def device_class(self) -> BinarySensorDeviceClass | None:
        return BinarySensorDeviceClass.CONNECTIVITY

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(
            async_dispatcher_connect(self.hass, SIGNAL_CALL_STARTED.format(self.deviceId, self.accessDoorName), self._call_started_callback)
        )
        self.async_on_remove(
            async_dispatcher_connect(self.hass, SIGNAL_CALL_ENDED.format(self.deviceId), self._call_ended_callback)
        )

    @callback
    def _call_started_callback(self) -> None:
        self._attr_is_on = True
        self.async_schedule_update_ha_state(True)
    
    @callback
    def _call_ended_callback(self) -> None:
        self._attr_is_on = False
        self.async_schedule_update_ha_state(True)
    
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

class BlueConConnectionStatusBinarySensor(BinarySensorEntity):
    _attr_should_poll = True

    def __init__(self, bluecon, deviceId, deviceInfo):
        self.__bluecon : BlueConAPI = bluecon
        self.deviceId = deviceId
        self._attr_unique_id = f'{self.deviceId}_connection_status'.lower()
        self.entity_id = f'{DOMAIN}.{self._attr_unique_id}'.lower()
        self._attr_is_on = deviceInfo is not None and deviceInfo.connectionState == STATE_CONNECTED
        self.__model = f'{deviceInfo.type} {deviceInfo.subType} {deviceInfo.family}'
    
    @property
    def unique_id(self) -> str | None:
        return self.entity_id
    
    @property
    def device_class(self) -> BinarySensorDeviceClass | None:
        return BinarySensorDeviceClass.CONNECTIVITY
    
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

    async def async_update(self):
        deviceInfo = await self.__bluecon.getDeviceInfo(self.deviceId)
        self._attr_is_on = deviceInfo is not None and deviceInfo.connectionState == STATE_CONNECTED
