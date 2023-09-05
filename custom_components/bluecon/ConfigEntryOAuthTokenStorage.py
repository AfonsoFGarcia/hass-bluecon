from bluecon import IOAuthTokenStorage, OAuthToken
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

class ConfigEntryOAuthTokenStorage(IOAuthTokenStorage):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        self.__entry = entry
        self.__hass = hass
    
    def retrieveOAuthToken(self) -> OAuthToken:
        return OAuthToken.fromJson(self.__entry.options["token"])
    
    def storeOAuthToken(self, oAuthToken: OAuthToken):
        new = {**self.__entry.options,
                      "token": oAuthToken.toJson()}
        self.__hass.config_entries.async_update_entry(self.__entry, options=new)
