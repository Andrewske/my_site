from datetime import datetime, timedelta
import requests, json
import time
import secrets
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
import urllib

access_token = 'BQB7Ov_L0zIs0i1C-HGTaleQt1RT35MmQoa0t50iMBbrIANbhNTTCFNpPfA68HUZtIyCX8GpA7S96k1O4cy3_1C-mMLCqbxlQL7b60uyZpNSV7OTEHckz366u4JLLL1ez6Jl0kKzJ2r-9WZLMHmAYG1KaPiL7meK9H_QOsJexIS8d3usUOKyQ6siPTnRdo2Way0uCUziFT9QvQd9KnrlCxdkyxtQLT7sCAudD0h9_AZ811HFRJA6O__VNzzc0xQ'


def check_date():
    time1 = datetime.now()
    time.sleep(60)
    time2 = datetime.now()
    diff = time2-time1
    print(diff)
    if diff > timedelta(minutes=1):
        print('yes')
    else:
        print('no')

    
def find_songs(access_token, limit=2, offset=None, q=None):
    #Response returns a dictionary with these values:
    # album, artists, available_markets, disc_number, duration_ms, explicit
    # external_ids, external_urls, href, id, is_playable, linked_from,
    # name, popularity, preview_url, track_number, type, uri

    url = 'https://api.spotify.com/v1/search'
    message = None

    data = {
        'q': q,
        'type':'track',
        'limit':limit,
    }

    if offset:
        data['offset'] = offset

    header_value = "Bearer " + access_token
    response = requests.get(url, params=data, headers={"Authorization": header_value})
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
        print(tracks)
        try:
            track_features = get_track_features(tracks, access_token)
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


def get_track_features(tracks, access_token):
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
                    'tempo':track['tempo'],
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
        return response_data

tracks = ["4JpKVNYnVcJ8tuMKjAj50A","2NRANZE9UCmPAS5XVbXL00","24JygzOLM0EmRQeGtFcIcG"]
print(find_songs(access_token, q='Skrillex'))
#print(get_track_features(tracks, access_token))