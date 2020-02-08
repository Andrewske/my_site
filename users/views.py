from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from hpltopin import pinterest
from music_minion import spotify

p = pinterest.Pinterest()
spotify = spotify.Spotify()

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
    code = request.GET.get("code", None)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, 
                                   request.FILES, 
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated.')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    if code != None:
        state = request.GET.get("state", None)
        error = request.GET.get("error", None)
        integration = requests.session['state'].spit('_')[0] 
        if error:
            message = integration + ': ' + state
            messages.ERROR(request, message)
            return redirect('profile' )
        if integration == 'spotify':
            response = spotify.get_access_token(code)
            message = response
            return render(request, 'users/register.html', {'message':message})

    spotify_data = spotify.get_auth_url()
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'pinterest_auth_url':p.get_auth_url(),
        'spotify_auth_url':spotify_data[0],
        'spotify_state': spotify_data[1]
    }
    
    return render(request, 'users/profile.html', context)
