from bluecon import IOAuthTokenStorage, OAuthToken
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import SIGNAL_ENTITY_UPDATED

class ConfigEntryOAuthTokenStorage(IOAuthTokenStorage):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        self.__entry = entry
        self.__hass = hass
    
    def retrieveOAuthToken(self) -> OAuthToken:
        return OAuthToken.fromJson(self.__entry.options["token"])
    
    def storeOAuthToken(self, oAuthToken: OAuthToken):
        new = {**self.__entry.options,
                      "token": oAuthToken.toJson()}
        self.__hass.bus.fire(SIGNAL_ENTITY_UPDATED.format(self.__entry.entry_id), new)
