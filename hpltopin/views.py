from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import bonanza, pinterest
from my_site import giphy

p = pinterest.Pinterest()

def index(request):
    if request.user.is_authenticated:
        welcome_gif=giphy.get_gif("hi friend")
        pinterest_auth_url = p.get_auth_url()
        return render(request, "hpltopin/user_homepage.html", context={
            'welcome_gif':welcome_gif,
            'pinterest_auth_url':pinterest_auth_url,
            })
    else:
        welcome_gif=giphy.get_gif("hi")
        pinterest_auth_url = p.get_auth_url()
        return render(request, "hpltopin/user_homepage.html", context={
            'welcome_gif':welcome_gif,
            'pinterest_auth_url':pinterest_auth_url,
            })



def get_listings(request):
    request.session['code'] = request.GET.get("code", None)
    if request.session['code'] == None:
        return render(request, 'hpltopin/user_homepage.html', {'auth_url':p.get_auth_url()})
    else:
        result, access_token = p.get_access_token(request.session['code'])
        if result == 1:
            request.session['access_token'] = access_token
            response, username = p.get_username(access_token)
            if response == 1:
                request.session['username'] == username
                if request.method == "POST":
                    hpl_url = request.POST.get("hpl_url")
                    listings, title = bonanza.find_listings(hpl_url)
                    listings_info = bonanza.get_items_information(listings)
                    request.session['title'] = title
                    request.session['listings'] = listings_info
                    return render(request, 'hpltopin/get_listings.html',
                        {
                            'username': request.session['username'],
                            'listing_count':len(listings),
                            'listings':listings_info,
                            'board_name':title,
                            'hpl_url':hpl_url,
                        }        
                    )
                else:
                    return render(request, 'hpltopin/get_listings.html', {'username': request.session['username']})
            else:
                message = username 
            return render(request, 'hpltopin/user_homepage.html', {'message':message})
        else:
            message = access_token 
            return render(request, 'hpltopin/user_homepage.html', {'message':message})

        

def create_and_post(request):
    try:
        title = request.session['title']
        username = request.session['username']
        listings = request.session['listings']
        access_token = request.session['access_token']

        result, board_url = p.create_pinterest_board(access_token, title)
        if result == 1:
            pin_urls = []
            for listing in listings:
                pin_urls.append(p.post_item_to_pinterest(access_tokem, username, listing, title))
            return render(request, 'hpltopin/success.html', {'pin_urls':pin_urls, 'board_url':board_url})
        else:
            return render(request, 'hpltopin/no_success.html', {'message':board_url})

    except:
        return render(request, 'hpltopin/no_success.html')