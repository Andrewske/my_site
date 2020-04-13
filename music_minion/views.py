from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import ListView 
from portfolio.models import Technologies
from .forms import SpotifySearchForm, SpotifyPlaylistForm
from . import spotify, youtube
from my_site import giphy
import json, random
import numpy as np
from .models import SpotifyUser
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from allauth.socialaccount.models import SocialToken

spotify_search = spotify.SpotifySearch()
spotify_auth = spotify.SpotifyAuth()
spotify_user_data = spotify.SpotifyUserData()
spotify_tasks = spotify.SpotifyRepeatTasks()



class MinionListView(ListView):
    model = Technologies
    template_name = 'music_minion/homepage.html'
    context_object_name = 'technologies'
    ordering = ['-date_added']

def homeView(request):
    minion_gif = giphy.get_gif('dj minion')
    message = None
    return render(request, 'music_minion/homepage.html', {'minion_gif':minion_gif, 'message':message})

def searchView(request):
    user = request.user.spotifyuser
    message = spotify_auth.check_auth(request)

    genres = spotify_search.available_genres(user.access_token)

    if request.method == 'POST':
        form = SpotifySearchForm(request.POST, genres=genres)
        if form.is_valid():
            search_type = form.cleaned_data.get('search_type')
            genre = form.cleaned_data.get('genre')
            query = form.cleaned_data.get('query')
            if search_type == 'track':
                tracks = spotify_search.find_songs(access_token= user.access_token, q=query)
                context = {
                    'form':form,
                    'tracks': tracks[1],
                    'message':tracks[0],
                    'tracks_json':json.dumps(tracks[1])
                }
                return render(request, 'music_minion/search.html', context=context)
        else:
            context = {
                'form':form,
                'message':'Form not Valid',
            }
            return render(request, 'music_minion/search.html', context=context)
    else: 
        form = SpotifySearchForm(genres=genres)

    return render(request, 'music_minion/search.html', {'form':form, 'message':message})


def playlistView(request):
    user = request.user.spotifyuser
    
    #Check user access_token before making requests
    message = spotify_auth.check_auth(user.user_id)
    
    if message == 'Access Token Updated':
        return redirect('music-minion-playlist')

    user = request.user.spotifyuser

    #Get a users playlists and save the names and ids
    playlists = spotify_user_data.get_user_playlists(user.username, user.access_token)
    playlist_values = [(playlist['id'], playlist['name']) for playlist in playlists['items']]
    playlist_names = [playlist['name'] for playlist in playlists['items']]
    playlist_ids = [playlist['id'] for playlist in playlists['items']]
    
    tracks, rec_tracks = None, None
    '''
    if request.method == 'POST':
        form = SpotifyPlaylistForm(request.POST, playlists=playlist_values)
        if form.is_valid():
            playlist = form.cleaned_data.get('playlist')
            i = playlist_names.index(playlist)
            playlist_id = playlist_ids[i]
            
            tracks = spotify_user_data.get_playlist_songs(playlist_id, user.access_token)


            #Get recommendations based on the songs in the playlist
            
            #Only 5 aritsts/tracks/genres can be used, by default we will give recommendations based on tracks
            #Choose 5 tracks at random
            if isinstance(tracks, list):
                track_ids = [track['id'] for track in tracks]
                seed_tracks = random.sample(track_ids, 5)

                #Use the average values to set targets
                target_values = {
                    'target_danceability': int(np.mean([track['danceability'] for track in tracks])),
                    'target_energy': int(np.mean([track['energy'] for track in tracks])),
                    #'target_key': int(np.mean([track['key'] for track in tracks])),
                    'target_loudness': int(np.mean([track['loudness'] for track in tracks])),
                    'target_mode': int(np.mean([track['mode'] for track in tracks])),
                    'target_speechiness': int(np.mean([track['speechiness'] for track in tracks])),
                    'target_acousticness': int(np.mean([track['acousticness'] for track in tracks])),
                    'target_instrumentalness': int(np.mean([track['instrumentalness'] for track in tracks])),
                    'target_valence': int(np.mean([track['valence'] for track in tracks])),
                    'target_tempo': int(np.mean([track['tempo'] for track in tracks])),
                }

                #Find recommendations with these values
                rec_tracks = spotify_search.get_recommendations(user.access_token, tracks=seed_tracks, target_values=target_values)[1]
            else:
                message = tracks
        else:
            message = "Form Not Valid?"
    else:
        '''
    form = SpotifyPlaylistForm(playlists=playlist_values)
    
    

    return render(request, 'music_minion/playlist.html', {'form':form, 'tracks':tracks, 'message':message, 'rec_tracks':rec_tracks, 'user_id':user.user_id })



