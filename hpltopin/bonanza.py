import re, json, urllib, requests
from bs4 import BeautifulSoup

url = "https://api.bonanza.com/api_requests/secure_request"

headers = {
    "Content-Type": "application/json; charset=utf-8",
    "X-BONANZLE-API-DEV-NAME": "iElmtQLpdrVHJ7Z",
    "X-BONANZLE-API-CERT-NAME": "jSA8b0otHxRcgWe",
}

listings = ["660154339", "669928968", "644198149", "650819038", "668243296"]

hpl_url = None


def set_hpl(url):
    global hpl_url
    hpl_url = url


def find_listings(url):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    elements = soup.find_all("a", attrs={"class": "image_wrap"})
    listings = []
    for l in elements:
        href = l.get("href")
        listings.append(re.match(".*?([0-9]+)$", href).group(1))
    title = soup.title.string
    title = title.replace(" - Hand Picked List", "")
    return listings, title




def get_items_information(listings):
    request_name = "getMultipleItemsRequest"

    # Turn listings array into dictionary
    item_dictionary = {"itemID": [i for i in listings]}

    # convert dictionary to json
    payload = json.dumps({request_name: item_dictionary})

    # make the request to Bonanza
    response = requests.post(url, data=payload, headers=headers)

    # the json response as a dictionary
    response_json = response.json()

    # build array of dictionarys
    listings_information = []

    if (
        response_json["ack"] == "Success"
        and "getMultipleItemsResponse" in response_json
    ):
        for item in response_json["getMultipleItemsResponse"]["item"]:
            listings_information.append(
                {
                    "title": item["title"],
                    "price": item["currentPrice"],
                    "itemUrl": item["viewItemURL"],
                    "pictureURL": item["pictureURL"][0],
                }
            )
    else:
        return response_json

    return listings_information


if __name__ == "__main__":
    # hpl_url = 'https://www.bonanza.com/hpl/Garden-Tools/163708'
    # print(find_listings('https://www.bonanza.com/hpl/Shades-and-Sunnies/163720'))
    print(get_items_information(['126125989', '562254958']))

