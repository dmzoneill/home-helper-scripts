import os
from os import listdir
from os.path import isfile, isdir, join
from pprint import pprint
import shutil
import requests
import re


def get_torrent_listing(name):
    jacket_key = os.getenv("JACKETT_KEY")
    url = (
        "http://127.0.0.1:9117/api/v2.0/indexers/all/results?apikey="
        + jacket_key
        + "&Query="
        + name
        + "&Category%5B%5D=2000&Category%5B%5D=2040&Category%5B%5D=2045&Tracker%5B%5D=iptorrents&Tracker%5B%5D=privatehd&_=1630824295288"
    )
    response = requests.get(url)
    return response.json()


def get_torrent(name):
    result = get_torrent_listing(name)
    if "Results" not in result:
        return None

    if len(result["Results"]) == 0:
        return None

    list = sorted(result["Results"], key=lambda x: x["Seeders"])
    return [list[-1]["Link"], list[-1]["Title"]]


def download_file(name, url):
    local_filename = "/tmp/" + name + ".torrent"
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                # if chunk:
                f.write(chunk)
    shutil.move(local_filename, "/downloads/" + name + ".torrent")
    return "/downloads/" + name + ".torrent"


def download_torrrent(name):
    torrent = get_torrent(name)
    if torrent is None:
        return

    try:
        torrent_file = download_file(torrent[1], torrent[0])
        print(torrent_file)
        return True
    except Exception as e:
        return False


def get_movie(path):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    onlydirs = [f for f in listdir(path) if isdir(join(path, f))]
    onlyvideo = [
        f
        for f in onlyfiles
        if f[-3:] not in ["png", "srt", "url", "nfo", "jpg", "den", "m4v", "sub", "idx"]
    ]
    dontwant = [f for f in onlyfiles if f[-3:] in ["url"]]
    onlyunwanted = [f for f in onlyvideo if f[-3:] in ["avi", "mp4"]]
    skip = True

    # no video files
    if len(onlyvideo) == 0:
        # empty folder
        if len(onlydirs) == 0:
            shutil.rmtree(path)
        # probably cd folders, search for new torrent
        else:
            parts = path.split("/")
            if download_torrrent(parts[-1]):
                shutil.rmtree(path)

    # check wanted video file
    if len(onlyunwanted) == 1 and skip is False:
        if (
            int(os.stat(path + "/" + onlyvideo[0]).st_size) > 733933568
            and int(os.stat(path + "/" + onlyvideo[0]).st_size) < 1503933568
        ):
            print(onlyunwanted[0])
            print(os.stat(path + "/" + onlyvideo[0]).st_size)
            download_torrrent(onlyvideo[0])

    # duplicates
    if len(onlyvideo) > 1:
        pprint(onlyvideo)

    # subfolders
    if len(onlydirs) > 0:
        pprint(onlydirs)
        for X in onlydirs:
            if X == "extrafanart":
                print("Delete: " + path + "/" + X)
                shutil.rmtree(path + "/" + X)
            if X == ".xattr":
                print("Delete: " + path + "/" + X)
                shutil.rmtree(path + "/" + X)
            if re.search("cd[1-2]", X, re.IGNORECASE):
                y = path.split("/")
                print("Download: " + y[-1])
                if download_torrrent(y[-1]):
                    shutil.rmtree(path + "/" + X)

    # dontwant
    if len(dontwant) > 0:
        for X in dontwant:
            print("Delete: " + path + "/" + X)
            os.unlink(path + "/" + X)


def iterate_movies():
    directory = r"/films"
    for entry in os.listdir(directory):
        if os.path.isdir(directory + "/" + entry):
            get_movie(directory + "/" + entry)


iterate_movies()
