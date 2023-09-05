from .const import DOMAIN, CONF_USERNAME, CONF_PASSWORD, SIGNAL_CALL_ENDED, SIGNAL_CALL_STARTED
from .HassDataOAuthTokenStorage import HassDataOAuthTokenStorage
from homeassistant.const import EVENT_HOMEASSISTANT_START, EVENT_HOMEASSISTANT_STOP, Platform
import homeassistant.helpers.config_validation as cv
import homeassistant.helpers.discovery as discovery
from homeassistant.helpers.dispatcher import dispatcher_send
import voluptuous as vol
from bluecon import BlueConAPI, INotification, CallNotification, CallEndNotification

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema({
            vol.Required(CONF_USERNAME): cv.string,
            vol.Required(CONF_PASSWORD): cv.string
        })
    },
    extra = vol.ALLOW_EXTRA
)


async def async_setup(hass, config):
    def notification_callback(notification: INotification):
        if type(notification) is CallNotification:
            dispatcher_send(hass, SIGNAL_CALL_STARTED.format(notification.deviceId, notification.accessDoorKey))
        elif type(notification) is CallEndNotification:
            dispatcher_send(hass, SIGNAL_CALL_ENDED.format(notification.deviceId))

    conf = config[DOMAIN]
    username = conf.get(CONF_USERNAME)
    password = conf.get(CONF_PASSWORD)

    hass.data[DOMAIN] = {
        "bluecon": None,
        "token": None
    }

    bluecon = await BlueConAPI.create(username, password, notification_callback, HassDataOAuthTokenStorage(hass))
    await hass.async_add_executor_job(bluecon.startNotificationListener)

    async def cleanup(event):
        await bluecon.stopNotificationListener()
    
    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, cleanup)
    hass.data[DOMAIN]["bluecon"] = bluecon

    hass.async_create_task(
        discovery.async_load_platform(hass, Platform.BINARY_SENSOR, DOMAIN, {}, config)
    )

    hass.async_create_task(
        discovery.async_load_platform(hass, Platform.LOCK, DOMAIN, {}, config)
    )

    hass.async_create_task(
        discovery.async_load_platform(hass, Platform.CAMERA, DOMAIN, {}, config)
    )

    hass.async_create_task(
        discovery.async_load_platform(hass, Platform.SENSOR, DOMAIN, {}, config)
    )

    return True
