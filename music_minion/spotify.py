from background_task import background
from django.contrib import messages
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
from .models import SpotifyUser, SpotifyTasks

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


class SpotifyAuth:

    def __init__(self):
        self.api_url = "https://accounts.spotify.com/"
        self.prod_redirect_uri = "http://kevinandrews.info/profile"
        self.test_redirect_uri = "http://127.0.0.1:8000/profile"

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
            "redirect_uri": self.prod_redirect_uri,
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
            "redirect_uri": self.prod_redirect_uri
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
    # If that time is > 1 hour we need to request a new token
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
            tracks = [track for track in response_data['tracks']['items']]
            return SpotifyTrackData().clean_track_response(tracks, access_token)
        else:
            message = response_data
            return [message, None]


    def get_recommendations(self, access_token, limit=25, min_values=None, max_values=None, artists=None, genres=None, tracks=None, target_values=None):

        url = 'https://api.spotify.com/v1/recommendations'

        #Full dictionary of values that a user can provide for recommendations
        recommend_dict = {
            'limit': limit,
            'market':'from_token',
            'seed_artists': artists,
            'seed_genres': genres,
            'seed_tracks': tracks,
            'min_acousticness':None,
            'max_acousticness':None,
            'target_acousticness':None,
            'min_danceability':None,
            'max_danceability':None,
            'target_danceability':None,
            'min_duration_ms':None,
            'max_duration_ms':None,
            'target_duration_ms':None,
            'min_energy':None,
            'max_energy':None,
            'target_energy':None,
            'min_instrumentalness':None,
            'max_instrumentalness':None,
            'target_instrumentalness':None,
            'min_key':None,
            'max_key':None,
            'target_key':None,
            'min_liveness':None,
            'max_liveness':None,
            'target_liveness':None,
            'min_loudness':None,
            'max_loudness':None,
            'target_loudness':None,
            'min_mode':None,
            'max_mode':None,
            'target_mode':None,
            'min_popularity':None,
            'max_popularity':None,
            'target_popularity':None,
            'min_speechiness':None,
            'max_speechiness':None,
            'target_speechiness':None,
            'min_tempo':None,
            'max_tempo':None,
            'target_tempo':None,
            'min_time_signature':None,
            'max_time_signature':None,
            'target_time_signature':None,
            'min_valence':None,
            'max_valence':None,
            'target_valence':None,
        }

        #If minimum, maximum, or target values are provided add them to the dictionary
        if min_values:
            for k,v in min_values.items():
                recommend_dict[k] = v

        if max_values:
            for k,v in max_values.items():
                recommend_dict[k] = v
        
        if target_values:
            for k,v in target_values.items():
                recommend_dict[k] = v

        #Remove any dictionary keys with None values
        data = {k: v for k, v in recommend_dict.items() if v is not None}

        header_value = "Bearer " + access_token
        response = requests.get(url, params=data, headers={"Authorization": header_value})
        response_data = json.loads(response.text)

        if response.status_code == 200:
            tracks = [track for track in response_data['tracks']]
            return SpotifyTrackData().clean_track_response(tracks, access_token)
        else:
            return response_data

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

    
    def get_user_playlists(self, user_id, access_token, limit=50, offset=0):
        
        url = self.api_url + user_id + '/playlists'

        data = {
            'limit': limit,
            'offset': offset,
        }
        header_value = "Bearer " + access_token

        response = requests.get(url, params=data, headers={"Authorization": header_value})
        response_data = json.loads(response.text)

        if response.status_code == 200:
            return response_data
        else:
            return response_data

    def get_playlist_songs(self, playlist_id, access_token, fields=None, limit=100, offset=0):
        url = 'https://api.spotify.com/v1/playlists/' + playlist_id + '/tracks'

        data = {
            'limit':limit,
            'offset':offset,
            'fields':fields,
            'market':'from_token'
        }

        header_value = "Bearer " + access_token

        response = requests.get(url, params=data, headers={"Authorization": header_value})
        response_data = json.loads(response.text)

        if response.status_code == 200:
            tracks = [track['track'] for track in response_data['items']]
            return SpotifyTrackData().clean_track_response(tracks, access_token)
        else:
            return None

    def create_playlist(self, access_token,  user_id, playlist_name):
        url = 'https://api.spotify.com/v1/users/' + user_id + '/playlists'
        
        data = {
            'name': playlist_name,
        }

        header_value = "Bearer " + access_token

        response = requests.post(url, json=data, headers= {"Authorization": header_value, "Content-Type":'application/json'})
        response_data = json.loads(response.text)

        try:
            return response_data['id']
        except:
            return response_data




