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
def get_listings(request):
    if request.method == "POST":
        hpl_url = request.POST.get("hpl_url")
        listings, title = bonanza.find_listings(hpl_url)
        listings_info = bonanza.get_items_information(listings)
        request.session['title'] = title
        request.session['listings'] = listings_info
        return render(request, 'hpltopin/get_listings.html',
            {
                'listing_count':len(listings),
                'listings':listings_info,
                'board_name':title,
                'hpl_url':hpl_url,
            }
            
        )
    else:
        return render(request, 'hpltopin/get_listings.html')

@login_required
def create_and_post(request):
    title = request.session['title']
    listings = request.session['listings']
    return render(request, 'hpltopin/success.html', 
        {
            'listings': listings,
            'title':title,
        }
    )