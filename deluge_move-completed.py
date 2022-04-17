#!/usr/bin/python
import os
import subprocess
import time

from deluge_client import DelugeRPCClient

client = DelugeRPCClient('127.0.0.1', 55555, 'deluge', os.environ.get('DELUGE_PASSWORD'))
client.connect()
torrents_list = client.core.get_torrents_status({},['name', 'download_location', 'label', 'progress', 'state', 'time_added'])

# filebot 
# -script fn:amc 
# --output /series 
# --action test 
# -non-strict "/mnt/downloads/midsomer.murders.s19e03.multi.1080p.hdtv.h264-sh0w.mkv" 
# --def "seriesFormat={n}/Season {s}/{n} - {s00}x{e00} - {t}"


def remove_series_torrent(id, download_location, name):
    filebot_cmd = [
        '/usr/bin/filebot',
        '-r',
        '-script',
        'fn:amc '
        '--output',
        '/series '   
        '--action',
        'copy', 
        '-non-strict',
        '"' + download_location + "/" + name + '"'
        ' --def',
        '"seriesFormat={n}/Season {s}/{n} - {s00}x{e00} - {t}"' 
    ]

    print(name)
    print(' '.join(filebot_cmd))
    result = subprocess.Popen(' '.join(filebot_cmd), stdout=subprocess.PIPE, shell=True).communicate()[0]
    print(result.decode("utf-8"))
    client.core.remove_torrent(id, True)
    print('=================================')

def remove_movies_torrent(id, download_location, name):
    filebot_cmd = [
        '/usr/bin/filebot',
        '-r',
        '-script',
        'fn:amc '
        '--output',
        '/films '   
        '--action',
        'copy', 
        '-non-strict',
        '"' + download_location + "/" + name + '"'
        ' --def',
        '"movieFormat=movies/{n} ({y})/{n} ({y})"' 
    ]

    print(name)
    print(' '.join(filebot_cmd))
    result = subprocess.Popen(' '.join(filebot_cmd), stdout=subprocess.PIPE, shell=True).communicate()[0]
    print(result.decode("utf-8"))
    client.core.remove_torrent(id, True)
    print('=================================')

def iterate_torrents():
    two_weeks = 1296000 # + 1 day
    for id, data in torrents_list.items():
        name = ""
        download_location = ""
        label = ""
        progress = ""
        state = ""
        time_added = 0

        for key, val in data.items():
            if key.decode() == "name":
                name = val.decode("utf-8")                 
            if key.decode() == "download_location":
                download_location = val.decode("utf-8")
            if key.decode() == "label":
                label = val.decode("utf-8")
            if key.decode() == "progress":
                progress = str(val)  
            if key.decode() == "state":
                state = val.decode("utf-8")
            if key.decode() == "time_added":
                time_added = int(val)

        if time_added == 0:
            print("eh?")
            return

        check_time = time_added + two_weeks 
        current_time = int(time.time())

        if progress == "100.0" and label == "tv-sonarr" and state == "Paused":
            #remove_series_torrent(id, download_location, name)
            print("")
        elif progress == "100.0" and label == "tv-sonarr" and check_time < current_time:
            print("Check time: " + str(check_time))
            #remove_series_torrent(id, download_location, name)
        elif progress == "100.0" and label == "radarr" and state == "Paused":
            remove_movies_torrent(id, download_location, name)
        elif progress == "100.0" and label == "radarr" and check_time < current_time:
            print("Check time: " + str(check_time))
            remove_movies_torrent(id, download_location, name)
        else:
            print("Ignored: " + name)

if __name__ == "__main__":
   iterate_torrents()


