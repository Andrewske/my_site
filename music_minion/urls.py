from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeView, name='music-minion-home'),
    path('search/', views.searchView, name='music-minion-search'),
    path('playlist/', views.playlistView, name='music-minion-playlist'),
    path('repeat_tasks/', views.RepeatTaskView, name='repeat-tasks'),
]