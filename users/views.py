from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, SpotifyDWPlaylistForm
from hpltopin import pinterest
from music_minion import spotify
from music_minion.models import SpotifyUser, SpotifyTasks
from datetime import datetime
from django.utils import timezone
import json

p = pinterest.Pinterest()
spotify_auth = spotify.SpotifyAuth()
spotify_user_data = spotify.SpotifyUserData()
spotify_track_data = spotify.SpotifyTrackData()


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created. Please Login')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})

@login_required
def profile(request):
    user = request.user
    message = None
    
    try:
        spotify_user = user.spotifyuser
        spotify_auth.check_auth(request)
    except:
        message = "No Spotify User"

    code = request.GET.get("code", None)
    
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, 
                                   request.FILES, 
                                   instance=request.user.profile)

        if 'monthly' in request.POST:
            spotify_track_data.discover_weekly_playlist(spotify_user.username, spotify_user.access_token, 'monthly')
            spotify_user.dw_monthly = True
            spotify_user.dw_updated_at = datetime.now()
            spotify_user.save()
            messages.success(request, f'Your monthly playlist automation has begun.')
        
        elif 'monthly_disconnect' in request.POST:
            spotify_user.dw_monthly = False
            spotify_user.dw_updated_at = datetime.now()
            spotify_user.save()
            messages.success(request, f'Your monthly playlist automation has ended.')
            
        elif 'yearly' in request.POST:
            spotify_track_data.discover_weekly_playlist(spotify_user.username, spotify_user.access_token, 'yearly')
            spotify_user.dw_yearly = True
            spotify_user.updated_at = datetime.now()
            spotify_user.save()
            messages.success(request, f'Your yearly playlist automation has begun.')
        
        elif 'yearly_disconnect' in request.POST:
            spotify_user.dw_yearly = False
            spotify_user.dw_updated_at = datetime.now()
            spotify_user.save()
            messages.success(request, f'Your yearly playlist automation has ended.')

        elif u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated.')
        return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        spotify_form = SpotifyDWPlaylistForm()
    
    if code != None:
        state = request.GET.get("state", None)
        error = request.GET.get("error", None)
        if state:
            integration = state.split('_')[0] 
        if error:
            message = error
        if integration == 'spotify':
            response = spotify_auth.get_access_token(code)
            if response[0] == 1:
                try:
                    access_token = response[1]['access_token']
                    refresh_token = response[1]['refresh_token']
                    user_data = spotify_user_data.get_user_data(access_token)
                    spotify_user = SpotifyUser(user_id=user.id, username=user_data['id'], access_token=access_token, refresh_token=refresh_token)
                    spotify_user.save()
                    message = "Spotify connection successful!"
                except Exception as x:
                    message_dict = {
                        'exception': str(x),
                        'user_id': user.id,
                        'access_token': response[1]['access_token'],
                        'refresh_token': response[1]['refresh_token'],
                    }
                    message = "Error: Database save failed!" + json.dumps(message_dict)
            elif response[0] == 2:
                message = "Error: Spotify Connection Failed: " + json.dumps(response[1])

    try:
        spotify_access_token = user.spotifyuser.access_token
        spotify_user_id = user.spotifyuser.username
    except:
        spotify_access_token = None
        spotify_user_id = None

        
    #message = spotify_user.access_token

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'dw_monthly': spotify_user.dw_monthly,
        'dw_yearly': spotify_user.dw_yearly,
        'dw_updated_at': spotify_user.dw_updated_at,
        'pinterest_auth_url':p.get_auth_url(),
        'spotify_auth_url':spotify_auth.get_auth_url()[0],
        'spotify_access_token': spotify_access_token,
        'message': spotify_user.user_id,
    }

    
    
    return render(request, 'users/profile.html', context)
