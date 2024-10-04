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
        if asyncio.get_running_loop() == self.__hass.loop:
            return self.__credentialsStore.async_load()
        else:
            return asyncio.run_coroutine_threadsafe(
                self.__credentialsStore.async_load(), self.__hass.loop
            ).result(timeout=2)
    
    async def storeCredentials(self, credentials: dict[str, dict[str, Any]]):
        if asyncio.get_running_loop() == self.__hass.loop:
            self.__credentialsStore.async_save(credentials)
        else:
            asyncio.run_coroutine_threadsafe(
                self.__credentialsStore.async_save(credentials), self.__hass.loop
            ).result(timeout=2)
    
    async def retrievePersistentIds(self) -> list[str] | None:
        if asyncio.get_running_loop() == self.__hass.loop:
            return self.__persistentIdsStore.async_load()
        else:
            return asyncio.run_coroutine_threadsafe(
                self.__persistentIdsStore.async_load(), self.__hass.loop
            ).result(timeout=2)
    
    async def storePersistentId(self, persistentId: str):
        persistentIds = await self.retrievePersistentIds()
        if type(persistentIds) is not list:
            persistentIds = []
        persistentIds.append(persistentId)
        if asyncio.get_running_loop() == self.__hass.loop:
            self.__persistentIdsStore.async_save(persistentIds)
        else:
            asyncio.run_coroutine_threadsafe(
                self.__persistentIdsStore.async_save(persistentIds), self.__hass.loop
            ).result(timeout=2)
