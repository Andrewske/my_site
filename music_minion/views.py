from django.shortcuts import render
from django.views.generic import ListView 
from portfolio.models import Technologies



class MinionListView(ListView):
    model = Technologies
    template_name = 'music_minion/homepage.html'
    context_object_name = 'technologies'
    ordering = ['-date_added']


