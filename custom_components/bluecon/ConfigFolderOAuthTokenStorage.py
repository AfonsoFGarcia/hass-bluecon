import asyncio
from bluecon import IOAuthTokenStorage, OAuthToken
from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store
from .const import DOMAIN
from pathlib import Path

class ConfigFolderOAuthTokenStorage(IOAuthTokenStorage):
    def __init__(self, hass: HomeAssistant):
        self.__hass = hass
        self.__oAuthTokenStore = Store(hass=hass, version=1, key=f"{DOMAIN}.OAUTH_TOKEN")
    
    async def retrieveOAuthToken(self) -> OAuthToken:
        if asyncio.get_running_loop() == self.__hass.loop:
            json = await self.__oAuthTokenStore.async_load()
        else:
            json = asyncio.run_coroutine_threadsafe(
                self.__oAuthTokenStore.async_load(), self.__hass.loop
            ).result(timeout=2)
        return OAuthToken.fromJson(json)
    
    async def storeOAuthToken(self, oAuthToken: OAuthToken):
        json = oAuthToken.toJson()
        if asyncio.get_running_loop() == self.__hass.loop:
            await self.__oAuthTokenStore.async_save(json)
        else:
            asyncio.run_coroutine_threadsafe(
                self.__oAuthTokenStore.async_save(oAuthToken.toJson()), self.__hass.loop
            ).result(timeout=2)
