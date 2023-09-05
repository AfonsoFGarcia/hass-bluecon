from bluecon import INotificationInfoStorage
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from typing import Any

class ConfigEntryNotificationInfoStorage(INotificationInfoStorage):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        self.__entry = entry
        self.__hass = hass
    
    def retrieveCredentials(self) -> dict[str, dict[str, Any]] | None:
        return self.__entry.options["credentials"]
    
    def storeCredentials(self, credentials: dict[str, dict[str, Any]]):
        new = {**self.__entry.options,
                      "credentials": credentials}
        self.__hass.config_entries.async_update_entry(self.__entry, options=new)
    
    def retrievePersistentIds(self) -> list[str] | None:
        return self.__entry.options["persistentIds"]
    
    def storePersistentId(self, persistentId: str):
        stored_persistent_ids = self.__entry.options["persistentIds"]
        if stored_persistent_ids is None:
            stored_persistent_ids = []
        
        stored_persistent_ids.append(persistentId)

        new = {**self.__entry.options,
                      "persistentIds": stored_persistent_ids}
        self.__hass.config_entries.async_update_entry(self.__entry, options=new)
