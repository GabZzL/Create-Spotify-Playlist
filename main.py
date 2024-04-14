import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# parameters to use with Spotipy
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
REDIRECT_URL = os.environ["REDIRECT_URL"]
SCOPE = "playlist-modify-private"
# answer for the date, save the full date and year
date = input("What date do you want to travel(YYYY-MM-DD): ")
year = date[0:4]

# make a request to the billboard endpoint, and use BeautifulSoup to work with the data
response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{date}/")
billboard_html = response.text
soup = BeautifulSoup(billboard_html, "html.parser")
# look up for the song name
song_title_list = soup.select(selector="li ul li h3")
# save just the text name like a list
title_list = [song_title.getText().strip() for song_title in song_title_list]
# authentication in Spotipy
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URL,
                                               scope=SCOPE)
                     )
# get our user ID
current_user = sp.current_user()
user_id = current_user['id']
# crate a new list to save the URI format to each song
uri_list = []
# search for the song using the name and year, then append to a list
# if there is not found just pass
for song in title_list:
    try:
        result = sp.search(q=f"track:{song} year:{year}", type="track", limit=1)
    except:
        print(f"{song} was not found ")
        pass
    else:
        uri_list.append(result["tracks"]["items"][0]["uri"])
# create a new user playlist
play_list = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False,
                                    description=f"{date} Best Songs"
                                    )
# get the playlist id
play_list_id = play_list["id"]
# add the songs to the playlist using the uri list
sp.user_playlist_add_tracks(user=user_id, playlist_id=play_list_id, tracks=uri_list)

print("done")
