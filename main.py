import json
import requests
from secrets import spotify_user_id, animeHits_id
from datetime import date
from refresh import Refresh


class SaveSongs:
    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = ""
        self.animeHits_id = animeHits_id
        self.tracks = ""
        self.new_playlist_id = ""

    def find_songs(self):

        print("Finding Songs in Anime Hits...")
        # Loop through playlist tracks, and track them to list

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            animeHits_id)

        response = requests.get(query,
                                headers={"content-type": "application/json",
                                         "Authorization": "Bearer {}".format(self.spotify_token)})

        response_json = response.json()

        print(response)

        for i in response_json["items"]:
            self.tracks += (i["track"]["uri"] + ",")
        self.tracks = self.tracks[:-1]

        self.add_to_playlist()

    def create_playlist(self):
        # Create a new playlist
        print("Trying to create a playlist...")
        today = date.today()
        todayFormatted = today.strftime("%d/%m/%Y")

        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            spotify_user_id)

        request_body = json.dumps({
            "name": todayFormatted + " Anime Hits",
            "description": "Relive your inner childhood with these awesome anime OSTs!",
            "public": True,
        })

        response = requests.post(query,
                                 data=request_body,
                                 headers={"content-type": "application/json",
                                          "Authorization": "Bearer {}".format(self.spotify_token)})

        response_json = response.json()

        return response_json["id"]

    def add_to_playlist(self):
        # Add all songs to new playlist
        print("Adding songs to playlist")

        self.new_playlist_id = self.create_playlist()

        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(
            self.new_playlist_id, self.tracks)

        response = requests.post(query,
                                 headers={"content-type": "application/json",
                                          "Authorization": "Bearer {}".format(self.spotify_token)})

        print(response.json)

    def call_refresh(self):

        print("Refreshing token")

        refreshCaller = Refresh()

        self.spotify_token = refreshCaller.refresh()

        self.find_songs()


a = SaveSongs()
a.call_refresh()
