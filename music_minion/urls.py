from django.urls import path
from . import views

urlpatterns = [
    path('', views.MinionListView.as_view(), name='music-minion-home'),
]