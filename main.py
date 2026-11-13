import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")

print("Client ID loaded:", bool(client_id))
print("Client Secret loaded:", bool(client_secret))
print("Redirect URI loaded:", bool(redirect_uri))