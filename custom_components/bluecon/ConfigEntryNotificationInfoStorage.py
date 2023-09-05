from bluecon import INotificationInfoStorage
from homeassistant.config_entries import ConfigEntry
from typing import Any

class ConfigEntryNotificationInfoStorage(INotificationInfoStorage):
    def __init__(self, entry: ConfigEntry):
        self.__entry = entry
    
    def retrieveCredentials(self) -> dict[str, dict[str, Any]] | None:
        return self.__entry.data["credentials"]
    
    def storeCredentials(self, credentials: dict[str, dict[str, Any]]):
        self.__entry.data["credentials"] = credentials
    
    def retrievePersistentIds(self) -> list[str] | None:
        return self.__entry.data["persistentIds"]
    
    def storePersistentId(self, persistentId: str):
        stored_persistent_ids = self.__entry.data["persistentIds"]
        if stored_persistent_ids is None:
            stored_persistent_ids = []
        
        stored_persistent_ids.append(persistentId)

        self.__entry.data["persistentIds"] = stored_persistent_ids