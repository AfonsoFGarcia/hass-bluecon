from homeassistant.components.camera import Camera
from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.const import CONF_API_KEY
from homeassistant.config_entries import ConfigEntry


from bluecon import BlueConAPI

from .const import DEVICE_MANUFACTURER, DOMAIN, HASS_BLUECON_VERSION, SIGNAL_CALL_ENDED, CONF_PACKAGE_NAME, CONF_APP_ID, CONF_PROJECT_ID, CONF_SENDER_ID

async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities):
    if entry.data.get(CONF_SENDER_ID, None) is not None and entry.data.get(CONF_API_KEY, None) is not None and entry.data.get(CONF_PROJECT_ID, None) is not None and entry.data.get(CONF_APP_ID, None) is not None and entry.data.get(CONF_PACKAGE_NAME, None) is not None:
        bluecon : BlueConAPI = hass.data[DOMAIN][entry.entry_id]

        pairings = await bluecon.getPairings()

        cameras = []

        for pairing in pairings:
            deviceInfo = await bluecon.getDeviceInfo(pairing.deviceId)
            if deviceInfo.photoCaller:
                image = await bluecon.getLastPicture(pairing.deviceId)
                cameras.append(
                    BlueConStillCamera(
                        bluecon,
                        pairing.deviceId,
                        image,
                        deviceInfo
                    )
                )
        
    async_add_entities(cameras)

class BlueConStillCamera(Camera):
    _attr_should_poll = False

    def __init__(self, bluecon: BlueConAPI, deviceId, image: bytes | None, deviceInfo):
        super().__init__()
        self.bluecon = bluecon
        self.deviceId = deviceId
        self._attr_unique_id = f'{self.deviceId}_last_still'.lower()
        self.entity_id = f'{DOMAIN}.{self._attr_unique_id}'.lower()
        self.__image: bytes | None = image
        self.__model = f'{deviceInfo.type} {deviceInfo.subType} {deviceInfo.family}'

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
            name = f'{self.__model} {self.deviceId}',
            manufacturer = DEVICE_MANUFACTURER,
            model = self.__model,
            sw_version = HASS_BLUECON_VERSION
        )
    
    def camera_image(self, width: int | None = None, height: int | None = None) -> bytes | None:
        return self.__image
