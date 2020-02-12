from datetime import datetime, timedelta
import requests, json
import time
import secrets

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
import urllib

access_token = 'BQAGuXWiuaJTD2tZTRjBerH247XpWE0M4w8NLS3AGwer35tkCzB-IPCcwRh5IL5zMiJvVze0uNScdW72h2xOiwR3mUxCoeY7VQc6lxB5A9-VDhC0WJerCAZVs6VORHGH4nBqqm-a1GIgnvkVvTNcbVHmEVTAAPPzsFUO1ccXjDkf2BzcYhoIzrz8IcLa8PwnOrb08Db0sXYslndwV7YL0SsyBzRs9QjV9LXReISTdZc5E7J6BEIXQWHsVV1r1GE'

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
            return json.dumps(response_data)
    
def get_recommendations(access_token, limit=25, min_values=None, max_values=None, artists=None, genres=None, tracks=None, target_values=None):

    url = 'https://api.spotify.com/v1/recommendations'

    #User can select any number of minimum values
    #This form is super dynamic and would probably be easier done in javascript

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

    if min_values:
        for k,v in min_values.items():
            recommend_dict[k] = v

    if max_values:
        for k,v in max_values.items():
            recommend_dict[k] = v
    
    if target_values:
        for k,v in target_values.items():
            recommend_dict[k] = v

    data = {k: v for k, v in recommend_dict.items() if v is not None}

    header_value = "Bearer " + access_token
    response = requests.get(url, params=data, headers={"Authorization": header_value})
    response_data = json.loads(response.text)

    if response.status_code == 200:
        tracks = [track for track in response_data['tracks']]
        return SpotifyTrackData().clean_track_response(tracks, access_token)
    else:
        return response_data


playlist_url = 'https://open.spotify.com/playlist/66esoX3teBQdi0Z44Q12Qj?si=suhoNLyITW2Vu2Jb5iIgOg'
playlist_id = '66esoX3teBQdi0Z44Q12Qj'
tracks = ["4JpKVNYnVcJ8tuMKjAj50A","2NRANZE9UCmPAS5XVbXL00","24JygzOLM0EmRQeGtFcIcG"]
target_values = {'target_tempo':150}
min_values = {'min_tempo':145}
max_values = {'max_tempo':155}

print(get_recommendations(access_token, limit=5, tracks=tracks, target_values=target_values, min_values=min_values, max_values=max_values))
