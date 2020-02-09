from datetime import datetime, timedelta
import requests, json
import time
import secrets

access_token = 'BQC2zlGAca3KPiRe_5vbW2bONGexWJptHYmEchTJH2eKhDIPCyKE5qcsKgx-b1HZRAMjR3JaelOm8jZ6I4zKdxVzRtLz6dQAFhK0AX-Hl80J_j9fky9lDY4knWhMJakRKXJ0Sft-C35mh5ek5uQ5-Tn8T56iBPppboA3Vlgn52pmxDV350anoAqipO6qF2HpEEy9cU1jbElmtYO7p2_PlRzqNERrp3qUr3LM4kKvvilgI1I-F6FHPAIv3lDEPhE'


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

def find_songs(search_type=None, limit=2, offset=None, q=None):
    url = 'https://api.spotify.com/v1/search'

    data = {
        'q': q,
        'type':search_type,
        'limit':limit,
    }

    if offset:
        data['offset'] = offset
    

    header_value = "Bearer " + access_token

    response = requests.get(url, params=data, headers={"Authorization": header_value})
    response_data = json.loads(response.text)
    return response_data['tracks']['items'][0]['name']

print(find_songs(search_type='track', q='skrillex'))