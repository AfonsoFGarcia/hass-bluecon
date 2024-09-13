from typing import Any
from homeassistant.config_entries import ConfigFlow, OptionsFlow, ConfigEntry
from homeassistant.data_entry_flow import FlowResult, AbortFlow
from homeassistant.const import (
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_API_KEY,
    CONF_CLIENT_ID,
    CONF_CLIENT_SECRET,
)
from homeassistant.core import callback, async_get_hass
import voluptuous as vol
from .ConfigFolderOAuthTokenStorage import ConfigFolderOAuthTokenStorage
from .ConfigFolderNotificationInfoStorage import ConfigFolderNotificationInfoStorage

from bluecon import BlueConAPI, IOAuthTokenStorage, INotificationInfoStorage

from custom_components.bluecon.const import CONF_LOCK_STATE_RESET, CONF_PACKAGE_NAME, CONF_APP_ID, CONF_PROJECT_ID, CONF_SENDER_ID

from . import DOMAIN

class BlueConConfigFlow(ConfigFlow, domain = DOMAIN):
    VERSION = 6

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        error_info: dict[str, str] = {}
        hass = async_get_hass()

        if user_input is not None:
            try:
                tokenStorage: IOAuthTokenStorage = ConfigFolderOAuthTokenStorage(hass)
                notificationInfoStorage: INotificationInfoStorage = ConfigFolderNotificationInfoStorage(hass)
                await BlueConAPI.create(
                    user_input[CONF_USERNAME], 
                    user_input[CONF_PASSWORD], 
                    user_input[CONF_CLIENT_ID],
                    user_input[CONF_CLIENT_SECRET],
                    user_input[CONF_SENDER_ID],
                    user_input[CONF_API_KEY],
                    user_input[CONF_PROJECT_ID],
                    user_input[CONF_APP_ID],
                    user_input[CONF_PACKAGE_NAME],
                    lambda x: None, 
                    tokenStorage, 
                    notificationInfoStorage
                )

                await self.async_set_unique_id(user_input[CONF_USERNAME])
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(
                    title = user_input[CONF_USERNAME], 
                    data = {
                        CONF_CLIENT_ID: user_input[CONF_CLIENT_ID],
                        CONF_CLIENT_SECRET: user_input[CONF_CLIENT_SECRET],
                        CONF_SENDER_ID: user_input[CONF_SENDER_ID],
                        CONF_API_KEY: user_input[CONF_API_KEY],
                        CONF_PROJECT_ID: user_input[CONF_PROJECT_ID],
                        CONF_APP_ID: user_input[CONF_APP_ID],
                        CONF_PACKAGE_NAME: user_input[CONF_PACKAGE_NAME]
                    }, 
                    options = {
                        CONF_LOCK_STATE_RESET: 5
                    }
                )
            except AbortFlow as e:
                raise e
            except Exception:
                error_info['base'] = 'invalid_auth'
        
        return self.async_show_form(
            step_id = "user",
            data_schema = vol.Schema({
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
                vol.Required(CONF_CLIENT_ID): str,
                vol.Required(CONF_CLIENT_SECRET): str,
                vol.Optional(CONF_API_KEY): str,
                vol.Optional(CONF_SENDER_ID): int,
                vol.Optional(CONF_APP_ID): int,
                vol.Optional(CONF_PROJECT_ID): str,
                vol.Optional(CONF_PACKAGE_NAME): str
            }),
            errors = error_info
        )
    
    async def async_step_reconfigure(self, user_input: dict[str, Any] | None = None):
        error_info: dict[str, str] = {}
        hass = async_get_hass()

        if user_input is not None:
            try:
                tokenStorage: IOAuthTokenStorage = ConfigFolderOAuthTokenStorage(hass)
                notificationInfoStorage: INotificationInfoStorage = ConfigFolderNotificationInfoStorage(hass)
                await BlueConAPI.create(
                    user_input[CONF_USERNAME], 
                    user_input[CONF_PASSWORD], 
                    user_input[CONF_CLIENT_ID],
                    user_input[CONF_CLIENT_SECRET],
                    user_input[CONF_SENDER_ID],
                    user_input[CONF_API_KEY],
                    user_input[CONF_PROJECT_ID],
                    user_input[CONF_APP_ID],
                    user_input[CONF_PACKAGE_NAME],
                    lambda x: None, 
                    tokenStorage, 
                    notificationInfoStorage
                )

                await self.async_set_unique_id(user_input[CONF_USERNAME])
                
                return self.async_create_entry(
                    title = user_input[CONF_USERNAME], 
                    data = {
                        CONF_CLIENT_ID: user_input[CONF_CLIENT_ID],
                        CONF_CLIENT_SECRET: user_input[CONF_CLIENT_SECRET],
                        CONF_SENDER_ID: user_input[CONF_SENDER_ID],
                        CONF_API_KEY: user_input[CONF_API_KEY],
                        CONF_PROJECT_ID: user_input[CONF_PROJECT_ID],
                        CONF_APP_ID: user_input[CONF_APP_ID],
                        CONF_PACKAGE_NAME: user_input[CONF_PACKAGE_NAME]
                    }, 
                    options = {
                        CONF_LOCK_STATE_RESET: 5
                    }
                )
            except AbortFlow as e:
                raise e
            except Exception:
                error_info['base'] = 'invalid_auth'
        
        return self.async_show_form(
            step_id = "user",
            data_schema = vol.Schema({
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
                vol.Required(CONF_CLIENT_ID): str,
                vol.Required(CONF_CLIENT_SECRET): str,
                vol.Optional(CONF_API_KEY): str,
                vol.Optional(CONF_SENDER_ID): int,
                vol.Optional(CONF_APP_ID): int,
                vol.Optional(CONF_PROJECT_ID): str,
                vol.Optional(CONF_PACKAGE_NAME): str
            }),
            errors = error_info
        )
    
    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return BlueConOptionsFlow(config_entry)

class BlueConOptionsFlow(OptionsFlow):
    def __init__(self, config_entry: ConfigEntry) -> None:
        self.config_entry = config_entry
    
    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        error_info: dict[str, str] = {}

        lockTimeout = self.config_entry.options.get(CONF_LOCK_STATE_RESET, 5)

        if user_input is not None:
            if user_input[CONF_LOCK_STATE_RESET] >= 0:
                self.hass.config_entries.async_update_entry(self.config_entry, options=user_input)
                return self.async_create_entry(title=None, data=None)
            else:
                error_info['base'] = 'negative_value'
        
        return self.async_show_form(
            step_id = "init", 
            data_schema = vol.Schema({
                vol.Required(CONF_LOCK_STATE_RESET, default = lockTimeout): int
            }),
            errors=error_info
        )