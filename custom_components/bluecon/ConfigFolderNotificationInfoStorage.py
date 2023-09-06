from bluecon import INotificationInfoStorage
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from typing import Any
from .const import DOMAIN
import json
from pathlib import Path

class ConfigFolderNotificationInfoStorage(INotificationInfoStorage):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        self.__credentialsFileName = Path(hass.config.path(f'.{DOMAIN}', entry.entry_id, 'credentials.json'))
        self.__persistentIdsFileName = Path(hass.config.path(f'.{DOMAIN}', entry.entry_id, 'persistent_ids.txt'))

        Path(hass.config.path(f'.{DOMAIN}', entry.entry_id)).mkdir(parents=True, exist_ok=True)
        Path(hass.config.path(f'.{DOMAIN}', entry.entry_id)).mkdir(parents=True, exist_ok=True)

        self.__credentialsFileName.touch(exist_ok=True)
        self.__persistentIdsFileName.touch(exist_ok=True)
    
    def retrieveCredentials(self) -> dict[str, dict[str, Any]] | None:
        try:
            with open(self.__credentialsFileName, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return None
    
    def storeCredentials(self, credentials: dict[str, dict[str, Any]]):
        with open(self.__credentialsFileName, "w") as f:
            json.dump(credentials, f)
    
    def retrievePersistentIds(self) -> list[str] | None:
        try:
            with open(self.__persistentIdsFileName, "r") as f:
                return [x.strip() for x in f]
        except FileNotFoundError:
            return None
    
    def storePersistentId(self, persistentId: str):
        with open(self.__persistentIdsFileName, "a") as f:
            f.write(persistentId + "\n")
