from bluecon import IOAuthTokenStorage, OAuthToken
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

class ConfigFolderOAuthTokenStorage(IOAuthTokenStorage):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        self.__oAuthTokenFileName = hass.config.path(f'.{DOMAIN}', entry.entry_id, 'oauth_token.json')
    
    def retrieveOAuthToken(self) -> OAuthToken:
        with open(self.__oAuthTokenFileName, "r") as f:
            return OAuthToken.fromJson(f)
    
    def storeOAuthToken(self, oAuthToken: OAuthToken):
        with open(self.__oAuthTokenFileName, "w+") as f:
            f.write(oAuthToken.toJson())
