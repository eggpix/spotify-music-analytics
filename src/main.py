"""
Run this file to retrieve all relavent data from the Spotify API and load it in your database.
"""

import os
import psycopg
import spotipy

from dotenv import load_dotenv
from getpass import getpass
from datetime import datetime, timezone
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

DATABASE_NAME = "spotify_music_analytics"

# Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-library-read user-read-recently-played user-top-read"
))

# PostgreSQL connection
conn = psycopg.connect(
    host="localhost",
    database=DATABASE_NAME,
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


def insert_track(track):
    album = track["album"]

    cur.execute("""
        INSERT INTO albums (id, name, type)
        VALUES (%s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    """, (album["id"], album["name"], album["album_type"]))

    for i, artist in enumerate(album["artists"]):
        insert_artist(artist)
        cur.execute("""
            INSERT INTO album_artists (album_id, artist_id, artist_role)
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (album["id"], artist["id"],
              "Primary" if i == 0 else "Featured"))

    cur.execute("""
        INSERT INTO tracks (id, name, duration_ms, album_id)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    """, (track["id"], track["name"],
          track["duration_ms"], album["id"]))

    for i, artist in enumerate(track["artists"]):
        insert_artist(artist)
        cur.execute("""
            INSERT INTO track_artists (track_id, artist_id, artist_role)
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (track["id"], artist["id"],
              "Primary" if i == 0 else "Featured"))


# Retrieve liked songs
results = sp.current_user_saved_tracks(limit=50)
total_liked = 0

while results:
    for item in results["items"]:
        track = item["track"]
        if not track or not track["id"] or not track["album"]["id"]:
            continue

        insert_track(track)

        cur.execute("""
            INSERT INTO liked_tracks (track_id, liked_at)
            VALUES (%s, %s)
            ON CONFLICT (track_id) DO NOTHING
        """, (track["id"], item["added_at"]))

        total_liked += 1

    results = sp.next(results) if results["next"] else None


# Retrieve recently played tracks
results = sp.current_user_recently_played(limit=50)
total_played = 0

while results:
    for item in results["items"]:
        track = item["track"]
        if not track or not track["id"] or not track["album"]["id"]:
            continue

        insert_track(track)

        cur.execute("""
            INSERT INTO recently_played (track_id, played_at)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
        """, (track["id"], item["played_at"]))

        total_played += 1

    results = sp.next(results) if results["next"] else None


# Retrieve top tracks and artists
snapshot_at = datetime.now(timezone.utc)

for time_range in ("short_term", "medium_term", "long_term"):

    results = sp.current_user_top_tracks(
        limit=50, time_range=time_range
    )

    for rank, track in enumerate(results["items"], start=1):
        insert_track(track)

        cur.execute("""
            INSERT INTO top_tracks
                (track_id, time_range, retrieved_at, rank)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (track["id"], time_range, snapshot_at, rank))

    results = sp.current_user_top_artists(
        limit=50, time_range=time_range
    )

    for rank, artist in enumerate(results["items"], start=1):
        insert_artist(artist)

        cur.execute("""
            INSERT INTO top_artists
                (artist_id, time_range, retrieved_at, rank)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (artist["id"], time_range, snapshot_at, rank))


conn.commit()
cur.close()
conn.close()

print(f"Successfully processed {total_liked} liked tracks!")
print(f"Successfully processed {total_played} recently played tracks!")
print("Successfully retrieved top tracks and artists!")