def get_playlist_tracks(request):
    print("getting playlist tracks")
    playlist_id = request.POST.get('playlist_id')
    user = get_object_or_404(SpotifyUser, user_id=request.POST.get('user_id'))
    use = request.POST.get('use') 
    print(str(playlist_id) + " : " + str(use))
    tracks = spotify_user_data.get_playlist_songs(playlist_id, user.access_token)
    #tracks = [{'id': '2RqZFOLOnzVmHUX7ZMcaES', 'name': 'Let It Go', 'img_url': 'https://i.scdn.co/image/ab67616d00001e02911ef35f75422d0482cec8bf', 'artists': "Keyshia Cole, Missy Elliott, Lil' Kim", 'href': 'https://api.spotify.com/v1/tracks/2RqZFOLOnzVmHUX7ZMcaES', 'popularity': 66, 'uri': 'spotify:track:2RqZFOLOnzVmHUX7ZMcaES', 'release_date': '2007-01-01', 'danceability': 0.806, 'energy': 0.721, 'key': '3A', 'loudness': -5.167, 'mode': 0, 'speechiness': 0.215, 'acousticness': 0.197, 'instrumentalness': 0, 'liveness': 0.209, 'valence': 0.781, 'tempo': 94, 'time_signature': 4, 'duration_ms': 238333}, {'id': '7EwPR8nTPQpWl9qSXzkHpq', 'name': '21 Questions', 'img_url': 'https://i.scdn.co/image/ab67616d00001e020770fe27caff8948d0cea4ec', 'artists': 'Unwrapped', 'href': 'https://api.spotify.com/v1/tracks/7EwPR8nTPQpWl9qSXzkHpq', 'popularity': 26, 'uri': 'spotify:track:7EwPR8nTPQpWl9qSXzkHpq', 'release_date': '2005', 'danceability': 0.666, 'energy': 0.678, 'key': '1A', 'loudness': -6.007, 'mode': 0, 'speechiness': 0.0298, 'acousticness': 0.415, 'instrumentalness': 0.232, 'liveness': 0.127, 'valence': 0.633, 'tempo': 94, 'time_signature': 4, 'duration_ms': 266733}, {'id': '0aj2QKJvz6CePykmlTApiD', 'name': 'Señorita', 'img_url': 'https://i.scdn.co/image/ab67616d00001e02346a5742374ab4cf9ed32dee', 'artists': 'Justin Timberlake', 'href': 'https://api.spotify.com/v1/tracks/0aj2QKJvz6CePykmlTApiD', 'popularity': 65, 'uri': 'spotify:track:0aj2QKJvz6CePykmlTApiD', 'release_date': '2002-11-04', 'danceability': 0.841, 'energy': 0.629, 'key': '3B', 'loudness': -5.351, 'mode': 1, 'speechiness': 0.0442, 'acousticness': 0.0729, 'instrumentalness': 0, 'liveness': 0.0742, 'valence': 0.87, 'tempo': 97, 'time_signature': 4, 'duration_ms': 294867}, {'id': '0uEp9E98JB5awlA084uaIg', 'name': 'Doo Wop (That Thing)', 'img_url': 'https://i.scdn.co/image/ab67616d00001e02e08b1250db5f75643f1508c9', 'artists': 'Ms. Lauryn Hill', 'href': 'https://api.spotify.com/v1/tracks/0uEp9E98JB5awlA084uaIg', 'popularity': 73, 'uri': 'spotify:track:0uEp9E98JB5awlA084uaIg', 'release_date': '1998-08-25', 'danceability': 0.535, 'energy': 0.505, 'key': '7A', 'loudness': -8.926, 'mode': 0, 'speechiness': 0.245, 'acousticness': 0.0393, 'instrumentalness': 0, 'liveness': 0.0923, 'valence': 0.495, 'tempo': 99, 'time_signature': 4, 'duration_ms': 320267}, {'id': '3TjE3A8tLih7KBwKJ03Htl', 'name': 'New Vibe Who Dis (feat. Little League)', 'img_url': 'https://i.scdn.co/image/ab67616d00001e02ebd63c63c3435d89535888a1', 'artists': 'Madison Mars, Little League', 'href': 'https://api.spotify.com/v1/tracks/3TjE3A8tLih7KBwKJ03Htl', 'popularity': 63, 'uri': 'spotify:track:3TjE3A8tLih7KBwKJ03Htl', 'release_date': '2019-08-23', 'danceability': 0.699, 'energy': 0.933, 'key': '3A', 'loudness': -3.504, 'mode': 0, 'speechiness': 0.175, 'acousticness': 0.16, 'instrumentalness': 5.62e-06, 'liveness': 0.196, 'valence': 0.646, 'tempo': 123, 'time_signature': 4, 'duration_ms': 191500}]
   
    context = {
        'tracks':tracks
    }

    if request.is_ajax():
        if use == 'table':
            html = render_to_string('music_minion/playlist_table.html', context, request=request)
            return JsonResponse({'form':html})
        elif use == 'list':
            print(tracks)
            return JsonResponse(tracks, safe=False)
    else: 
        print("Invalid Request")

