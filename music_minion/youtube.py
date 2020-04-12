from django.contrib import messages
import requests, json
from requests.auth import HTTPBasicAuth
from my_site import secrets
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from .models import SpotifyUser
from allauth.socialaccount.models import SocialAccount


try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

def search_youtube(search_term, access_token): #https://developers.google.com/youtube/v3/docs/search/list
    url = 'https://www.googleapis.com/youtube/v3/search'

    data = {
        'part':'snippet',
        'maxResults':5,
        'order': 'relevance', #date, rating, relevance, title, videoCount, viewCount
        'q':search_term,
        'type':'video', #channel, playlist, video
        #'videoCategoryId': None, Maybe use music?

    }
    header_value = "Bearer " + str(access_token)
    response = requests.get(url, params=data, headers={"Authorization": header_value})
    response_data = json.loads(response.text)
    try:
        return response_data
    except Exception as x :
        return ["No Genres Available", str(x)]