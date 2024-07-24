from pytube import YouTube
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import urllib.request
import re
import os

# PyTube and Spotipy required to run. To install, run: 'pip install pytube spotipy

#Authentication - without user
client_credentials_manager = SpotifyClientCredentials(client_id='84fcd57e42d24ea7b33713c00fb384b1', client_secret='20ea528369ef4452aaffa4f41ee13945')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def on_complete(stream, filepath):
    print("Download Complete!")

def main():
    try:
        playlist_link = input("Enter the link to the Spotify playlist to convert: ")
        save_location = input("Enter the path to the location where you would like to save your new playlist: ")

        playlist_URI = playlist_link.split("/")[-1].split("?")[0]
        track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]

        playlist_name = sp.playlist(playlist_URI)["name"]

        for track in sp.playlist_tracks(playlist_URI)["items"]:
            track_name = track["track"]["name"].replace(" ", "+")
            artist_name = track["track"]["artists"][0]["name"].replace(" ", "+")

            # Get youtube url based on name and artist
            search_query = u"https://www.youtube.com/results?search_query=" + track_name + "+" + artist_name + "+lyrics"

            results = urllib.request.urlopen(search_query.encode('ascii', 'ignore').decode("ascii"))


            youtube_url = "https://www.youtube.com/watch?v=" + re.findall(r"watch\?v=(\S{11})", results.read().decode())[0]

            video_object = YouTube(youtube_url, on_complete_callback=on_complete)

            # Video Information
            print(video_object.title)
            print(f'{video_object.length / 60} minutes')

            # Download
            download_folder = save_location + "/" + playlist_name
            try:
                out_file = video_object.streams.get_audio_only().download(download_folder)
            except:
                pass

            try:
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)
            except:
                print("That song is already downloaded in the directory!")
    except:
        print("Unexpected error")
        return

main()