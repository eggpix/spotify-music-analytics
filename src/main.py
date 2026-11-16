
import os
import psycopg2
import spotipy

from dotenv import load_dotenv
from getpass import getpass
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

# Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-library-read"
))

# PostgreSQL connection
conn = psycopg2.connect(
    host="localhost",
    database="spotify_music",
    user="postgres",
    password=getpass("PostgreSQL password: ")
)

cur = conn.cursor()

def insert_artist(artist):
    cur.execute("""
        INSERT INTO artists (id, name)
        VALUES (%s, %s)
        ON CONFLICT (id) DO NOTHING
    """, (artist["id"], artist["name"]))

# Retrieve saved tracks
results = sp.current_user_saved_tracks(limit=50)
total_tracks = 0

while results:
    for item in results["items"]:
        track = item["track"]
        if not track or not track["id"]:
            continue

        album = track["album"]

        # Insert album
        cur.execute("""
            INSERT INTO albums (id, name, type)
            VALUES (%s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (album["id"], album["name"], album["album_type"]))

        # Insert album artists and relationships
        for i, artist in enumerate(album["artists"]):
            insert_artist(artist)
            cur.execute("""
                INSERT INTO album_artists (album_id, artist_id, artist_role)
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (album["id"], artist["id"],
                  "Primary" if i == 0 else "Featured"))

        # Insert track
        cur.execute("""
            INSERT INTO tracks (id, name, duration_ms, album_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (track["id"], track["name"],
              track["duration_ms"], album["id"]))

        # Insert track artists and relationships
        for i, artist in enumerate(track["artists"]):
            insert_artist(artist)
            cur.execute("""
                INSERT INTO track_artists (track_id, artist_id, artist_role)
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (track["id"], artist["id"],
                  "Primary" if i == 0 else "Featured"))

        total_tracks += 1

    results = sp.next(results) if results["next"] else None

conn.commit()
cur.close()
conn.close()

print(f"Successfully processed {total_tracks} saved tracks!")
