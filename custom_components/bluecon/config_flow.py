from typing import Any
from homeassistant.config_entries import ConfigFlow
from homeassistant.data_entry_flow import FlowResult, AbortFlow
from homeassistant.const import (
    CONF_USERNAME,
    CONF_PASSWORD
)
from homeassistant.core import callback
import voluptuous as vol

from bluecon import BlueConAPI, InMemoryOAuthTokenStorage, IOAuthTokenStorage

from . import DOMAIN

class BlueConConfigFlow(ConfigFlow, domain = DOMAIN):
    VERSION = 3

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        error_info: dict[str, str] = {}

        if user_input is not None:
            try:
                tokenStorage: IOAuthTokenStorage = InMemoryOAuthTokenStorage()
                await BlueConAPI.create(user_input[CONF_USERNAME], user_input[CONF_PASSWORD], lambda x: None, tokenStorage)
                self.__oAuthToken = tokenStorage.retrieveOAuthToken().toJson()

                await self.async_set_unique_id(user_input[CONF_USERNAME])
                self._abort_if_unique_id_configured()
                
                return self._async_finish_flow()
            except AbortFlow as e:
                entry = next(e for e in self.hass.config_entries.async_entries(DOMAIN) if e.unique_id == user_input[CONF_USERNAME])
                self.hass.config_entries.async_update_entry(
                    entry, options={**entry.options, **{"token": self.__oAuthToken}}
                )
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
    
    @callback
    def _async_finish_flow(self):
        return self.async_create_entry(title = DOMAIN, data = {}, options = {"token": self.__oAuthToken, "credentials": None, "persistentIds": None})
