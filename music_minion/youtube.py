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

    data = {
        'part':'snippet',
        'snippet.title' : title,
    }
    header_value = "Bearer " + str(access_token)
    response = requests.post(url, params=data, headers={"Authorization": header_value})
    response_data = json.loads(response.text)
    try:
        return response_data
    except Exception as x:
        return ["No Tracks Available", str(x)]

def add_to_playlist(track_id, playlist_id, access_token):
    url = 'https://www.googleapis.com/youtube/v3/playlists'
    details = {
        videoId: track_id,
        kind: 'youtube#video',
    }
    data = {
        'part':'snippet',
        'snippet.playlist_id' : title,
        'resourceId' : details,
    }
    header_value = "Bearer " + str(access_token)
    response = requests.post(url, params=data, headers={"Authorization": header_value})
    response_data = json.loads(response.text)
    try:
        return response_data
    except Exception as x:
        return ["No Tracks Available", str(x)]