import base64
from datetime import datetime
import string
import secrets
import os
from dotenv import load_dotenv


load_dotenv()


class Spotify:
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    redirect_uri = os.getenv('REDIRECT_URI')

    client_creds = f"{client_id}:{client_secret}"
    client_creds_b64 = base64.b64encode(client_creds.encode()).decode()

    scope = " ".join(["playlist-modify-public", "playlist-modify-private",
                      "ugc-image-upload", "user-read-recently-played", "user-read-private", "user-read-email",])
    auth_base_url = "https://accounts.spotify.com/authorize"
    token_url = "https://accounts.spotify.com/api/token"

    def get_user_endpoint():
        return "https://api.spotify.com/v1/me"

    def create_playlist_endpoint(user_id):
        return f"https://api.spotify.com/v1/users/{user_id}/playlists"

    def get_recently_played_endpoint():
        return "https://api.spotify.com/v1/me/player/recently-played"

    def add_to_playlist_endpoint(playlist_id):
        return f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

    def to_unix(played_at):
        """converts played_at field given by Spotify API to unix timestamp in ms

        Args:
            played_at (str): played_at field given by Spotify API

        Returns:
            int: unix timestamp in ms
        """

        try:
            time = int(datetime.strptime(
                played_at, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp())
        except:
            time = int(datetime.strptime(
                played_at, "%Y-%m-%dT%H:%M:%SZ").timestamp())

        return time

    def unix_to_month(unix):
        """converts unix timestamp to month in format MM-YYYY

        Args:
            unix (int): unix timestamp

        Returns:
            str: MM-YYYY
        """
        return datetime.fromtimestamp(unix).strftime("%m-%Y")

    def build_state():
        state = ''.join(
            secrets.choice(string.ascii_uppercase + string.digits) for _ in range(16)
        )

        return state
