import spotipy
from spotipy.oauth2 import SpotifyOAuth
import subprocess
import time

# ========== ENTER YOUR CREDENTIALS ==========
CLIENT_ID = "2c0c1f5d02e54fc3868352ae0f212bd4"
CLIENT_SECRET = "ca300f593ebc46dba99a4ae814de241d"
REDIRECT_URI = "http://localhost:8888/callback"

# ============================================

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-modify-playback-state user-read-playback-state"
))

def play_song(song_name):
    try:
        # 1️⃣ Open Spotify Desktop App (Mac)
        subprocess.run(["open", "-a", "Spotify"])
        
        # 2️⃣ Wait for app to fully load
        time.sleep(3)

        # 3️⃣ Search for song
        results = sp.search(q=song_name, type="track", limit=1)

        if not results["tracks"]["items"]:
            return "Song not found"

        track = results["tracks"]["items"][0]
        track_uri = track["uri"]

        # 4️⃣ Get active device
        devices = sp.devices()

        if not devices["devices"]:
            return "No active Spotify device found"

        device_id = devices["devices"][0]["id"]

        # 5️⃣ Start playback
        sp.start_playback(device_id=device_id, uris=[track_uri])

        return f"Playing {track['name']}"

    except Exception as e:
        return f"Error: {e}"