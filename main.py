from flask import Flask, url_for, redirect, request, session, render_template
from werkzeug.exceptions import HTTPException
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
from pprint import pprint
from bs4 import BeautifulSoup
import time
import requests
from datetime import datetime
from flask_bootstrap import Bootstrap

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

Bootstrap(app)

# authorize code flow - SpotifyOAuth object
sp_oauth = SpotifyOAuth(
    client_id=os.environ.get("SPOTIPY_CLIENT_ID"),
    client_secret=os.environ.get("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.environ.get("REDIRECT_URI"),
    scope="playlist-modify-private"
)


@app.route("/")
def login():
    # getting code & exchanging it for access token
    auth_url = sp_oauth.get_authorize_url()
    return "<a href='" + auth_url + "'>Login to Spotify</a>"


@app.route("/redirect")
def redirectPage():
    session.clear()
    code = request.args.get("code")
    token = sp_oauth.get_access_token(code)
    session["token_info"] = token
    return redirect(url_for("playlist"))


@app.route("/playlist", methods=["GET", "POST"])
def playlist():
    token = check_token()
    if not token:
        return redirect(url_for("login"))
    sp_web = spotipy.Spotify(auth=token["access_token"])
    is_billboard = request.args.get("billboard")
    if is_billboard:
        billBoard(sp_web)
    elif request.method == "POST":
        artist_name = request.form.get("artist_name")
        searchArtist(sp_web, artist_name)
    return render_template("playlist.html")


def check_token():
    token = session.get("token_info")
    diff_expiration = int(token["expires_at"]) - time.time()
    print(diff_expiration)
    if diff_expiration < 30:
        print("i am expired")
        token = sp_oauth.refresh_access_token(token["refresh_token"])
        print("I am refreshed token")
        return token
    else:
        return token


def billBoard(sp_web):
    url = "https://www.billboard.com/charts/hot-100/"
    response = requests.get(url)
    billboard = response.text
    soup = BeautifulSoup(billboard, "html.parser")
    song_names = [song.getText().strip() for song in soup.select("li #title-of-a-story")]
    artist_names = [artist.getText().strip("\n\t") for artist in
                    soup.select("ul li span.c-label.a-no-trucate.a-font-primary-s")]
    today = datetime.now().strftime("%Y/%m/%d")
    pairs = [(song_names[num], artist_names[num]) for num in range(len(song_names))]
    pairs_uri = []

    for pair in pairs:
        uri = sp_web.search(q=pair)["tracks"]["items"][0]["uri"][14:]
        if not uri:
            print("The song doesn't exist in Spotify")
            continue
        pairs_uri.append(uri)
    addSong(sp_web, playlist_id=createPlaylist(sp_web, playlist_name=f"Billboard {today}"), track_list=pairs_uri)
    print("Billboard playlist is done")


def searchArtist(sp_web, artist_name):
    artist_id = sp_web.search(q=artist_name, limit=5)["tracks"]["items"][0]["album"]["artists"][0]["id"]
    if not artist_id:
        print("This artist doesn't exist in Spotify")
    artist_top_tracks_info = sp_web.artist_top_tracks(artist_id=artist_id)["tracks"]
    # artist_top_tracks_name = [track["name"] for track in artist_top_tracks_info]
    artist_top_tracks_uri = [track["uri"] for track in artist_top_tracks_info]
    addSong(sp_web, playlist_id=createPlaylist(sp_web, artist_name), track_list=artist_top_tracks_uri)
    print("New artist playlist is done")


def createPlaylist(sp_web, playlist_name):
    # get token
    user_id = sp_web.current_user()["id"]
    # create playlist
    new_playlist = sp_web.user_playlist_create(user=user_id, name=playlist_name, public=False)
    return new_playlist["id"]


def addSong(sp_web, playlist_id, track_list):
    sp_web.playlist_add_items(playlist_id, items=track_list, position=None)
    print("Song added to New Playlist")

if __name__ == "__main__":
    app.run(debug=True)

