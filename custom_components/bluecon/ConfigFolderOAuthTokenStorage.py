from bluecon import IOAuthTokenStorage, OAuthToken
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from pathlib import Path

class ConfigFolderOAuthTokenStorage(IOAuthTokenStorage):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        self.__oAuthTokenFileName = Path(hass.config.path(f'.{DOMAIN}', entry.entry_id, 'oauth_token.json'))

        Path(hass.config.path(f'.{DOMAIN}', entry.entry_id)).mkdir(parents=True, exist_ok=True)

        self.__oAuthTokenFileName.touch(exist_ok=True)
    
    def retrieveOAuthToken(self) -> OAuthToken:
        with open(self.__oAuthTokenFileName, "r") as f:
            return OAuthToken.fromJson(f)
    
    def storeOAuthToken(self, oAuthToken: OAuthToken):
        with open(self.__oAuthTokenFileName, "w") as f:
            f.write(oAuthToken.toJson())
