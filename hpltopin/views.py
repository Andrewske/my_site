from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import bonanza
from my_site import giphy


def index(request):
    if request.user.is_authenticated:
        welcome_gif=giphy.get_gif("hi friend")
        return render(request, "hpltopin/user_homepage.html", context={'welcome_gif':welcome_gif})
    else:
        welcome_gif=giphy.get_gif("hi")
        return render(request, "hpltopin/anon_homepage.html", context={'welcome_gif':welcome_gif})


@login_required
def pin_list(request):
    if request.method == "POST":
        hpl_url = request.POST.get("hpl_url")
        listings, title = bonanza.find_listings(hpl_url)
        listings_info = bonanza.get_items_information(listings)
        return render(request, 'hpltopin/pin_list.html',
            {
                'listing_count':len(listings),
                'board_name':title,
                'hpl_url':hpl_url,
            }
            
        )
    else:
        return render(request, 'hpltopin/pin_list.html')