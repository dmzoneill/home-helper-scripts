import os
import subprocess
import urllib.parse
from pprint import pprint

gio = True
films = "/smb/films/Entertainment/Films"
series = "/smb/series/Entertainment/Series"

def set_folder_art(direct, name):   
    gio_cmd = "gio set -t unset \"" + direct + "/" + name + "\" metadata::custom-icon"
    if os.path.exists(direct + "/" + name + "/folder.jpg"):
        gio_cmd = "gio set \"" + direct + "/" + name + "\" metadata::custom-icon \"file://" + direct + "/" + urllib.parse.quote(name) + "/folder.jpg\""
    os.system(gio_cmd)     
    print(gio_cmd)

def iterate(direct):
    directory = os.fsencode(direct)
    for name in os.listdir(directory):
        if os.path.isdir(direct + "/" + os.fsdecode(name)): 
            if gio is True:
            	set_folder_art(direct, os.fsdecode(name))

if __name__ == "__main__":
    iterate(films)
    iterate(series)
