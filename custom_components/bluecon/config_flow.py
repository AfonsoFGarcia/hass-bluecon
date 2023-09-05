from typing import Any
from homeassistant.config_entries import ConfigFlow, ConfigEntry
from homeassistant.data_entry_flow import FlowResult, AbortFlow
from homeassistant.const import (
    CONF_USERNAME,
    CONF_PASSWORD
)
from homeassistant.core import callback, HomeAssistant
import voluptuous as vol
import json

from bluecon import BlueConAPI, InMemoryOAuthTokenStorage, IOAuthTokenStorage

from . import DOMAIN

class BlueConConfigFlow(ConfigFlow, domain = DOMAIN):
    VERSION = 2

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        error_info: dict[str, str] = {}

        if user_input is not None:
            try:
                tokenStorage: IOAuthTokenStorage = InMemoryOAuthTokenStorage()
                await BlueConAPI.create(user_input[CONF_USERNAME], user_input[CONF_PASSWORD], lambda x: None, tokenStorage)
                self.__oAuthToken = tokenStorage.retrieveOAuthToken().toJson()

                await self.async_set_unique_id(user_input[CONF_USERNAME])
                self._abort_if_unique_id_configured(updates = {"token": self.__oAuthToken})
                
                return self._async_finish_flow()
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
    
    @callback
    def _async_finish_flow(self):
        return self.async_create_entry(title = DOMAIN, data = {"token": self.__oAuthToken, "credentials": None, "persistentIds": None})
    
    async def async_migrate_entity(hass: HomeAssistant, config_entry: ConfigEntry):
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
            config_entry.version = 2
            hass.config_entries.async_update_entry(config_entry, data=new)
        
        return True

