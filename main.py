from gettext import find

from spotify import find_song, add_to_playlist
from youtube import get_playlist_titles
from dotenv import load_dotenv
import logging
import re
import json


def old_way():
    playlist_id = 'PLyq3jUL3Z6wOh5XFjl0MCRjj-VYJpNe0v'
    get_playlist_titles(playlist_id)

    tracks = get_playlist_titles(playlist_id)

    # Ausgabe der Titel
    for track in tracks:
        track[1] = track[1].lower().replace("vevo", "")
        pattern = rf"\s*(-\s*|{re.escape(track[1])}|\[official video\]|\(official video\)|\(official music video\)|\(audio\)|\(official lyric video\))"
        track[0] = re.sub(pattern, "", track[0].lower()).strip()
        song = find_song(track[0], track[1])
        if song is None:
            logging.error(f"Spotify not found: {track}")
            continue
        elif track[0].lower() == song['name'].lower() and track[1].lower() == song['artists'][0]['name'].lower():
            continue
        print(f"Youtube: {track} - Spotify: {song['name']} by {song['artists'][0]['name']}")
        user_input = input("y correct n add to log: ")
        if user_input == 'n':
            logging.warning(f"Not the Right YT: {track} SP: {song['name']} by {song['artists'][0]['name']}")

    add_to_playlist("newPlaylist", tracks)


def setup():
    load_dotenv()

    logging.basicConfig(
        filename='app.log',  # Log file name
        level=logging.INFO,  # Minimum log level to handle
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'  # Log message format
    )


def create_json_from_youtube(playlist_id):
    output_file = "tracks_info.json"
    tracks = get_playlist_titles(playlist_id)
    track_info_list = [{"title": track[0], "artist": track[1]} for track in tracks]

    with open(output_file, 'w') as json_file:
        json.dump(track_info_list, json_file, indent=4)


def load_playlist_from_json(filename):
    spotify_tracks = []
    with open(filename) as json_file:
        data = json.load(json_file)

    for track in data:
        song = find_song(track["title"], track["artist"])
        if song:
            uri = song.get("uri")
            if uri:
                spotify_tracks.append(uri)

    add_to_playlist("Youtube2", spotify_tracks)


if __name__ == '__main__':
    setup()

    #old_way()
    #create_json_from_youtube('PLyq3jUL3Z6wOh5XFjl0MCRjj-VYJpNe0v')
    load_playlist_from_json("tracks_info_edited.json")
