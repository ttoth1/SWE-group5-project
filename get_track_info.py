import requests
import os
import json

def get_track_info(track_id):
    """This takes in a track_id and returns relevant information."""
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")

    AUTH_URL = "https://accounts.spotify.com/api/token"
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    #Convert response to JSON
    auth_response_data = auth_response.json()
    print(auth_response_data)

    #Save the access token
    access_token = auth_response_data['access_token']

    #Need to pass access token into header to send properly formed GET request to API server
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }

    BASE_URL = f"https://api.spotify.com/v1/tracks/{track_id}"
    
    print(f'track id is: {track_id}')
    print(f'BASE_URL is: {BASE_URL}\n')

    response = requests.get(
        BASE_URL,
        headers=headers,
    )
    r = response.json()
    # print(r)
    # print(json.dumps(r, indent=4))
    artist = r["album"]["artists"][0]["name"]
    print(f'artist name: {artist}')

    return "Hello from get_track_info()"



# def get_track_info(track_id):
#     response = requests.get(
#         f"https://api.spotify.com/v1/tracks/{track_id}",
#         params={
#             "market": "ES",
#             "token": os.getenv("CLIENT_ID"),
#         },
#     )
#     json_response = response.json()
#     print(json_response)

    # title = json_response["title"]
    # tagline = json_response["tagline"]
    # genres = ", ".join(genre["name"] for genre in json_response["genres"])
    # poster_path = json_response["poster_path"]
    # poster_image = f"{IMAGE_BASE_URL}/{POSTER_SIZE}{poster_path}"
    # return (title, tagline, genres, poster_image)