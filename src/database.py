
"""
Handles all PostgreSQL database connections and operations.
"""

import os
from getpass import getpass

import psycopg
from dotenv import load_dotenv


DATABASE_NAME = "spotify_music_analytics"


def connect():
    """Connect to PostgreSQL, locally or through a connection URL."""

    load_dotenv()

    database_url = os.getenv("DATABASE_URL")

    if database_url:
        return psycopg.connect(database_url)

    # Default to a locally hosted PostgreSQL server.
    params = {
        "host": os.getenv("PGHOST", "localhost"),
        "port": os.getenv("PGPORT", "5432"),
        "dbname": os.getenv("PGDATABASE", DATABASE_NAME),
        "user": os.getenv("PGUSER", "postgres"),
    }

    password = os.getenv("PGPASSWORD")

    if password:
        params["password"] = password

    return psycopg.connect(**params)


class Database:
    """Provides methods for interacting with the database."""

    def __init__(self):
        self.conn = connect()

    def close(self):
        self.conn.close()

    def insert_artist(self, artist):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO artists (id, name)
                VALUES (%s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (artist["id"], artist["name"]))

    def insert_track(self, track):
        album = track["album"]

        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO albums (id, name, type)
                VALUES (%s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (
                album["id"],
                album["name"],
                album["album_type"]
            ))

        for i, artist in enumerate(album["artists"]):
            self.insert_artist(artist)

            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO album_artists
                        (album_id, artist_id, artist_role)
                    VALUES (%s, %s, %s)
                    ON CONFLICT DO NOTHING
                """, (
                    album["id"],
                    artist["id"],
                    "Primary" if i == 0 else "Featured"
                ))

        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO tracks
                    (id, name, duration_ms, album_id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (
                track["id"],
                track["name"],
                track["duration_ms"],
                album["id"]
            ))

        for i, artist in enumerate(track["artists"]):
            self.insert_artist(artist)

            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO track_artists
                        (track_id, artist_id, artist_role)
                    VALUES (%s, %s, %s)
                    ON CONFLICT DO NOTHING
                """, (
                    track["id"],
                    artist["id"],
                    "Primary" if i == 0 else "Featured"
                ))

    def insert_liked_track(self, track_id, liked_at):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO liked_tracks (track_id, liked_at)
                VALUES (%s, %s)
                ON CONFLICT (track_id) DO NOTHING
            """, (track_id, liked_at))

            return cur.rowcount

    def get_latest_played_at(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT MAX(played_at)
                FROM recently_played
            """)

            return cur.fetchone()[0]

    def insert_recently_played(self, track_id, played_at):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO recently_played (track_id, played_at)
                VALUES (%s, %s)
                ON CONFLICT (track_id, played_at) DO NOTHING
            """, (track_id, played_at))

            return cur.rowcount

    def insert_top_track(self, track_id, time_range, retrieved_at, rank):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO top_tracks
                    (track_id, time_range, retrieved_at, rank)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (track_id, time_range, retrieved_at, rank))

    def insert_top_artist(self, artist_id, time_range, retrieved_at, rank):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO top_artists
                    (artist_id, time_range, retrieved_at, rank)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (artist_id, time_range, retrieved_at, rank))

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()
