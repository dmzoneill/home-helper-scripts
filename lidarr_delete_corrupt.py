#!/usr/bin/env python3
import subprocess
from difflib import SequenceMatcher
from wsgiref.simple_server import WSGIRequestHandler
from youtubesearchpython import VideosSearch
from pprint import pprint
import requests
import os
import eyed3
from os.path import exists

endpoint = "http://127.0.0.1:8686"
api_key = "771de60596e946f6b3e5e6f5fb6fd729"


def rescan(path):
    data = {"name": "RescanFolders", "folders": [path]}
    response = requests.post(
        endpoint + "/api/v1/command", json=data, headers={"X-Api-Key": api_key}
    )
    data = {"name": "DownloadedAlbumsScan", "path": path, "folders": [path]}
    response = requests.post(
        endpoint + "/api/v1/command", json=data, headers={"X-Api-Key": api_key}
    )


def get_file_source(file):
    response = requests.get(
        endpoint + "/logfile/" + file, headers={"X-Api-Key": api_key}
    )
    if response.status_code == 200:
        return response.content.decode("UTF-8").split("\n")
    return []


files = [
    "Lidarr.txt",
    "Lidarr0.txt",
    "Lidarr1.txt",
    "Lidarr2.txt",
    "Lidarr3.txt",
    "Lidarr4.txt",
    "Lidarr5.txt",
    "Lidarr6.txt",
    "Lidarr7.txt",
]

for file in files:
    for line in get_file_source(file):
        if "File is corrupt" in line:
            parts = line.split("Tag reading failed for ")
            rightpart = parts[1].split(".  File is")
            try:
                os.remove(rightpart[0])
                print(rightpart[0])
                pathParts = rightpart[0].split("/")
                pathParts.pop()
                path = "/".join(pathParts)
                print(path)
                rescan(rightpart[0])
            except:
                pass
