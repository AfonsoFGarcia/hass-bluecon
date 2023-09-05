from .const import DOMAIN, SIGNAL_CALL_ENDED, SIGNAL_CALL_STARTED
from .ConfigEntryOAuthTokenStorage import ConfigEntryOAuthTokenStorage
from homeassistant.const import EVENT_HOMEASSISTANT_STOP, Platform
from homeassistant.helpers.dispatcher import dispatcher_send
from bluecon import BlueConAPI, INotification, CallNotification, CallEndNotification
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    def notification_callback(notification: INotification):
        if type(notification) is CallNotification:
            dispatcher_send(hass, SIGNAL_CALL_STARTED.format(notification.deviceId, notification.accessDoorKey))
        elif type(notification) is CallEndNotification:
            dispatcher_send(hass, SIGNAL_CALL_ENDED.format(notification.deviceId))

    hass.data[DOMAIN] = {
        "bluecon": None
    }

    bluecon = BlueConAPI.create_already_authed(notification_callback, ConfigEntryOAuthTokenStorage(entry))
    await hass.async_add_executor_job(bluecon.startNotificationListener)

    async def cleanup(event):
        await bluecon.stopNotificationListener()
    
    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, cleanup)
    hass.data[DOMAIN]["bluecon"] = bluecon

    await hass.config_entries.async_forward_entry_setups(entry, [Platform.BINARY_SENSOR, Platform.LOCK, Platform.CAMERA, Platform.SENSOR])
    entry.async_on_unload(cleanup)

    return True
