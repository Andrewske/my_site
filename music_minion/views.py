from django.shortcuts import render
from django.views.generic import ListView 
from portfolio.models import Technologies
from .forms import SpotifySearchForm, SpotifyPlaylistForm
from . import spotify
import json

spotify_search = spotify.SpotifySearch()
spotify_auth = spotify.SpotifyAuth()
spotify_user_data = spotify.SpotifyUserData()



class MinionListView(ListView):
    model = Technologies
    template_name = 'music_minion/homepage.html'
    context_object_name = 'technologies'
    ordering = ['-date_added']


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
    playlists = spotify_user_data.get_user_playlists(user.username, user.access_token)
    playlist_names = [playlist['name'] for playlist in playlists['items']]
    playlist_ids = [playlist['id'] for playlist in playlists['items']]
    tracks, message = None, None

    if request.method == 'POST':
        form = SpotifyPlaylistForm(request.POST, playlists=playlist_names)
        if form.is_valid():
            playlist = form.cleaned_data.get('playlist')
            i = playlist_names.index(playlist)
            playlist_id = playlist_ids[i]
            tracks = spotify_user_data.get_playlist_songs(playlist_id, user.access_token)
        else:
            message = "Form Not Valid?"
    else:
        form = SpotifyPlaylistForm(playlists=playlist_names)
    
    return render(request, 'music_minion/playlist.html', {'form':form, 'tracks':tracks[1], 'message':message})
