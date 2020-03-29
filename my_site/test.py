from datetime import datetime, timedelta
import requests, json
import time
import secrets


spotify_track_data = spotify.SpotifyTrackData()
spotify_user_data = spotify.SpotifyUserData()

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
import urllib

user_id = 'kevinbigfoot'
access_token = 'BQAWuM_WbzXJ5WSxCXO-pka9T-8-hVsHSPJblRKy686Zs6wA2peAZVvnAlPT_ibN50RPNiFJ8m-dZV7pIIKBdk5nRSQCaybVsfURoi1qu-t3JqclE_XCwxVdgBhdSceQFmiYaKHToLWJxBRJgL_as-Vp62EJe5YMO05cO1IWsu-yrmEB6T8XRuuE1qjQO5dM6PCPK4yi0PICxkcvMM0QaWtvuF2X6vI-w-s1GgwD6LJ8mxFIbJ3-D2aTud44PRA'

def get_user_playlists(user_id, access_token, limit=50, offset=0):
        
        url = 'https://api.spotify.com/v1/users/' + user_id + '/playlists'

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
            return None

def create_playlist(access_token,  user_id, playlist_name):
    url = 'https://api.splotify.com/v1/users/' + user_id + '/playlists'
    
    data = {
        'Content-Type': 'application/json',
        'name': playlist_name,
    }

    header_value = "Bearer " + access_token

    response = requests.get(url, params=data, headers= {"Authorization": header_value})
    response_data = json.loads(response.text)

    try:
        return response_data['id']
    except:
        return Exception

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
    
def discover_weekly_playlist(user_id, access_token, interval):

    #Response Data
    data = {
        'message':None, 
        'updated_at': None, 
        'exception': None
        }

    #Find or create spotify playlist based on interval
    user_playlists = get_user_playlists(user_id, access_token)
    playlists = [[playlist['name'], playlist['id']]  for playlist in user_playlists['items']]
    if interval == "Month":
        playlist_name = str(datetime.now().Month) + ' ' + str(datetime.now().Year) + ' Discover Weekly'
    else:
        playlist_name = str(datetime.now().year) + ' Discover Weekly'

    if playlist_name in playlists:
            playlist_id = ['id']
    else:
        playlist_id = create_playlist(access_token, playlist_name)

    #Get discover weekly tracks
    for playlist in playlists:
        if playlist['name'] == 'Discover Weekly':
            dw_id = playlist['id']
            tracks = get_playlist_songs(dw_id, access_token)
            track_ids = [track['id'] for track in tracks]

    #Add tracks to the new playlist
    try:
        data['message'] = spotify_track_data.add_to_playlist(access_token, playlist_id, track_ids)
    except:
        data['exception'] = Exception

    return data


print(discover_weekly_playlist(user_id, access_token, 'Month'))


playlist_url = 'https://open.spotify.com/playlist/66esoX3teBQdi0Z44Q12Qj?si=suhoNLyITW2Vu2Jb5iIgOg'
playlist_id = '66esoX3teBQdi0Z44Q12Qj'
tracks = ["4JpKVNYnVcJ8tuMKjAj50A","2NRANZE9UCmPAS5XVbXL00","24JygzOLM0EmRQeGtFcIcG"]
target_values = {'target_tempo':150}
min_values = {'min_tempo':145}
max_values = {'max_tempo':155}

#print(get_recommendations(access_token, limit=5, tracks=tracks, target_values=target_values, min_values=min_values, max_values=max_values))









