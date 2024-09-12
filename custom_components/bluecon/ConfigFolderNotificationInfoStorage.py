from bluecon import INotificationInfoStorage
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store
from typing import Any
from .const import DOMAIN


class ConfigFolderNotificationInfoStorage(INotificationInfoStorage):
    def __init__(self, hass: HomeAssistant):
        self.__credentialsStore = Store(hass=hass, version=1, key=f"{DOMAIN}.CREDENTIALS")
        self.__persistentIdsStore = Store(hass=hass, version=1, key=f"{DOMAIN}.PERSISTENT_IDS")
    
    async def retrieveCredentials(self) -> dict[str, dict[str, Any]] | None:
        return await self.__credentialsStore.async_load()
    
    async def storeCredentials(self, credentials: dict[str, dict[str, Any]]):
        await self.__credentialsStore.async_save(credentials)
    
    async def retrievePersistentIds(self) -> list[str] | None:
        return await self.__persistentIdsStore.async_load()
    
    async def storePersistentId(self, persistentId: str):
        persistentIds = await self.retrievePersistentIds() or []
        persistentId.append(persistentId)
        await self.__persistentIdsStore.async_save(persistentIds)
