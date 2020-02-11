from datetime import datetime, timedelta
import requests, json
import time
import secrets
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
import urllib

access_token = 'BQCVkCT8MDWTIytj0fs9i9RErLNCmFTkHswfSM7yUF9CwID3SYuvcJ8tzJSwanhDpt1_tVHfmm1ZMbnvJZQrAy-M7Ww6f6oOb0pDGBHRgIG7U56HWp5qKM2M7u9DvK1uQ7myxzys44obtc_e33Jbw0FjpKa0p-4kYqaTAbHB-vhMlxXxl9A-69zRmXEqC8dZ-ApV4be6RflvlJmJpTkjT9agOPE8fGoUdpNe7eIqE-i4C0feEB0_1pSQDLkayG8'


    
def get_user_data(access_token):
    url = 'https://api.spotify.com/v1/me'
    header_value = "Bearer " + access_token
    response = requests.get(
        url, headers={"Authorization": header_value}
    )
    response_data = json.loads(response.text)
    return response_data

def get_playlist_songs(playlist_id, access_token, fields=None, limit=100, offset=0):
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
        return response_data['items'][0]['track'].keys()
    else:
        return None

playlist_url = 'https://open.spotify.com/playlist/66esoX3teBQdi0Z44Q12Qj?si=suhoNLyITW2Vu2Jb5iIgOg'
playlist_id = '66esoX3teBQdi0Z44Q12Qj'
tracks = ["4JpKVNYnVcJ8tuMKjAj50A","2NRANZE9UCmPAS5XVbXL00","24JygzOLM0EmRQeGtFcIcG"]
print(get_playlist_songs(playlist_id, access_token))
