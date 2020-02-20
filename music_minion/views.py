from django.shortcuts import render
from django.views.generic import ListView 
from portfolio.models import Technologies
from .forms import SpotifySearchForm, SpotifyPlaylistForm
from . import spotify
import json, random
import numpy as np

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

    #Check user access_token before making requests
    message = spotify_auth.check_auth(request)

    #Get a users playlists and save the names and ids
    playlists = spotify_user_data.get_user_playlists(user.username, user.access_token)
    playlist_names = [playlist['name'] for playlist in playlists['items']]
    playlist_ids = [playlist['id'] for playlist in playlists['items']]
    
    tracks, rec_tracks = None, None

    if request.method == 'POST':
        form = SpotifyPlaylistForm(request.POST, playlists=playlist_names)
        if form.is_valid():
            playlist = form.cleaned_data.get('playlist')
            i = playlist_names.index(playlist)
            playlist_id = playlist_ids[i]
            tracks = spotify_user_data.get_playlist_songs(playlist_id, user.access_token)[1]

            #Get recommendations based on the songs in the playlist
            
            #Only 5 aritsts/tracks/genres can be used, by default we will give recommendations based on tracks
            #Choose 5 tracks at random
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
            message = "Form Not Valid?"
    else:
        form = SpotifyPlaylistForm(playlists=playlist_names)
    
    return render(request, 'music_minion/playlist.html', {'form':form, 'tracks':tracks, 'message':message, 'rec_tracks':rec_tracks})
