#!/usr/bin/env python3
import subprocess
from difflib import SequenceMatcher
from youtubesearchpython import VideosSearch
from pprint import pprint
import requests
import urllib.parse
import os
import sys

endpoint = "http://127.0.0.1:8686"
api_key = "771de60596e946f6b3e5e6f5fb6fd729"


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def rescan(path):
    data = {"name": "RescanFolders", "folders": [path]}
    response = requests.post(
        endpoint + "/api/v1/command", json=data, headers={"X-Api-Key": api_key}
    )
    pprint(response)
    pprint(response.content)


def import_track(match):
    pprint(match)
    response = requests.put(
        endpoint + "/api/v1/manualimport?", headers={"X-Api-Key": api_key}, json=[match]
    )
    pprint(response.content)
    pprint(response.status_code)
    if response.status_code == 202:
        result = response.json()
        albumReleaseId = result[0]["albumReleaseId"]
        trackId = result[0]["tracks"][0]["id"]

        data = {
            "name": "ManualImport",
            "files": [
                {
                    "path": match["path"],
                    "artistId": match["artist"]["id"],
                    "albumId": match["album"]["releases"][0]["albumId"],
                    "albumReleaseId": albumReleaseId,
                    "trackIds": [trackId],
                    "quality": {
                        "quality": {"id": 0, "name": "Unknown"},
                        "revision": {"version": 1, "real": 0, "isRepack": "false"},
                    },
                    "disableReleaseSwitching": "false",
                }
            ],
            "importMode": "auto",
            "replaceExistingFiles": "false",
        }

        confirm = requests.get(
            endpoint + "/api/v1/command", headers={"X-Api-Key": api_key}, data=data
        )
        if confirm.status_code == 200:
            pprint(confirm.json())

    sys.exit()


def get_album(artistId, albumName):
    response = requests.get(
        endpoint + "/api/v1/album?artistId=" + str(artistId),
        headers={"X-Api-Key": api_key},
    )
    if response.status_code == 200:
        albums = response.json()
        for album in albums:
            if album["title"] == albumName:
                return album
    return None


def scan_folder_for_songs(artistId, artistPath, filePath, albumName):
    query = "artistId=" + str(artistId) + "&"
    query += "folder=" + urllib.parse.quote(artistPath) + "&"
    query += "filterExistingFiles=true" + "&"
    query += "replaceExistingFiles=false"

    match = None

    response = requests.get(
        endpoint + "/api/v1/manualimport?" + query, headers={"X-Api-Key": api_key}
    )
    if response.status_code == 200:
        files = response.json()
        for file in files:
            if file["path"] == filePath:
                match = file
                break

    if match is not None:
        print("Matched")
        album = get_album(artistId, albumName)
        if album is not None:
            match["album"] = album
            import_track(match)
            print("Do import")

    print("End")
    sys.exit()


def get_song(artistID, artistName, albumName, title):
    best = 0
    bestLink = ""
    searchFor = artistName + " - " + title
    path = "/music/" + artistName + "/" + albumName
    filePath = path + "/" + artistName + " - " + albumName + " - " + title + ".mp3"

    if os.path.exists(filePath):
        return

    videosSearch = VideosSearch(searchFor)

    for song in videosSearch.result()["result"]:
        print(searchFor + " == " + song["title"])
        if similar(searchFor, song["title"]) > best:
            best = similar(searchFor, song["title"])
            bestLink = song["link"]

    print("Best: " + str(best))

    if best < 0.7:
        print("Unable to find " + searchFor)
        return

    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)

    downloader = 'youtube-dl --no-progress -x --audio-format mp3 "{link}" -o "{trackname}"'.format(
        link=bestLink, trackname=filePath.replace('"', '\\"')
    )
    print(downloader)

    proc = subprocess.Popen(downloader, shell=True, stdout=subprocess.PIPE)
    proc.wait()

    if proc.returncode == 0:
        print("Downloaded successfully")
        pprint(proc.stdout.read().decode("utf8"))
        rescan(path)

    # scan_folder_for_songs(artistID, "/music/" + artistName, filePath, albumName)


def import_lidarr_missing():
    response = requests.get(
        endpoint + "/api/v1/wanted/missing?page=0&pageSize=500",
        headers={"X-Api-Key": api_key},
    )
    if response.status_code == 200:
        json = response.json()

        for missing in json["records"]:
            resp = requests.get(
                endpoint
                + "/api/v1/track?artistid="
                + str(missing["artist"]["id"])
                + "&albumid="
                + str(missing["id"]),
                headers={"X-Api-Key": api_key},
            )
            if resp.status_code == 200:
                jsonb = resp.json()

                pprint(missing)
                print(missing["title"])
                print(missing["artist"]["path"])
                print(missing["artist"]["artistName"])

                for track in jsonb:
                    get_song(
                        missing["artist"]["id"],
                        missing["artist"]["artistName"],
                        missing["title"],
                        track["title"],
                    )


if __name__ == "__main__":
    import_lidarr_missing()
