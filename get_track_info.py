import requests
import os
import json


def get_track_info(track_id):
    """This takes in a track_id and returns relevant information."""
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")

    AUTH_URL = "https://accounts.spotify.com/api/token"
    auth_response = requests.post(
        AUTH_URL,
        {
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
    )

    # Convert response to JSON
    auth_response_data = auth_response.json()

    # Save the access token
    access_token = auth_response_data["access_token"]

    # Need to pass access token into header to send properly formed GET request to API server
    headers = {"Authorization": "Bearer {token}".format(token=access_token)}

    BASE_URL = f"https://api.spotify.com/v1/tracks/{track_id}"

    response = requests.get(
        BASE_URL,
        headers=headers,
    )
    r = response.json()

    track_name = r["name"]
    track_link = r["external_urls"]["spotify"]
    artist = r["album"]["artists"][0]["name"]
    artist_link = r["album"]["artists"][0]["external_urls"]["spotify"]
    album = r["album"]["name"]
    album_link = r["album"]["external_urls"]["spotify"]
    album_pic = r["album"]["images"][1]["url"]
    return (track_name, track_link, artist, artist_link, album, album_link, album_pic)
