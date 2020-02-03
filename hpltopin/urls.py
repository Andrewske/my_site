from django.urls import path
from . import views
from my_site import giphy


urlpatterns = [
    path('', views.index, name='index'),   
    path('pin_list/', views.pin_list, name='pin_list'),  
]