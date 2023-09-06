from bluecon import INotificationInfoStorage
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from typing import Any
from .const import SIGNAL_ENTITY_UPDATED
from homeassistant.helpers.dispatcher import dispatcher_send

class ConfigEntryNotificationInfoStorage(INotificationInfoStorage):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        self.__entry = entry
        self.__hass = hass
    
    def retrieveCredentials(self) -> dict[str, dict[str, Any]] | None:
        return self.__entry.options["credentials"]
    
    def storeCredentials(self, credentials: dict[str, dict[str, Any]]):
        new = {**self.__entry.options,
                      "credentials": credentials}
        dispatcher_send(self.__hass, SIGNAL_ENTITY_UPDATED.format(self.__entry.entry_id), new)
    
    def retrievePersistentIds(self) -> list[str] | None:
        return self.__entry.options["persistentIds"]
    
    def storePersistentId(self, persistentId: str):
        stored_persistent_ids = self.__entry.options["persistentIds"]
        if stored_persistent_ids is None:
            stored_persistent_ids = []
        
        stored_persistent_ids.append(persistentId)

        new = {**self.__entry.options,
                      "persistentIds": stored_persistent_ids}
        dispatcher_send(self.__hass, SIGNAL_ENTITY_UPDATED.format(self.__entry.entry_id), new)
