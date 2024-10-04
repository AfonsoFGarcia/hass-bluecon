import asyncio
from bluecon import INotificationInfoStorage
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store
from typing import Any
from .const import DOMAIN


class ConfigFolderNotificationInfoStorage(INotificationInfoStorage):
    def __init__(self, hass: HomeAssistant):
        self.__hass = hass
        self.__credentialsStore = Store(hass=hass, version=1, key=f"{DOMAIN}.CREDENTIALS")
        self.__persistentIdsStore = Store(hass=hass, version=1, key=f"{DOMAIN}.PERSISTENT_IDS")
    
    async def retrieveCredentials(self) -> dict[str, dict[str, Any]] | None:
        return asyncio.run_coroutine_threadsafe(
            self.__credentialsStore.async_load(), self.__hass.loop
        ).result()
    
    async def storeCredentials(self, credentials: dict[str, dict[str, Any]]):
        asyncio.run_coroutine_threadsafe(
            self.__credentialsStore.async_save(credentials), self.__hass.loop
        ).result()
    
    async def retrievePersistentIds(self) -> list[str] | None:
        return asyncio.run_coroutine_threadsafe(
            self.__persistentIdsStore.async_load(), self.__hass.loop
        ).result()
    
    async def storePersistentId(self, persistentId: str):
        persistentIds = asyncio.run_coroutine_threadsafe(
            self.retrievePersistentIds(), self.__hass.loop
        ).result() or []
        persistentId.append(persistentId)
        asyncio.run_coroutine_threadsafe(
            self.__persistentIdsStore.async_save(persistentIds), self.__hass.loop
        ).result()
