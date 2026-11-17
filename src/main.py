
"""
Main application entry point.

Usage:
    python main.py          Update recently played tracks.
    python main.py --full   Perform a complete initial import.
"""

import argparse

from datetime import datetime, timezone

from dotenv import load_dotenv

import database
import spotify


def import_liked_tracks(sp, db):
    """Import all liked tracks."""

    results = spotify.get_liked_tracks(sp)
    total = 0

    for item in results:
        track = item["track"]

        if not spotify.valid_track(track):
            continue

        db.insert_track(track)
        total += db.insert_liked_track(
            track["id"],
            item["added_at"]
        )

    print(f"Imported {total} liked tracks.")


def import_top_tracks_and_artists(sp, db):
    """Import top tracks and artists across all time ranges."""

    snapshot_at = datetime.now(timezone.utc)

    for time_range in ("short_term", "medium_term", "long_term"):

        tracks = spotify.get_top_tracks(sp, time_range)

        for rank, track in enumerate(tracks, start=1):
            if not spotify.valid_track(track):
                continue

            db.insert_track(track)

            db.insert_top_track(
                track["id"],
                time_range,
                snapshot_at,
                rank
            )

        artists = spotify.get_top_artists(sp, time_range)

        for rank, artist in enumerate(artists, start=1):
            if not artist.get("id"):
                continue

            db.insert_artist(artist)

            db.insert_top_artist(
                artist["id"],
                time_range,
                snapshot_at,
                rank
            )

    print("Successfully imported top tracks and artists.")


def update_recently_played(sp, db):
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

    total = 0

    for item in results:
        track = item["track"]

        if not spotify.valid_track(track):
            continue

        db.insert_track(track)

        total += db.insert_recently_played(
            track["id"],
            item["played_at"]
        )

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

    args = parser.parse_args()

    db = None

    try:
        sp = spotify.connect()
        db = database.Database()

        if args.full:
            import_liked_tracks(sp, db)
            import_top_tracks_and_artists(sp, db)

        update_recently_played(sp, db)

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
