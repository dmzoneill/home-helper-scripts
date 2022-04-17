import os
import requests
import shutil

gio = True

api_key=os.environ.get('LIDARR_KEY')
root = "/music"
path = os.path.abspath(__file__) + "/.."

def set_folder_artist_art(artist_name):   
    gio_cmd = "gio set -t unset \"" + root + "/" + artist_name + "\" metadata::custom-icon"
    if os.path.exists(root + "/" + artist_name + "/folder.jpg"):
        gio_cmd = "gio set \"" + root + "/" + artist_name + "\" metadata::custom-icon \"file://" + root + "/" + artist_name + "/folder.jpg\""
    os.system(gio_cmd)     
    print(gio_cmd)

def set_folder_artist_album_art(artist_name, album):   
    gio_cmd = "gio set -t unset \"" + root + "/" + artist_name + "/" + album + "\" metadata::custom-icon"
    if os.path.exists(root + "/" + artist_name + "/" + album + "/folder.jpg"):
        gio_cmd = "gio set \"" + root + "/" + artist_name + "/" + album + "\" metadata::custom-icon \"file://" + root + "/" + artist_name  + "/" + album + "/folder.jpg\""
    os.system(gio_cmd)     
    print(gio_cmd)


def update_album_artwork(artist, album):
    print(album['title'])
    try:
        shutil.copyfile(path + "/lidarr/MediaCover/Albums/" + str(album['id']) + "/cover.jpg", artist['path'] + "/" + album['title'] + " (" + album['releaseDate'][0:4] + ")/folder.jpg")       
        set_folder_artist_album_art(os.fsdecode(artist['artistName']), os.fsdecode(album['title'] + " (" + album['releaseDate'][0:4] + ")"))    
    except Exception as e:
        pass


def update_artist_artwork(artist):
    print(artist['artistName'])
    try:
        shutil.copyfile(path + "/lidarr/MediaCover/" + str(artist['id']) + "/poster.jpg", artist['path'] + "/folder.jpg")  
        set_folder_artist_art(os.fsdecode(artist['artistName']))     
    except Exception as e:
        pass


def iterate_albums(artist):
    response = requests.get("http://127.0.0.1:8686/api/v1/album?artistid=" + str(artist['id']), headers={"X-Api-Key":api_key})
    if response.status_code == 200:
        json = response.json()
        for album in json:
            update_album_artwork(artist, album)


def iterate_artists():
    response = requests.get("http://127.0.0.1:8686/api/v1/artist", headers={"X-Api-Key":api_key})
    if response.status_code == 200:
        json = response.json()
        for artist in json:
            update_artist_artwork(artist)            
            iterate_albums(artist)


if __name__ == "__main__":
    iterate_artists()
