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
            "redirect_uri": "https://127.0.0.1:8000/profile",
            "client_id": secrets.PINTEREST_APP_ID,
            "scope": "read_public, write_public, read_relationships, write_relationships",
        }
        params = urlencode(auth_code_dict, True)
        return self.api_url + "oauth/?" + params

    def get_access_token(self, code):
        access_token_dict = {
            "grant_type": "authorization_code",
            "client_id": secrets.bonz_pinterest_app_id,
            "client_secret": secrets.bonz_pinterest_app_secret_key,
            "code": code,
        }
        response = requests.post(
            self.api_url + "v1/oauth/token", data=access_token_dict
        )
        if "access_token" in json.loads(response.text):
            return json.loads(response.text)["access_token"]
        else:
            return response.text

    def set_username(self, access_token=None):
        user = current_user
        username_dict = {"access_token": user.access_token, "fields": "username"}
        response = requests.get(self.api_url + "v1/me", params=username_dict)
        user_data = json.loads(response.text)
        try:
            user.username = user_data["data"]["username"]
            db.session.commit()
            return user_data["data"]["username"]
        except:
            return (response, user_data)

    def post_item_to_pinterest(self, listing, title):
        user = current_user
        item_dictionary = {
            "access_token": secrets.BONZ_PINTEREST_ACCESS_TOKEN,
            "board": "BonanzaMarket"
            + "/"
            + "-".join(title.replace("'", "").split()).lower(),
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

    def create_pinterest_board(self, title):
        item_dictionary = {
            "access_token": secrets.BONZ_PINTEREST_ACCESS_TOKEN,
            "name": title.replace("'", ""),
        }

        response = requests.post(
            self.api_url + "v1/boards/", params=item_dictionary
        )
        response_data = json.loads(response.text)
        if "data" in response_data:
            if "url" in response_data:
                board_url = Board(
                    url=response_data["data"]["url"],
                    board_name=title,
                    user=current_user,
                )
                session.add(board_url)
                session.commit()
                return response_data["data"]["url"]
        elif "message" in response_data:
            if "DuplicateBoardSlugException" in response_data["message"]:
                print("Is Duplicate")
                return response_data["message"]
        else:
            print("Response data" + str(response_data))
            return response_data

    def get_user_info(self):
        username_dict = {
            "access_token": "Ata0gPkksPFjJSLxFBGma0jV5fh2FY9ZD9Sp17ZFr4fbGYClgACaADAAAAA0RbURD3sgt4gAAAAA"
        }
        response = requests.get(self.api_url + "v1/me/", params=username_dict)
        user_data = json.loads(response.text)
        try:
            self.username = user_data["data"]["username"]
        except:
            return (response, user_data)


if __name__ == "__main__":
    p = Pinterest()
    print(p.get_user_info())
