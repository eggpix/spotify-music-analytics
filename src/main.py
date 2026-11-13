
import os
import psycopg2
import spotipy

from dotenv import load_dotenv
from getpass import getpass
from spotipy.oauth2 import SpotifyOAuth


# Load environment variables
load_dotenv()


# Authenticate with Spotify
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="user-library-read"
    )
)


# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="spotify_music",
    user="postgres",
    password=getpass("PostgreSQL password: ")
)

cur = conn.cursor()


# Retrieve all saved tracks
results = sp.current_user_saved_tracks(limit=50)

total_tracks = 0

while results:
    for item in results["items"]:
        track = item["track"]

        if not track:
            continue

        album = track["album"]

        # Insert album
        cur.execute("""
            INSERT INTO albums (album_id, album_name, album_type)
            VALUES (%s, %s, %s)
            ON CONFLICT (album_id) DO NOTHING
        """, (
            album["id"],
            album["name"],
            album["album_type"]
        ))

        # Insert album artists
        for index, artist in enumerate(album["artists"]):
            cur.execute("""
                INSERT INTO artists (artist_id, artist_name)
                VALUES (%s, %s)
                ON CONFLICT (artist_id) DO NOTHING
            """, (
                artist["id"],
                artist["name"]
            ))

            cur.execute("""
                INSERT INTO album_artists
                    (album_id, artist_id, artist_role)
                VALUES (%s, %s, %s)
                ON CONFLICT (album_id, artist_id) DO NOTHING
            """, (
                album["id"],
                artist["id"],
                "Primary" if index == 0 else "Featured"
            ))

        # Insert track
        cur.execute("""
            INSERT INTO tracks
                (track_id, track_name, track_duration, album_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (track_id) DO NOTHING
        """, (
            track["id"],
            track["name"],
            track["duration_ms"],
            album["id"]
        ))

        # Insert track artists
        for index, artist in enumerate(track["artists"]):
            cur.execute("""
                INSERT INTO artists (artist_id, artist_name)
                VALUES (%s, %s)
                ON CONFLICT (artist_id) DO NOTHING
            """, (
                artist["id"],
                artist["name"]
            ))

            cur.execute("""
                INSERT INTO track_artists
                    (track_id, artist_id, artist_role)
                VALUES (%s, %s, %s)
                ON CONFLICT (track_id, artist_id) DO NOTHING
            """, (
                track["id"],
                artist["id"],
                "Primary" if index == 0 else "Featured"
            ))

        total_tracks += 1

    # Retrieve the next page
    if results["next"]:
        results = sp.next(results)
    else:
        results = None

# Commit database changes
conn.commit()

# Close database connection
cur.close()
conn.close()

print(f"Successfully processed {total_tracks} saved tracks!")
