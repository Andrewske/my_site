from django.urls import path
from . import views
from my_site import giphy

urlpatterns = [
    path('', views.HomeListView.as_view(), name='portfolio-home'),
    path('contact/', views.contactView, name='contact'),
    path('success/', views.successView, name='success')
]