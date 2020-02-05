from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import bonanza, pinterest
from my_site import giphy
import re

p = pinterest.Pinterest()

no_success_gif = giphy.get_gif("Uh Oh")
success_gif = giphy.get_gif("success")

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
        request.session['code'] = request.GET.get("code", None)
        if request.session['code'] != None :
            return render(request, 'hpltopin/user_homepage.html', {'auth_url':p.get_auth_url()})
        else:
            result, access_token = p.get_access_token(request.session['code'])
            if result == 1:
                request.session['access_token'] = access_token
                response, username = p.get_username(access_token)
                if response == 1:
                    request.session['username'] = username
                    return render(request, 'hpltopin/get_listings.html', {'username': request.session['username'], 'message':request.session['access_token']})
                else:
                    message = username 
                    return render(request, 'hpltopin/no_success.html', {'message':message, 'no_success_gif':no_success_gif})
            else:
                return render(request, 'hpltopin/no_success.html', {'message':message,  'no_success_gif':no_success_gif})

        

def create_and_post(request):
    username = request.session['username']
    listings = request.session['listings']
    access_token = request.session['access_token']
    title = request.session['title']
    title_url = '-'.join([re.sub(r'\W+','', word).lower() for word in title.split(' ')])

    response = p.create_pinterest_board(access_token, title)

    if 'rate limit' in response[1]:
        return render(request, 'hpltopin/no_success.html', {'message':response[1], 'no_success_gif':no_success_gif})
    elif response[0] == 1:
        board_url = response[1]
    else:
        board_url = "https://www.pinterest.com/" + username + "/" + title_url
    
    #Try to post the listings
    pin_urls = []
    for listing in listings[:2]:
        pin_urls.append(p.post_item_to_pinterest(access_token, username, listing, title_url))
    
    errors = 0
    for url in pin_urls:
        if 'message' in url:
            errors += 1
    
    if errors > 0:
        message = str(errors) + " pins received an error:" + "\n" + "\n".join([pin_urls])
        return render(request, 'hpltopin/no_success.html', {'message':message, 'no_success_gif':no_success_gif})
    else:
        return render(request, 'hpltopin/success.html', {'pin_urls':pin_urls, 'board_url':board_url, 'success_gif':success_gif})
    