import requests, json
from my_site import secrets

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


class Pinterest:
    def __init__(self):
        self.api_url = "https://api.pinterest.com/"
        self.username = None
        self.board_name = None

    def get_auth_url(self):
        auth_code_dict = {
            "response_type": "code",
            "redirect_uri": "https://kevinandrews.info/hpltopin/get_listings",
            "client_id": secrets.PINTEREST_APP_ID,
            "scope": "read_public, write_public, read_relationships, write_relationships",
            "state": "98926"
        }
        params = urlencode(auth_code_dict, True)
        return self.api_url + "oauth/?" + params

    def get_access_token(self, code):
        access_token_dict = {
            "grant_type": "authorization_code",
            "client_id": secrets.PINTEREST_APP_ID,
            "client_secret": secrets.PINTEREST_SECRET_KEY,
            "code": code,
        }
        response = requests.post(
            self.api_url + "v1/oauth/token", data=access_token_dict
        )
        if "access_token" in json.loads(response.text):
            result = 1
            access_token = json.loads(response.text)["access_token"]
            return result, access_token
        else:
            result = 0
            return result, response.text

    def post_item_to_pinterest(self, access_token, username,  listing, title):
        item_dictionary = {
            "access_token": access_token,
            "board": username
            + "/"
            + title,
            "note": listing["price"] + " " + listing["title"],
            "link": listing["itemUrl"],
            "image_url": listing["pictureURL"],
        }
        
        response = requests.post(self.api_url + "v1/pins/", params=item_dictionary)
        response_data = json.loads(response.text)
        try:
            return response_data["data"]["url"]
        except:
            return response_data

    def create_pinterest_board(self, access_token, title):
        item_dictionary = {
            "access_token": access_token,
            "name": title,
        }

        response = requests.post(
            self.api_url + "v1/boards/", params=item_dictionary
        )
        response_data = json.loads(response.text)
        try:
            board_url = response_data["data"]["url"]
            return [1, board_url]
        except:
            return [2, json.dumps(response_data)]


    def get_username(self, access_token):
        username_dict = {
            "access_token": access_token,
            "fields": "username"
        }
        response = requests.get(self.api_url + "v1/me/", params=username_dict)
        user_data = json.loads(response.text)
        try:
            username = user_data["data"]["username"]
            result = 1
            return result, username
        except:
            result = 0
            return result, user_data


if __name__ == "__main__":
    p = Pinterest()
    print(p.get_auth_url())
