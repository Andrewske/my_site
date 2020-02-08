import requests, json
from requests.auth import HTTPBasicAuth
from my_site import secrets
import random
import string
import base64
import urllib

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode



class Spotify:

    def __init__(self):
        self.api_url = "https://accounts.spotify.com/"
        #self.encoded_data = base64.b64encode(bytes(f"{secrets.SPOTIFY_CLIENT_ID}:{secrets.SPOTIFY_CLIENT_SECRET}", "ISO-8859-1"))
        #self.authorization_header_string = f"Authorization: Basic {self.encoded_data}"
        #self.auth64 = base64.b64encode('%s:%s' % (secrets.SPOTIFY_CLIENT_ID,secrets.SPOTIFY_CLIENT_SECRET).encode()).replace('\n', '')
        #self.header = ("Authorization: Basic %s" % self.auth64)

    def get_auth_url(self):
        scopes = [
            'playlist-read-collaborative',
            'playlist-modify-public',
            'user-library-modify',
            'user-top-read',
            'playlist-read-private',
            'user-follow-read',
            'user-read-recently-played',
            'playlist-modify-private',
            'user-follow-modify',
            'user-library-read'
        ]
        scope = ' '.join(scopes)
        state = 'spotify_' + ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        auth_code_dict = {
            "client_id": secrets.SPOTIFY_CLIENT_ID,
            "response_type": "code",
            "redirect_uri": "http://127.0.0.1:8000/profile",
            "scope": scope,
            "state": state
        }
        params = urlencode(auth_code_dict, True, quote_via=urllib.parse.quote)
        return [self.api_url + 'authorize?' + params, state]

    #Once receiving the code from Spotify we request the access token
    def get_access_token(self, code):
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "http://127.0.0.1:8000/profile"
        }
        response = requests.post(
            self.api_url + 'api/token?', data=data, auth =(secrets.SPOTIFY_CLIENT_ID,secrets.SPOTIFY_CLIENT_SECRET)
        )
        response_data = json.loads(response.text)
        try:
            access_token = response_data["access_token"]
            return [1, response_data]
        except:
            return [2, json.dumps(response_data)]
        

    # A token is automatically set to expire every hour. This code will refresh that token.
    # With this we need to keep track of the last time a token was requested
    # If that time is > 1 hour we first need to request a new token
    def refresh_access_token(self, refresh_token):
        data = {
            'grant_type':'refresh_token',
            'refresh_token': refresh_token
        }

        response = requests.post(
            self.api_url + "api/token", data=data, headers=self.authorization_header_string
        )

if __name__ == "__main__":
    print("spotify")