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
        #Response returns a dictionary with these values:
        # album, artists, available_markets, disc_number, duration_ms, explicit
        # external_ids, external_urls, href, id, is_playable, linked_from,
        # name, popularity, preview_url, track_number, type, uri

        message = None

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

        if response.status_code == 200:
            #Clean the response to keep only data we want, and add data from track_features
            cleaned_tracks = []
            for track in response_data['tracks']['items']:
                new_dict = {
                    'id': track['id'],
                    'name': track['name'],
                    'artists': ', '.join(artist['name'] for artist in track['artists']),
                    'href': track['href'],
                    'popularity': track['popularity'],
                }
                cleaned_tracks.append(new_dict)

            #Get the track ids and find audio features
            tracks = [track['id'] for track in response_data['tracks']['items']]
            try:
                track_features = self.get_track_features(tracks, access_token)
            except Exception as x:
                track_features = None
                message = "Couldn't Get Track Features"

            #If there are track features add them to the dictionaries
            if track_features:
                for i in range(len(track_features)):
                    if track_features[i]:
                        cleaned_tracks[i].update(track_features[i])

            return [message, cleaned_tracks]
        else:
            message = response_data
            return [message, None]



    def get_track_features(self, tracks, access_token):
        url = 'https://api.spotify.com/v1/audio-features/'
        data = {
            'ids': ','.join(tracks),
        }
        params = urlencode(data, True)
        header_value = "Bearer " + access_token
        response = requests.get(url, params=params, headers={"Authorization": header_value})
        response_data = json.loads(response.text)

        if response.status_code == 200:
            tracks = []
            for track in response_data['audio_features']:
                try:
                    track_features = {
                        'danceability': track['danceability'],
                        'energy': track['energy'],
                        'key': track['key'],
                        'loudness': track['loudness'],
                        'mode': track['mode'],
                        'speechiness': track['speechiness'],
                        'acousticness': track['acousticness'],
                        'instrumentalness': track['instrumentalness'],
                        'liveness': track['liveness'],
                        'valence': track['valence'],
                        'tempo': int(track['tempo']),
                        'time_signature':track['time_signature'],
                        'duration_ms':track['duration_ms'],
                    }
                except:
                    track_features = {
                        'danceability': 'Not Available',
                        'energy': 'Not Available',
                        'key': 'Not Available',
                        'loudness': 'Not Available',
                        'mode': 'Not Available',
                        'speechiness': 'Not Available',
                        'acousticness': 'Not Available',
                        'instrumentalness': 'Not Available',
                        'liveness': 'Not Available',
                        'valence': 'Not Available',
                        'tempo': 'Not Available',
                        'time_signature': 'Not Available',
                        'duration_ms': 'Not Available',
                    }
                tracks.append(track_features)
            return tracks
        else:
            return None

    def get_recommendations(self, access_token, limit=25, min=None, max=None, artists=None, genres=None, tracks=None, target=None):

        url = 'https://api.spotify.com/v1/recommendations'

        #User can select any number of minimum values
        #This form is super dynamic and would probably be easier done in javascript
        #Saving this function for another day. Shows that I need to complete that CodeAcademy Course        


class SpotifyUserData():

    def __init__(self):
        self.api_url = 'https://api.spotify.com/v1/users/'

    def get_user_data(self, access_token):
        url = 'https://api.spotify.com/v1/me'
        header_value = "Bearer " + access_token
        response = requests.get(
            url, headers={"Authorization": header_value}
        )
        response_data = json.loads(response.text)
        
        if response.status_code == 200:
            return response_data
        else:
            return None

    
    def get_user_playlists(self, user_id, access_token):
        pass
    

if __name__ == "__main__":
    print(timezone.now())