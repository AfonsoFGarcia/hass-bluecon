from homeassistant.components.camera import Camera
from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import DeviceInfo

from bluecon import BlueConAPI

from .const import DOMAIN, SIGNAL_CALL_ENDED

async def async_setup_platform(hass, config, async_add_entities, discovery_info = None):
    bluecon : BlueConAPI = hass.data[DOMAIN]["bluecon"]

    pairings = await bluecon.getPairings()

    locks = []

    for pairing in pairings:
        image = await bluecon.getLastPicture(pairing.deviceId)
        locks.append(
            BlueConStillCamera(
                bluecon,
                pairing.deviceId,
                image
            )
        )
    
    async_add_entities(locks)

class BlueConStillCamera(Camera):
    _attr_should_poll = False

    def __init__(self, bluecon: BlueConAPI, deviceId, image: bytes | None):
        super().__init__()
        self.bluecon = bluecon
        self.deviceId = deviceId
        self._attr_unique_id = f'{self.deviceId}_last_still'.lower()
        self.entity_id = f'{DOMAIN}.{self._attr_unique_id}'.lower()
        self.__image: bytes | None = image

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(
            async_dispatcher_connect(self.hass, SIGNAL_CALL_ENDED.format(self.deviceId), self._call_ended_callback)
        )

    @callback
    async def _call_ended_callback(self) -> None:
        self.__image = await self.bluecon.getLastPicture(self.deviceId)
        self.async_schedule_update_ha_state(True)
    
    @property
    def device_info(self) -> DeviceInfo | None:
        return DeviceInfo(
            identifiers = {
                (DOMAIN, self.deviceId)
            },
            name = f'Fermax Blue {self.deviceId}',
            manufacturer = 'Fermax',
            model = 'Blue',
            sw_version = '0.0.1'
        )
    
    def camera_image(self, width: int | None = None, height: int | None = None) -> bytes | None:
        return self.__image