def get_youtube_tracks(request):
    print("Getting Youtube Tracks")
    track_id = request.POST.get('track_id')
    artists = request.POST.get('artists')
    name = request.POST.get('name')
    user = get_object_or_404(User, id=request.POST.get('user_id'))
    access_token = str(SocialToken.objects.filter(account__user=user, account__provider='google')[:1].get())
    search_query = str(artists) + " - " + str(name)
    tracks = youtube.search_youtube(search_query, access_token)
    #tracks = [{'id': '2RqZFOLOnzVmHUX7ZMcaES', 'name': 'Let It Go', 'img_url': 'https://i.scdn.co/image/ab67616d00001e02911ef35f75422d0482cec8bf', 'artists': "Keyshia Cole, Missy Elliott, Lil' Kim", 'href': 'https://api.spotify.com/v1/tracks/2RqZFOLOnzVmHUX7ZMcaES', 'popularity': 66, 'uri': 'spotify:track:2RqZFOLOnzVmHUX7ZMcaES', 'release_date': '2007-01-01', 'danceability': 0.806, 'energy': 0.721, 'key': '3A', 'loudness': -5.167, 'mode': 0, 'speechiness': 0.215, 'acousticness': 0.197, 'instrumentalness': 0, 'liveness': 0.209, 'valence': 0.781, 'tempo': 94, 'time_signature': 4, 'duration_ms': 238333}, {'id': '7EwPR8nTPQpWl9qSXzkHpq', 'name': '21 Questions', 'img_url': 'https://i.scdn.co/image/ab67616d00001e020770fe27caff8948d0cea4ec', 'artists': 'Unwrapped', 'href': 'https://api.spotify.com/v1/tracks/7EwPR8nTPQpWl9qSXzkHpq', 'popularity': 26, 'uri': 'spotify:track:7EwPR8nTPQpWl9qSXzkHpq', 'release_date': '2005', 'danceability': 0.666, 'energy': 0.678, 'key': '1A', 'loudness': -6.007, 'mode': 0, 'speechiness': 0.0298, 'acousticness': 0.415, 'instrumentalness': 0.232, 'liveness': 0.127, 'valence': 0.633, 'tempo': 94, 'time_signature': 4, 'duration_ms': 266733}, {'id': '0aj2QKJvz6CePykmlTApiD', 'name': 'Señorita', 'img_url': 'https://i.scdn.co/image/ab67616d00001e02346a5742374ab4cf9ed32dee', 'artists': 'Justin Timberlake', 'href': 'https://api.spotify.com/v1/tracks/0aj2QKJvz6CePykmlTApiD', 'popularity': 65, 'uri': 'spotify:track:0aj2QKJvz6CePykmlTApiD', 'release_date': '2002-11-04', 'danceability': 0.841, 'energy': 0.629, 'key': '3B', 'loudness': -5.351, 'mode': 1, 'speechiness': 0.0442, 'acousticness': 0.0729, 'instrumentalness': 0, 'liveness': 0.0742, 'valence': 0.87, 'tempo': 97, 'time_signature': 4, 'duration_ms': 294867}, {'id': '0uEp9E98JB5awlA084uaIg', 'name': 'Doo Wop (That Thing)', 'img_url': 'https://i.scdn.co/image/ab67616d00001e02e08b1250db5f75643f1508c9', 'artists': 'Ms. Lauryn Hill', 'href': 'https://api.spotify.com/v1/tracks/0uEp9E98JB5awlA084uaIg', 'popularity': 73, 'uri': 'spotify:track:0uEp9E98JB5awlA084uaIg', 'release_date': '1998-08-25', 'danceability': 0.535, 'energy': 0.505, 'key': '7A', 'loudness': -8.926, 'mode': 0, 'speechiness': 0.245, 'acousticness': 0.0393, 'instrumentalness': 0, 'liveness': 0.0923, 'valence': 0.495, 'tempo': 99, 'time_signature': 4, 'duration_ms': 320267}, {'id': '3TjE3A8tLih7KBwKJ03Htl', 'name': 'New Vibe Who Dis (feat. Little League)', 'img_url': 'https://i.scdn.co/image/ab67616d00001e02ebd63c63c3435d89535888a1', 'artists': 'Madison Mars, Little League', 'href': 'https://api.spotify.com/v1/tracks/3TjE3A8tLih7KBwKJ03Htl', 'popularity': 63, 'uri': 'spotify:track:3TjE3A8tLih7KBwKJ03Htl', 'release_date': '2019-08-23', 'danceability': 0.699, 'energy': 0.933, 'key': '3A', 'loudness': -3.504, 'mode': 0, 'speechiness': 0.175, 'acousticness': 0.16, 'instrumentalness': 5.62e-06, 'liveness': 0.196, 'valence': 0.646, 'tempo': 123, 'time_signature': 4, 'duration_ms': 191500}]
    if request.is_ajax():
        return JsonResponse(tracks, safe=False)
    else: 
        print("Invalid Request")


