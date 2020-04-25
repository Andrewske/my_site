from datetime import datetime, timedelta
import requests, json
import time


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
        return response_data
        

access_token = 'BQC2p5MGB5Lzs-1h1T5NUNlxtEA6SkMVAK5q1JBTjsEhQLeXGTEXLBUYvtVtxyyA2r8xLy4F362XiRh_1RSqm_vBvx-cXcrVO5kTaqPe2EUsJoMC1dv0HeeJ5iN5_GrkoNCVDDD42MXl6H-kNaBJduXckoouNDBq6iuDO5EcSC422i-CD7uZzv5DbZfjmMlIal9wD9kMRJDFArKgSmAq7fSAxL1VxW-e9RqIB4HdAksVGOoMF4LEfEHMTHkfel0'
playlist_url = 'https://open.spotify.com/playlist/66esoX3teBQdi0Z44Q12Qj?si=suhoNLyITW2Vu2Jb5iIgOg'
playlist_id = '66esoX3teBQdi0Z44Q12Qj'
tracks = ["4JpKVNYnVcJ8tuMKjAj50A","2NRANZE9UCmPAS5XVbXL00","24JygzOLM0EmRQeGtFcIcG"]
target_values = {'target_tempo':150}
min_values = {'min_tempo':145}
max_values = {'max_tempo':155}

print(get_user_playlists('kevinbigfoot', access_token))









