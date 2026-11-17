# Spotify Music Analytics

Get detailed analytics on Spotify listening history, top tracks and artists, and liked songs. Store the result in a PostgreSQL database.

## Creating a Spotify App

Before you begin, you must create a Spotify developer app. **You must have Spotify Premium to do this.** Go to [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard), log in and select "Create App". Set the redirect URI to `http://127.0.0.1:8888/callback`. Select "Web API" as the API type.

Once your app is created, copy the client ID, client secret, and redirect URI into a new .env file. **Do not share these values with anyone. Your .env should remain in .gitignore if you are forking this project.** Your .env file should look like this:

```bash
SPOTIPY_CLIENT_ID="your_client_id_here"
SPOTIPY_CLIENT_SECRET="your_client_secret_here"
SPOTIPY_REDIRECT_URI="http://127.0.0.1:8888/callback"
```

## Python Imports

Before using this project, you must install the following Python modules:

- spotipy
- python-dotenv
- psycopg

To install, run the following command in your Python terminal:

```
pip install spotipy python-dotenv psycopg
```

## Setting up the Database

Using PostgreSQL, set up a database called "spotify_music_analytics" using the [Schema SQL file](sql/schema.sql) to initialize tables. Information on the database design can be found in [database_design.md](docs/database_design.md). Once the database is set up, you can run [main.py](src/main.py) and fill the tables with data.

## Getting the Data

Run one of the [example queries](docs/example_queries.md) in a client tool like pgAdmin to get information from your database.