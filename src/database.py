"""
Handles all PostgreSQL database connections and operations.
"""

import os
from getpass import getpass
from itertools import islice

import psycopg
from psycopg import sql
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

    INSERT_BATCH_SIZE = 1000

    def __init__(self):
        self.conn = connect()

    def close(self):
        self.conn.close()

    def _insert_many(self, table, columns, rows):
        """Insert rows in bounded multi-row statements and return the inserted count."""

        inserted = 0
        columns_sql = sql.SQL(", ").join(
            sql.Identifier(column) for column in columns
        )
        row_placeholders = sql.SQL("({})").format(
            sql.SQL(", ").join(sql.Placeholder() for _ in columns)
        )

        rows = iter(rows)
        batch = list(islice(rows, self.INSERT_BATCH_SIZE))
        if not batch:
            return 0

        with self.conn.cursor() as cur:
            while batch:
                values_sql = sql.SQL(", ").join(
                    row_placeholders for _ in batch
                )
                query = sql.SQL("""
                    INSERT INTO {} ({})
                    VALUES {}
                    ON CONFLICT DO NOTHING
                """).format(
                    sql.Identifier(table),
                    columns_sql,
                    values_sql
                )
                cur.execute(query, [
                    value
                    for row in batch
                    for value in row
                ])
                inserted += cur.rowcount
                batch = list(islice(rows, self.INSERT_BATCH_SIZE))

        return inserted

    def insert_artists(self, artists):
        rows = {}
        for artist in artists:
            rows.setdefault(artist["id"], (artist["id"], artist["name"]))

        return self._insert_many("artists", ("id", "name"), rows.values())

    def insert_artist(self, artist):
        return self.insert_artists([artist])

    def insert_tracks(self, tracks):
        albums = {}
        artists = {}
        track_rows = {}
        album_artist_rows = {}
        track_artist_rows = {}

        for track in tracks:
            album = track["album"]
            album_id = album["id"]
            track_id = track["id"]

            albums.setdefault(
                album_id,
                (album_id, album["name"], album["album_type"])
            )
            track_rows.setdefault(track_id, (
                track_id,
                track["name"],
                track["duration_ms"],
                album_id
            ))

            for role_index, artist in enumerate(album["artists"]):
                artist_id = artist["id"]
                artists.setdefault(artist_id, (artist_id, artist["name"]))
                album_artist_rows.setdefault(
                    (album_id, artist_id),
                    (
                        album_id,
                        artist_id,
                        "Primary" if role_index == 0 else "Featured"
                    )
                )

            for role_index, artist in enumerate(track["artists"]):
                artist_id = artist["id"]
                artists.setdefault(artist_id, (artist_id, artist["name"]))
                track_artist_rows.setdefault(
                    (track_id, artist_id),
                    (
                        track_id,
                        artist_id,
                        "Primary" if role_index == 0 else "Featured"
                    )
                )

        self._insert_many("albums", ("id", "name", "type"), albums.values())
        self._insert_many("artists", ("id", "name"), artists.values())
        self._insert_many(
            "tracks",
            ("id", "name", "duration_ms", "album_id"),
            track_rows.values()
        )
        self._insert_many(
            "album_artists",
            ("album_id", "artist_id", "artist_role"),
            album_artist_rows.values()
        )
        self._insert_many(
            "track_artists",
            ("track_id", "artist_id", "artist_role"),
            track_artist_rows.values()
        )

    def insert_track(self, track):
        return self.insert_tracks([track])

    def insert_liked_tracks(self, rows):
        return self._insert_many(
            "liked_tracks",
            ("track_id", "liked_at"),
            rows
        )

    def insert_liked_track(self, track_id, liked_at):
        return self.insert_liked_tracks([(track_id, liked_at)])

    def get_latest_played_at(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT MAX(played_at)
                FROM recently_played
            """)

            return cur.fetchone()[0]

    def insert_recently_played(self, track_id, played_at):
        return self.insert_recently_played_many([(track_id, played_at)])

    def insert_recently_played_many(self, rows):
        return self._insert_many(
            "recently_played",
            ("track_id", "played_at"),
            rows
        )

    def insert_top_tracks(self, rows):
        return self._insert_many(
            "top_tracks",
            ("track_id", "time_range", "retrieved_at", "rank"),
            rows
        )

    def insert_top_track(self, track_id, time_range, retrieved_at, rank):
        return self.insert_top_tracks([
            (track_id, time_range, retrieved_at, rank)
        ])

    def insert_top_artists(self, rows):
        return self._insert_many(
            "top_artists",
            ("artist_id", "time_range", "retrieved_at", "rank"),
            rows
        )

    def insert_top_artist(self, artist_id, time_range, retrieved_at, rank):
        return self.insert_top_artists([
            (artist_id, time_range, retrieved_at, rank)
        ])

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()
