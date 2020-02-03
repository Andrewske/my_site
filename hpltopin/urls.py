from django.urls import path
from . import views
from my_site import giphy


urlpatterns = [
    path('', views.index, name='index'),   
]