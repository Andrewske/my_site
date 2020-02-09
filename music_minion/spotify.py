import requests, json
from requests.auth import HTTPBasicAuth
from my_site import secrets
import random
import string
import base64
import urllib
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from .models import SpotifyUser

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode



class SpotifyAuth:

    def __init__(self):
        self.api_url = "https://accounts.spotify.com/"

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
            return [2, response_data]
        

    # A token is automatically set to expire every hour. This code will refresh that token.
    # With this we need to keep track of the last time a token was requested
    # If that time is > 1 hour we first need to request a new token
    def check_auth(self, request):
        try:
            s = request.user.spotifyuser
            time_since_auth = timezone.now() - s.auth_date
            if time_since_auth > timedelta(hours=1):
                response = self.refresh_access_token(s.refresh_token)
                if response[0] == 1:
                    try: 
                        s.access_token = response[1]['access_token']
                        s.save()
                        return "Access Token Updated"
                    except Exception as x:
                        return "Couldn't save new access token: " + str(x)
                else:
                    return json.dumps(response[1])
            else:
                return "User auth token is valid"
        except Exception as x:
            return "Error: " + str(x)
            #refresh_access_token()
        

    
    def refresh_access_token(self, refresh_token):
        data = {
            'grant_type':'refresh_token',
            'refresh_token': refresh_token
        }

        response = requests.post(
            self.api_url + "api/token", data=data, auth=(secrets.SPOTIFY_CLIENT_ID,secrets.SPOTIFY_CLIENT_SECRET)
        )
        response_data = json.loads(response.text)
        
        try:
            access_token = response_data["access_token"]
            return [1, response_data]
        except:
            return [2, response_data]


class SpotifySearch():
    
    def __init__(self):
        self.api_url = 'https://api.spotify.com/v1/search'

    def available_genres(self, access_token):
        url = 'https://api.spotify.com/v1/recommendations/available-genre-seeds'
        header_value = "Bearer " + access_token
        response = requests.get(url, headers={"Authorization": header_value})
        response_data = json.loads(response.text)
        try:
            return response_data['genres']
        except Exception as x :
            return ["No Genres Available", str(x)]


        
    
    def find_songs(self, access_token, limit=25, offset=None, q=None):
        
        data = {
            'q': q,
            'type':'track',
            'limit':limit,
        }

        if offset:
            data['offset'] = offset

        header_value = "Bearer " + access_token
        response = requests.get(self.api_url, params=data, headers={"Authorization": header_value})
        response_data = json.loads(response.text)
        return response_data['tracks']['items']

        #Response returns a dictionary with these values:
        # album, artists, available_markets, disc_number, duration_ms, explicit
        # external_ids, external_urls, href, id, is_playable, linked_from,
        # name, popularity, preview_url, track_number, type, uri





    

if __name__ == "__main__":
    print(timezone.now())