from django.urls import path
from . import views
from my_site import giphy


urlpatterns = [
    path('', views.index, name='index'),   
    path('get_listings/', views.get_listings, name='get_listings'),
    path('pin_list/', views.create_and_post, name='pin_list'),    
]