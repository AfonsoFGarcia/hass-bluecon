from typing import Any
from homeassistant.config_entries import ConfigFlow, OptionsFlow, ConfigEntry
from homeassistant.data_entry_flow import FlowResult, AbortFlow
from homeassistant.const import (
    CONF_USERNAME,
    CONF_PASSWORD
)
from homeassistant.core import callback
import voluptuous as vol

from bluecon import BlueConAPI, InMemoryOAuthTokenStorage, IOAuthTokenStorage

from custom_components.bluecon.const import CONF_LOCK_STATE_RESET

from . import DOMAIN

class BlueConConfigFlow(ConfigFlow, domain = DOMAIN):
    VERSION = 5

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        error_info: dict[str, str] = {}

        if user_input is not None:
            try:
                tokenStorage: IOAuthTokenStorage = InMemoryOAuthTokenStorage()
                await BlueConAPI.create(user_input[CONF_USERNAME], user_input[CONF_PASSWORD], lambda x: None, tokenStorage)

                await self.async_set_unique_id(user_input[CONF_USERNAME])
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(title = user_input[CONF_USERNAME], data = {}, options = {})
            except AbortFlow as e:
                raise e
            except Exception:
                error_info['base'] = 'invalid_auth'
        
        return self.async_show_form(
            step_id = "user",
            data_schema = vol.Schema({
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str
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

        if user_input is not None:
            self.async_create_entry(title="", data=user_input)
        
        return self.async_show_form(
            step_id = "init", 
            data_schema = vol.Schema({
                vol.Required(CONF_LOCK_STATE_RESET, default = 5): int
            }),
            errors=error_info
        )