def youtubeView(request):
    message = None
    minion_gif = giphy.get_gif('dj minion')
    user = request.user
    access_token = str(SocialToken.objects.filter(account__user=user, account__provider='google')[:1].get())
    
    message = youtube.create_playlist('Test Playlist', access_token)

    return render(request,'music_minion/youtube.html', {'message': message, 'minion_gif':minion_gif,})

def spotifyToYoutube(request):
    user = request.user
    spotify_user = user.spotifyuser
    
    message = spotify_auth.check_auth(spotify_user.user_id)
    
    if message == 'Access Token Updated':
        return redirect('spotify-to-youtube')

    spotify_tracks = [{'track_img': user.profile.image.url, 'title': "Song #1", "artist": "Kevin"}]
    youtube_tracks = [{'track_img': user.profile.image.url, 'title': "Song #1", "artist": "Kevin"}]
    
    playlists = spotify_user_data.get_user_playlists(spotify_user.username, spotify_user.access_token)
    playlist_values = [(playlist['id'], playlist['name']) for playlist in playlists['items']]
    playlist_form = SpotifyPlaylistForm(playlists=playlist_values)

    context = {
        'spotify_tracks':spotify_tracks,
        'youtube_tracks':youtube_tracks,
        'playlist_form':playlist_form,
    }

    return render(request,'music_minion/spotify_to_youtube.html', context=context)

