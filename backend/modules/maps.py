from dotenv import load_dotenv
import googlemaps
import os

import googlemaps.places

ADDRESS = "1095 Military Trail, Scarborough, ON M1C 5J9"

load_dotenv('./.env')

gmaps = googlemaps.Client(os.environ.get("GCP"))

def getDonations():
    res = []

    loc = googlemaps.places.places(gmaps, "Clothes Donation", ADDRESS, radius=1500, type="donation")

    places = loc["results"][:5]

    for place in places:

        res.append({
            "name": place["name"],
            "address": place["formatted_address"]
        })

    return res

def getThrift():

    res = []

    loc = googlemaps.places.places(gmaps, "Thrift Store", ADDRESS, radius=1500, type="store")

    places = loc["results"][:5]

    for place in places:

        res.append({
            "name": place["name"],
            "address": place["formatted_address"]
        })

    return res

if __name__ == "__main__":
    print(getDonations())
    print(getThrift())
