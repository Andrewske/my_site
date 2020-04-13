from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeView, name='music-minion-home'),
    path('search/', views.searchView, name='music-minion-search'),
    path('playlist/', views.playlistView, name='music-minion-playlist'),
    path('get_playlist_tracks/', views.get_playlist_tracks, name='get_playlist_tracks'),
    path('get_youtube_tracks/', views.get_youtube_tracks, name='get_youtube_tracks'),
    path('make_youtube_playlist/', views.make_youtube_playlist, name='make_youtube_playlist'),
    path('youtube/', views.youtubeView, name='youtube'),
    path('spotify_to_youtube/', views.spotifyToYoutube, name='spotify-to-youtube'),
]