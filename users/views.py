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
from background_task import background
from background_task.models import Task

p = pinterest.Pinterest()
spotify_auth = spotify.SpotifyAuth()
spotify_user_data = spotify.SpotifyUserData()
spotify_track_data = spotify.SpotifyTrackData()
spotify_tasks = spotify.SpotifyRepeatTasks()


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
            spotify_user.dw_monthly_updated_at = datetime.now()
            spotify_user.save()
            
            spotify_tasks.dw_monthly_task(spotify_user_id=spotify_user.user_id, repeat=360, creator=spotify_user)
            messages.success(request, f'Your monthly playlist automation has begun.')
        
        elif 'monthly_disconnect' in request.POST:
            spotify_user.dw_monthly = False
            spotify_user.dw_monthly_updated_at = datetime.now()
            spotify_user.save()
            Task.objects.created_by(spotify_user).filter(task_name="music_minion.spotify.dw_monthly_task").delete()
            messages.success(request, f'Your monthly playlist automation has ended.')
            
        elif 'yearly' in request.POST:
            spotify_track_data.discover_weekly_playlist(spotify_user.username, spotify_user.access_token, 'yearly')
            spotify_user.dw_yearly = True
            spotify_user.dw_yearly_updated_at = datetime.now()
            spotify_user.save()
            spotify_tasks.dw_yearly_task(spotify_user_id=spotify_user.user_id, repeat=360, creator=spotify_user)
            messages.success(request, f'Your yearly playlist automation has begun.')
        
        elif 'yearly_disconnect' in request.POST:
            spotify_user.dw_yearly = False
            spotify_user.dw_yearly_updated_at = datetime.now()
            spotify_user.save()
            Task.objects.created_by(spotify_user).filter(task_name="music_minion.spotify.dw_yearly_task").delete()

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
        dw_monthly = spotify_user.dw_monthly
        dw_yearly = spotify_user.dw_yearly
        dw_monthly_updated_at = spotify_user.dw_monthly_updated_at
        dw_yearly_updated_at = spotify_user.dw_yearly_updated_at
    except:
        spotify_access_token = None
        spotify_user_id = None
        dw_monthly = False
        dw_yearly = False
        dw_monthly_updated_at = None
        dw_yearly_updated_at = None

    message = timezone.now() - spotify_user.auth_date

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'dw_monthly': dw_monthly,
        'dw_yearly': dw_yearly,
        'dw_monthly_updated_at': dw_monthly_updated_at,
        'dw_yearly_updated_at':dw_yearly_updated_at,
        'pinterest_auth_url': p.get_auth_url(),
        'spotify_auth_url':spotify_auth.get_auth_url()[0],
        'spotify_access_token': spotify_access_token,
        'message': message,
    }

    
    
    return render(request, 'users/profile.html', context)
