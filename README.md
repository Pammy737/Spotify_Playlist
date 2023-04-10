# Spotify Playlist

allows users to create Spotify Playlist with just one click

## Table of Contents

* [Demonstration](https://github.com/Pammy737/Spotify_Playlist#demonstration)
* [Techniques & Tools](https://github.com/Pammy737/Spotify_Playlist#techniques--tools)
* [How to use](https://github.com/Pammy737/Spotify_Playlist#how-to-use)
* [Upcoming Features](https://github.com/Pammy737/Spotify_Playlist#upcoming-features)
* [Notes](https://github.com/Pammy737/Spotify_Playlist#notes)

## Demonstration
* Log in Page
  ![log in](https://github.com/Pammy737/Spotify_Playlist/blob/main/images/1.png)
* OAuth Authorization
  ![Authorization](https://github.com/Pammy737/Spotify_Playlist/blob/main/images/2.png)
* Click Today's Billboard 100
   * Today's Billboard Hot 100 playlist created
* Enter the preferred artist name
   * Playlist of artist's Top 10 songs is created
   

## Techniques & Tools

* Environment
    * [poetry](https://python-poetry.org/docs/#installation) (1.4.1) (check [Notes]())
    * [python-dotenv](https://pypi.org/project/python-dotenv/) (1.0.0)
* Python (3.9)
    * [flask](https://flask.palletsprojects.com/en/2.2.x/) (2.2.3)
* API
    * [Spotipy](https://spotipy.readthedocs.io/en/2.22.1/) (2.23.0)
    * [OAuth 2.0 Authorization Flow](https://developer.spotify.com/documentation/web-api/tutorials/code-flow)
* Webscraping
    * [beautifulsoup4](https://pypi.org/project/beautifulsoup4/) (4.12.2)

## How to use

User may create a playlist of...

* current [Billboard Hot 100](https://www.billboard.com/charts/hot-100/) songs with one click
* top 10 songs of a preferred artist, just by entering his/her name and clicking submit

## Upcoming Features

## Notes
* if couldn't find Poetry after installing, for Mac users try ```export PATH="$HOME/.local/bin:$PATH”```
* if accidentally pushed files with sensitive information, try the solution [here](https://daily-dev-tips.com/posts/removing-a-env-file-from-git-history/)
  * in order to delete history, you might need [this](https://www.educative.io/answers/the-fatal-refusing-to-merge-unrelated-histories-git-error), and Mac users could take a look at [this](https://gist.github.com/kenandersen/2042103942473af82dd2)  
