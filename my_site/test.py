import pycurl_requests as requests
import json


access_token = 'BQBaSpF1yvn02BCna3Kuq8SPgRh2g0_M0LL51iBsFAt-WVIBhWZ-F1nndCX6No0ZSzLEGBFIeVDyQ77D76p8b_9vm3e7IhRAhNe0b69ikbbdjPLD3SsScQKKYjx2FJnKZWMYslMgz2ohgwIBkjsuiaa37eCBO1ml_8SeTvuSYL6rpFkMNQlNKPFd0kOxszXM18vbxvj_yAVjfJlO-qVG4DN_4tRyJkOIaEyPFig_Bdag8dRoP1UJ7kGPT86y6dU'

def spotify():
    playlist_id = '5zaqtQk3NGJwstUuyAR8SW'
    url = 'https://api.spotify.com/v1/playlists/' + playlist_id + '/tracks'

    data = {
        'fields':['total'],
        'market':'from_token'
    }

    header_value = "Bearer " + access_token

    response = requests.get(url, params=data, headers={"Authorization": header_value})
    response_data = json.loads(response.text)
    print(response)
    try:
        return response_data['total']
    except Exception as e:
        return "Can't get total: " + str(e)

spotify()
