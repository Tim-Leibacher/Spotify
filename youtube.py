import logging
import os
import json

from dotenv import load_dotenv
from googleapiclient.discovery import build

# Hier den eigenen API-Schlüssel einfügen
load_dotenv()
API_KEY = os.getenv('YT_API_KEY')
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


# Funktion, um die Titel der Videos in einer Playlist abzurufen
def get_playlist_titles(playlist_id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

    titles = []
    request = youtube.playlistItems().list(
        part='snippet',
        playlistId=playlist_id,
        maxResults=50
    )

    while request is not None:
        response = request.execute()
        for item in response['items']:
            if item['snippet']['title'] in ['Private video', 'Deleted video']:
                logging.info(json.dumps(item))
                continue
            artist = item['snippet']['videoOwnerChannelTitle']
            if artist.lower().endswith(' - topic'):
                artist = artist[:-8]
            titles.append([(item['snippet']['title']), artist])

        # Weiterhin durch die Playlist blättern, wenn mehr als 50 Videos vorhanden sind
        request = youtube.playlistItems().list_next(request, response)

    return titles
