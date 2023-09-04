from bluecon import IOAuthTokenStorage, OAuthToken
from homeassistant.core import HomeAssistant
from .const import DOMAIN

class HassDataOAuthTokenStorage(IOAuthTokenStorage):
    def __init__(self, hass: HomeAssistant):
        self.__hass = hass
    
    def retrieveOAuthToken(self) -> OAuthToken:
        return self.__hass.data[DOMAIN]["token"]
    
    def storeOAuthToken(self, oAuthToken: OAuthToken):
        self.__hass.data[DOMAIN]["token"] = oAuthToken