def make_youtube_playlist(request):
    track_ids = request.POST.get('track_ids')
    playlist_name = request.POST.get('playlist_name')
    user = get_object_or_404(SpotifyUser, user_id=request.POST.get('user_id'))
    tracks = [{'id': '2RqZFOLOnzVmHUX7ZMcaES', 'name': 'Let It Go', 'img_url': 'https://i.scdn.co/image/ab67616d00001e02911ef35f75422d0482cec8bf', 'artists': "Keyshia Cole, Missy Elliott, Lil' Kim", 'href': 'https://api.spotify.com/v1/tracks/2RqZFOLOnzVmHUX7ZMcaES', 'popularity': 66, 'uri': 'spotify:track:2RqZFOLOnzVmHUX7ZMcaES', 'release_date': '2007-01-01', 'danceability': 0.806, 'energy': 0.721, 'key': '3A', 'loudness': -5.167, 'mode': 0, 'speechiness': 0.215, 'acousticness': 0.197, 'instrumentalness': 0, 'liveness': 0.209, 'valence': 0.781, 'tempo': 94, 'time_signature': 4, 'duration_ms': 238333}, {'id': '7EwPR8nTPQpWl9qSXzkHpq', 'name': '21 Questions', 'img_url': 'https://i.scdn.co/image/ab67616d00001e020770fe27caff8948d0cea4ec', 'artists': 'Unwrapped', 'href': 'https://api.spotify.com/v1/tracks/7EwPR8nTPQpWl9qSXzkHpq', 'popularity': 26, 'uri': 'spotify:track:7EwPR8nTPQpWl9qSXzkHpq', 'release_date': '2005', 'danceability': 0.666, 'energy': 0.678, 'key': '1A', 'loudness': -6.007, 'mode': 0, 'speechiness': 0.0298, 'acousticness': 0.415, 'instrumentalness': 0.232, 'liveness': 0.127, 'valence': 0.633, 'tempo': 94, 'time_signature': 4, 'duration_ms': 266733}, {'id': '0aj2QKJvz6CePykmlTApiD', 'name': 'Señorita', 'img_url': 'https://i.scdn.co/image/ab67616d00001e02346a5742374ab4cf9ed32dee', 'artists': 'Justin Timberlake', 'href': 'https://api.spotify.com/v1/tracks/0aj2QKJvz6CePykmlTApiD', 'popularity': 65, 'uri': 'spotify:track:0aj2QKJvz6CePykmlTApiD', 'release_date': '2002-11-04', 'danceability': 0.841, 'energy': 0.629, 'key': '3B', 'loudness': -5.351, 'mode': 1, 'speechiness': 0.0442, 'acousticness': 0.0729, 'instrumentalness': 0, 'liveness': 0.0742, 'valence': 0.87, 'tempo': 97, 'time_signature': 4, 'duration_ms': 294867}, {'id': '0uEp9E98JB5awlA084uaIg', 'name': 'Doo Wop (That Thing)', 'img_url': 'https://i.scdn.co/image/ab67616d00001e02e08b1250db5f75643f1508c9', 'artists': 'Ms. Lauryn Hill', 'href': 'https://api.spotify.com/v1/tracks/0uEp9E98JB5awlA084uaIg', 'popularity': 73, 'uri': 'spotify:track:0uEp9E98JB5awlA084uaIg', 'release_date': '1998-08-25', 'danceability': 0.535, 'energy': 0.505, 'key': '7A', 'loudness': -8.926, 'mode': 0, 'speechiness': 0.245, 'acousticness': 0.0393, 'instrumentalness': 0, 'liveness': 0.0923, 'valence': 0.495, 'tempo': 99, 'time_signature': 4, 'duration_ms': 320267}, {'id': '3TjE3A8tLih7KBwKJ03Htl', 'name': 'New Vibe Who Dis (feat. Little League)', 'img_url': 'https://i.scdn.co/image/ab67616d00001e02ebd63c63c3435d89535888a1', 'artists': 'Madison Mars, Little League', 'href': 'https://api.spotify.com/v1/tracks/3TjE3A8tLih7KBwKJ03Htl', 'popularity': 63, 'uri': 'spotify:track:3TjE3A8tLih7KBwKJ03Htl', 'release_date': '2019-08-23', 'danceability': 0.699, 'energy': 0.933, 'key': '3A', 'loudness': -3.504, 'mode': 0, 'speechiness': 0.175, 'acousticness': 0.16, 'instrumentalness': 5.62e-06, 'liveness': 0.196, 'valence': 0.646, 'tempo': 123, 'time_signature': 4, 'duration_ms': 191500}]
    
    if request.is_ajax():
        return JsonResponse(tracks, safe=False)
    else: 
        print("Invalid Request")

    