# Spotify Music Analytics

Get detailed analytics on Spotify listening history, top tracks and artists, and liked songs.

## Creating a Spotify App

Before you begin, you must create a Spotify developer app. **You must have Spotify Premium to do this.** Go to [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard), log in and select "Create App". Set the redirect URI to `http://127.0.0.1:8888/callback`. Select "Web API" as the API type.

Once your app is created, copy the client ID, client secret, and redirect URI into a new .env file. **Do not share these values with anyone. Your .env should remain in .gitignore if you are forking this project.**

## Python Imports

Before using this project, you must install the following python modules:
- spotipy
- python-dotenv

## Setting up the Database

Using PostgreSQL, set up a database called "spotify_music" using the [Schema SQL file](sql/schema.sql). Information on the database design can be found in [database_design.md](docs/database_design.md). Once the database is set up, you can run [main.py](src/main.py) and fill the tables with data.