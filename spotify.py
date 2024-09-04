import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

import os


# Set up your credentials
load_dotenv()
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'
SCOPE = 'playlist-modify-public'

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=SCOPE
))


def find_song(title, artist):
    # Search for the song
    query = f"track:\"{title}\" artist:\"{artist}\""
    results = sp.search(q=query, type='track', limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        return results['tracks']['items'][0]
    else:
        print(f"Track '{title}' by {artist} not found.")
        return None


def test():
    # Search for the song "Chemie Chemie Ya"
    results = sp.search(q='Chemie Chemie Ya', type='track', limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        track_uri = track['uri']
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        print(f"Found track: {track_name} by {artist_name}")

        # Create a new playlist
        user_id = sp.current_user()['id']
        playlist_name = 'New Playlist with Chemie Chemie Ya'
        playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
        playlist_id = playlist['id']

        # Add the track to the playlist
        sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist_id, tracks=[track_uri])
        print(f"Added {track_name} to the playlist '{playlist_name}'")
    else:
        print("Track not found.")


def add_to_playlist(playlist_name, tracks):
    max_tracks = 50

    user_id = sp.current_user()['id']
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
    playlist_id = playlist['id']

    sp.playlist_add_items(playlist_id, tracks)
    # Split the tracks into chunks of MAX_TRACKS
    for i in range(0, len(tracks), max_tracks):
        batch = tracks[i:i + max_tracks]
        try:
            sp.playlist_add_items(playlist_id, batch)
            print(f"Successfully added {len(batch)} tracks to the playlist.")
        except spotipy.exceptions.SpotifyException as e:
            print(f"Error adding tracks: {e}")
            # You may want to add additional error handling here


if __name__ == '__main__':
    find_song("Bee Gees - Stayin' Alive (Official Music Video)")