class SpotifyTrackData():

    def __init__(self):
        self.api_url = "https:"

    def clean_track_response(self, tracks, access_token):
        message = None
        #Clean the response to keep only data we want, and add data from track_features
        cleaned_tracks = []
        for track in tracks:
            new_dict = {
                'id': track['id'],
                'name': track['name'],
                'artists': ', '.join(artist['name'] for artist in track['artists']),
                'href': track['href'],
                'popularity': track['popularity'],
                'uri': track['uri'],
                'release_date': track['album']['release_date'],
            }
            cleaned_tracks.append(new_dict)

        #Get the track ids and find audio features
        track_ids = [track['id'] for track in tracks]
        try:
            track_features = self.get_track_features(track_ids, access_token)
        except Exception as x:
            track_features = None
            message = "Couldn't Get Track Features" + str(x)

        #If there are track features add them to the dictionaries
        if track_features:
            for i in range(len(track_features)):
                if track_features[i]:
                    cleaned_tracks[i].update(track_features[i])

        return [message, cleaned_tracks]


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
                        'key': self.convert_key(track['key'], track['mode']),
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
            return json.dumps(response_data)

    def convert_key(self, key, mode):

        pitch_class = {
            0 : 'C',
            1 : 'Db',
            2 : 'D',
            3 : 'Eb',
            4 : 'E',
            5 : 'F',
            6 : 'Gb',
            7 : 'G',
            8 : 'Ab',
            9 : 'A',
            10 : 'Bb',
            11 : 'B'
        }

        pitch = pitch_class[key]

        camelot_major = {
            'B' : '1B',
            'Gb' : '2B',
            'Db' : '3B',
            'Ab' : '4B',
            'Eb' : '5B',
            'Bb' : '6B',
            'F' : '7B',
            'C' : '8B',
            'G' : '9B',
            'D' : '10B',
            'A' : '11B',
            'E' : '12B'
        }

        camelot_minor = {
            'Ab' : '1A',
            'Eb' : '2A',
            'Bb' : '3A',
            'F' : '4A',
            'C' : '5A',
            'G' : '6A',
            'D' : '7A',
            'A' : '8A',
            'E' : '9A',
            'B' : '10A',
            'Gb' : '11A',
            'Db' : '12A'
        }

        if mode == 1:
            return camelot_major[pitch]
        elif mode == 0:
            return camelot_minor[pitch]
        else:
            return 'No Mode'

    def add_to_playlist(self, access_token, playlist_id, uri_list):
        url = 'https://api.spotify.com/v1/playlists/' + playlist_id + '/tracks'

        data = {
            'uris' : ['spotify:track:'+ str(uri) for uri in uri_list],
        }

        header_value = "Bearer " + access_token

        response = requests.post(url, json=data, headers={"Authorization": header_value, 'Content-Type':'application/json'})
        response_data = json.loads(response.text)

        if response.status_code == 200:
            return 'Tracks Added'
        else:
            return response_data

    def save_tracks(self, request, tracks):
        pass

    def discover_weekly_playlist(self, user_id, access_token, interval):

        #Response Data
        data = {
            'message':None, 
            'updated_at': None, 
            'exception': None
            }

        #Find or create spotify playlist based on interval
        user_playlists = SpotifyUserData().get_user_playlists(user_id, access_token)

        try:
            playlists = [[playlist['name'], playlist['id']]  for playlist in user_playlists['items']]
        except:
            return user_playlists
        
        if interval == "monthly":
            playlist_name = datetime.now().strftime("%b") + ' ' + datetime.now().strftime("%y") + ' - Discover Weekly'
        else:
            playlist_name = datetime.now().strftime("%Y") + ' Discover Weekly'
        
        playlist_id = None

        for playlist in playlists:
            if playlist[0] == playlist_name:
                playlist_id = playlist[1]
                break

        if not playlist_id:
            playlist_id = SpotifyUserData().create_playlist(access_token, user_id, playlist_name)

        #Get discover weekly tracks
        tracks = None
        track_ids = None

        for playlist in playlists:
            if playlist[0] == 'Discover Weekly':
                dw_id = playlist[1]
                tracks = SpotifyUserData().get_playlist_songs(dw_id, access_token)
                try:
                    track_ids = [track['id'] for track in tracks[1]]
                except:
                    track_ids = None
                break

        #Add tracks to the new playlist
        
        message = SpotifyTrackData().add_to_playlist(access_token, playlist_id, track_ids)

        return playlist_id
        
        
        
class SpotifyRepeatTasks():

    def __init__(self):
        self.users = None

    @background(schedule=60)
    def dw_monthly_task(self, spotify_user_id):
        user = SpotifyUser.filter(user_id=spotify_user_id)
        time_since_updated = datetime.now(timezone.utc) - user.dw_updated_at
        if time_since_updated.total_seconds() >= 60:
            monthly = '' 
            if user.dw_monthly:
                SpotifyTrackData().discover_weekly_playlist(user.username, user.access_token, 'monthly')
                user.dw_updated_at = datetime.now(timezone.utc)
                user.save()
                monthly = 'Monthly'
        else:
            pass
        
        return time_since_updated.total_seconds()
        
    #@background(schedule=60)
    def dw_yearly_task(self, spotify_user_id):
        user = SpotifyUser.filter(user_id=spotify_user_id)
        time_since_updated = datetime.now(timezone.utc) - user.dw_updated_at
        if time_since_updated.total_seconds() >= 60:
            if user.dw_yearly:
                SpotifyTrackData().discover_weekly_playlist(user.username, user.access_token, 'yearly')
                user.dw_updated_at = datetime.now(timezone.utc)
                user.save()
        else:
            pass
        
        return time_since_updated.total_seconds()


if __name__ == "__main__":
    print(timezone.now())