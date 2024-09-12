from bluecon import IOAuthTokenStorage, OAuthToken
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store
from .const import DOMAIN
from pathlib import Path

class ConfigFolderOAuthTokenStorage(IOAuthTokenStorage):
    def __init__(self, hass: HomeAssistant):
        self.__oAuthTokenStore = Store(hass=hass, version=1, key=f"{DOMAIN}.OAUTH_TOKEN")
    
    async def retrieveOAuthToken(self) -> OAuthToken:
        return await self.__oAuthTokenStore.async_load()
    
    async def storeOAuthToken(self, oAuthToken: OAuthToken):
        await self.__oAuthTokenStore.async_save(oAuthToken)
