"""
Main application entry point.

Usage:
    python main.py            Runs full data import (identical to python main.py --full).
    python main.py --full     Perform a complete initial import.
    python main.py --liked    Insert liked songs data
    python main.py --top      Insert top artists and tracks
    python main.py --recent   Insert recent tracks
"""

import argparse

from datetime import datetime, timezone

from dotenv import load_dotenv

import database
import spotify


def import_liked_tracks(sp, db):
    """Import all liked tracks."""

    results = spotify.get_liked_tracks(sp)
    valid_items = [
        item for item in results
        if spotify.valid_track(item["track"])
    ]

    db.insert_tracks([item["track"] for item in valid_items])
    total = db.insert_liked_tracks([
        (item["track"]["id"], item["added_at"])
        for item in valid_items
    ])

    print(f"Imported {total} liked tracks.")


def import_top_tracks_and_artists(sp, db):
    """Import top tracks and artists across all time ranges."""

    snapshot_at = datetime.now(timezone.utc)

    for time_range in ("short_term", "medium_term", "long_term"):

        tracks = spotify.get_top_tracks(sp, time_range)
        valid_tracks = [
            (rank, track)
            for rank, track in enumerate(tracks, start=1)
            if spotify.valid_track(track)
        ]

        db.insert_tracks([track for _, track in valid_tracks])
        db.insert_top_tracks([
            (track["id"], time_range, snapshot_at, rank)
            for rank, track in valid_tracks
        ])

        artists = spotify.get_top_artists(sp, time_range)
        valid_artists = [
            (rank, artist)
            for rank, artist in enumerate(artists, start=1)
            if artist.get("id")
        ]

        db.insert_artists([artist for _, artist in valid_artists])
        db.insert_top_artists([
            (artist["id"], time_range, snapshot_at, rank)
            for rank, artist in valid_artists
        ])

    print("Successfully imported top tracks and artists.")


def import_recently_played(sp, db):
    """Import only recently played tracks not already in the database."""

    latest_played_at = db.get_latest_played_at()

    after = None

    if latest_played_at:
        # Include a small overlap to avoid missing boundary events.
        after = max(
            0,
            int(latest_played_at.timestamp() * 1000) - 5000
        )

    results = spotify.get_recently_played(sp, after=after)

    valid_items = [
        item for item in results
        if spotify.valid_track(item["track"])
    ]

    db.insert_tracks([item["track"] for item in valid_items])
    total = db.insert_recently_played_many([
        (item["track"]["id"], item["played_at"])
        for item in valid_items
    ])

    print(f"Imported {total} new listening events.")


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Spotify Music Analytics data importer."
    )

    parser.add_argument(
        "--full",
        action="store_true",
        help="Import liked tracks, top tracks, top artists, and recent plays."
    )
    parser.add_argument(
        "--liked",
        action="store_true",
        help="Import liked tracks for current user."
    )
    parser.add_argument(
        "--top",
        action="store_true",
        help="Import top tracks and top artists for current user."
    )
    parser.add_argument(
        "--recent",
        action="store_true",
        help="Import recent tracks for current user."
    )

    args = parser.parse_args()

    db = None

    try:
        print("Connecting to Spotify...", flush=True)
        sp = spotify.connect()

        print("Connecting to PostgreSQL...", flush=True)
        db = database.Database()

        print("Connections established!", flush=True)

        if args.liked or args.full:
            print("Retrieving liked tracks...", flush=True)
            import_liked_tracks(sp, db)

        if args.top or args.full:
            print("Retrieving top tracks and artists...", flush=True)
            import_top_tracks_and_artists(sp, db)

        if args.recent or args.full:
            print("Updating recently played...", flush=True)
            import_recently_played(sp, db)

        db.commit()
        print("Database update completed successfully!")

    except Exception:
        if db:
            db.rollback()
        raise

    finally:
        if db:
            db.close()


if __name__ == "__main__":
    main()
