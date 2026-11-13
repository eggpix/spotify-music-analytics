
import os
import spotipy

from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="user-library-read",
        open_browser=True
    )
)

print("Successfully authenticated with Spotify!")
