from datetime import datetime, timedelta
import requests, json
import time
import secrets
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
import urllib

access_token = 'BQBnM9uDIVzMZJGtrhwb9GSrC5EIC107Z6o-kuFMW67bGC1jRvz8t3wZXAs3SX64U6vUkcZgta3A8OVCdJF7Bjx3YEDNjyt7cyseX-YVnHZ2I0X3tOvggl_rygi_xR1OSSgcihqdyJc5An_s3lfnRq9pkQ_nZ7wvarF813VzHwfZr7vFSpuj40_X6_NrBugHPoRMzRIf5sIHEIAdiOe6cajO55mRNJnA5Amw7Fha6JSiLHEKNrQjw8iJkj83Htk'


    
def get_user_data(access_token):
    url = 'https://api.spotify.com/v1/me'
    header_value = "Bearer " + access_token
    response = requests.get(
        url, headers={"Authorization": header_value}
    )
    response_data = json.loads(response.text)
    return response_data

tracks = ["4JpKVNYnVcJ8tuMKjAj50A","2NRANZE9UCmPAS5XVbXL00","24JygzOLM0EmRQeGtFcIcG"]
print(get_user_data(access_token))
