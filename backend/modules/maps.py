from dotenv import load_dotenv
import googlemaps
import os

import googlemaps.places

ADDRESS = "1095 Military Trail, Scarborough, ON M1C 5J9"

load_dotenv('./.env')

gmaps = googlemaps.Client(os.environ.get("GCP"))

def getDonations(address: str):
    res = []

    loc = googlemaps.places.places(gmaps, "Clothes Donation", address, radius=1500, type="donation")

    places = loc["results"][:5]

    for place in places:

        res.append({
            "name": place["name"],
            "address": place["formatted_address"]
        })

    return res

def getThrift(address: str):

    res = []

    loc = googlemaps.places.places(gmaps, "Thrift Store", address, radius=1500, type="store")

    places = loc["results"][:5]

    for place in places:

        res.append({
            "name": place["name"],
            "address": place["formatted_address"]
        })

    return res

if __name__ == "__main__":
    print(getDonations(ADDRESS))
    print(getThrift(ADDRESS))
