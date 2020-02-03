from django.shortcuts import render

from my_site import giphy


def index(request):
    if request.user.is_authenticated:
        welcome_gif=giphy.get_gif("hi friend")
        return render(request, "hpltopin/user_homepage.html", context={'welcome_gif':welcome_gif})
    else:
        welcome_gif=giphy.get_gif("hi")
        return render(request, "hpltopin/anon_homepage.html", context={'welcome_gif':welcome_gif})