from django.contrib import messages
import requests, json
from requests.auth import HTTPBasicAuth
from my_site import secrets
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from django.utils import timezone
from .models import SpotifyUser
from allauth.socialaccount.models import SocialToken, SocialAccount
from requests_oauthlib import OAuth2Session


try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

def get_oauth2_session(request):
    """ Create OAuth2 session which autoupdates the access token if it has expired """

    # This needs to be amended to whatever your refresh_token_url is.
    refresh_token_url = 'https://oauth2.googleapis.com/token' #AzureOAuth2Adapter.refresh_token_url
    
    social_token = SocialToken.objects.get(account__user=request.user)


    if not social_token.expires_at:
        print("No Expiration")
    else:
        print(social_token.expires_at)

    def token_updater(token):
        social_token.token = token['access_token']
        social_token.token_secret = token['refresh_token']
        social_token.expires_at = timezone.now() + timedelta(seconds=int(token['expires_in']))
        social_token.save()

    client_id = social_token.app.client_id
    client_secret = social_token.app.secret

    extra = {
        'client_id': client_id,
        'client_secret': client_secret
    }

    expires_in = (social_token.expires_at - timezone.now()).total_seconds()
    token = {
        'access_token': social_token.token,
        'refresh_token': social_token.token_secret,
        'token_type': 'Bearer',
        'expires_in': expires_in  # Important otherwise the token update doesn't get triggered.
    }
    
    client =  OAuth2Session(client_id, token=token, auto_refresh_kwargs=extra, 
                         auto_refresh_url=refresh_token_url, token_updater=token_updater)
    return client.get('https://www.googleapis.com/oauth2/v1/userinfo')


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
        return clean_youtube_tracks(response_data)
    except Exception as x:
        return ["No Tracks Available", str(x)]

def clean_youtube_tracks(data):
    tracks = []
    for track in data['items']:
        track_data = {
            'id':track['id']['videoId'],
            'name':track['snippet']['title'],
            'artists':track['snippet']['channelTitle'],
            'img_url':track['snippet']['thumbnails']['high']['url']
        }
        tracks.append(track_data)
    return tracks


def create_playlist(title, access_token):
    url = 'https://www.googleapis.com/youtube/v3/playlists'


    resource = {
        "kind":"youtube#playlist",
        "snippet" : {
            'title':title,
        },
    }

    data = {
        'part':'snippet',
    }

    header_value = "Bearer " + str(access_token)
    response = requests.post(url, params=data, json=resource, headers= {"Authorization": header_value, "Content-Type":'application/json'})
    response_data = json.loads(response.text)
    
    try:
        return response_data['id']
    except Exception as x:
        return ["No Tracks Available", response_data]

def add_to_playlist(track_id, playlist_id, access_token):
    url = 'https://www.googleapis.com/youtube/v3/playlistItems'
    
    resource = {
        'kind': 'youtube#playlistItem',
        'snippet': {
            'playlistId': playlist_id,
            'resourceId':{
                'kind': 'youtube#video',
                'videoId': track_id,
            }
        },
    }

    data = {
        'part':'snippet',
    }

    header_value = "Bearer " + str(access_token)
    response = requests.post(url, params=data, json=resource, headers= {"Authorization": header_value, "Content-Type":'application/json'})
    response_data = json.loads(response.text)
    try:
        return ["Success", track_id]
    except Exception as x:
        return ["Failure", str(x), track_id]