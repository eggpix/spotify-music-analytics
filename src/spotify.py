
"""
Handles Spotify authentication and API requests.
"""

import os

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth


def connect():
    """Authenticate and return a Spotify client."""

    load_dotenv()

    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope=(
            "user-library-read "
            "user-read-recently-played "
            "user-top-read"
        ),
        cache_path=".cache"
    ))


def get_all_pages(sp, results):
    """Retrieve all pages of a paginated Spotify response."""

    items = []

    while results:
        items.extend(results["items"])

        results = (
            sp.next(results)
            if results.get("next")
            else None
        )

    return items


def get_liked_tracks(sp):
    """Retrieve all saved tracks."""

    results = sp.current_user_saved_tracks(limit=50)

    return get_all_pages(sp, results)


def get_recently_played(sp, after=None):
    """
    Retrieve recently played tracks.

    Args:
        after: Optional Unix timestamp in milliseconds.
    """

    results = sp.current_user_recently_played(
        limit=50,
        after=after
    )

    return get_all_pages(sp, results)


def get_top_tracks(sp, time_range):
    """Retrieve the user's top tracks."""

    results = sp.current_user_top_tracks(
        limit=50,
        time_range=time_range
    )

    return results["items"]


def get_top_artists(sp, time_range):
    """Retrieve the user's top artists."""

    results = sp.current_user_top_artists(
        limit=50,
        time_range=time_range
    )

    return results["items"]


def valid_track(track):
    """Check whether a Spotify track has the information we need."""

    return (
        track
        and track.get("id")
        and track.get("album")
        and track["album"].get("id")
    )
