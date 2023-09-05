from bluecon import IOAuthTokenStorage, OAuthToken
from homeassistant.config_entries import ConfigEntry

class ConfigEntryOAuthTokenStorage(IOAuthTokenStorage):
    def __init__(self, entry: ConfigEntry):
        self.__entry = entry
    
    def retrieveOAuthToken(self) -> OAuthToken:
        return OAuthToken.fromJson(self.__entry.data["token"])
    
    def storeOAuthToken(self, oAuthToken: OAuthToken):
        self.__entry.data["token"] = oAuthToken.toJson()
