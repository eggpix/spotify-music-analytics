# Spotify Music Analytics

Get detailed analytics on Spotify listening history, top tracks and artists, and liked songs.

## Python Imports

Before using this project, you must install the following python modules:
- spotipy
- python-dotenv

## Setting up the Database

Using PostgreSQL, set up a database called "spotify_music" using the [Schema SQL file](sql/schema.sql). Information on the database design can be found in [database_design.md](docs/database_design.md). Once the database is set up, you can run [main.py](src/main.py) and fill the tables with data.