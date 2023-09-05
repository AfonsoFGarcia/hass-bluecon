from .const import DOMAIN, SIGNAL_CALL_ENDED, SIGNAL_CALL_STARTED
from .ConfigEntryOAuthTokenStorage import ConfigEntryOAuthTokenStorage
from .ConfigEntryNotificationInfoStorage import ConfigEntryNotificationInfoStorage
from homeassistant.const import EVENT_HOMEASSISTANT_STOP, Platform
from homeassistant.helpers.dispatcher import dispatcher_send
from bluecon import BlueConAPI, INotification, CallNotification, CallEndNotification
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
import json


PLATFORMS: list[str] = [Platform.BINARY_SENSOR, Platform.LOCK, Platform.CAMERA, Platform.SENSOR]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    def notification_callback(notification: INotification):
        if type(notification) is CallNotification:
            dispatcher_send(hass, SIGNAL_CALL_STARTED.format(notification.deviceId, notification.accessDoorKey))
        elif type(notification) is CallEndNotification:
            dispatcher_send(hass, SIGNAL_CALL_ENDED.format(notification.deviceId))

    hass.data[DOMAIN] = {
        "bluecon": None
    }

    bluecon = BlueConAPI.create_already_authed(notification_callback, ConfigEntryOAuthTokenStorage(entry), ConfigEntryNotificationInfoStorage(entry))
    await hass.async_add_executor_job(bluecon.startNotificationListener)

    async def cleanup(event):
        await bluecon.stopNotificationListener()
    
    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, cleanup)
    hass.data[DOMAIN][entry.entry_id] = bluecon

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok

async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    if config_entry.version == 1:
        try:
            with open("credentials.json", "r") as f:
                credentials = json.load(f)
        except FileNotFoundError:
            credentials = None
        
        try:
            with open("persistent_ids.txt", "r") as f:
                persistentIds = [x.strip() for x in f]
        except FileNotFoundError:
            persistentIds = None
        
        new = {
            **config_entry.data,
            "credentials": credentials,
            "persistentIds": persistentIds
        }
        config_entry.version = 3
        hass.config_entries.async_update_entry(config_entry, data={}, options=new)
    if config_entry.version == 2:
        new = {**config_entry.data}
        config_entry.version = 3
        hass.config_entries.async_update_entry(config_entry, data={}, options=new)
    
    return True
