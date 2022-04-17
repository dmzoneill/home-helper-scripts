#!/usr/bin/python
import os
from deluge_client import DelugeRPCClient
client = DelugeRPCClient('127.0.0.1', 55555, 'deluge', os.environ.get('DELUGE_PASSWORD'))
client.connect()
torrents_list = client.core.get_torrents_status({},[])

allowed_trackers = [
    'bgp.technology',
    'empirehost.me',
    'stackoverflow.tech'
]

for id, data in torrents_list.items():
    name = ""
    tracker = ""
    progress = 0
    for key, val in data.items():
        if key.decode() == "name":
            name = val.decode("utf-8") 
        if key.decode() == "tracker_host":
            tracker = val.decode("utf-8")
        if key.decode() == "progress":
            progress = str(val)
    if progress == "100.0" and tracker not in allowed_trackers:
        print(name)
        print(tracker)
        print(str(val))
        client.core.pause_torrent(id)
