#!/usr/bin/env python3
import os
import glob

def startsWith(haystack, needle):
    length = len(needle)
    return haystack.lower()[:length] == needle.lower()

def endsWith(haystack, needle):
    length = len(needle)
    if not length:
        return True
    return haystack[-length:] == needle

def recursiveScan(dir):
    tree = glob.glob(dir.rstrip('/') + '/*')
    if isinstance(tree, list):
        for file in tree:
            if os.path.isdir(file):
                recursiveScan(file)
            elif os.path.isfile(file):
                if endsWith(file, "poster.jpg"): continue
                if endsWith(file, "folder.jpg"): continue
                if endsWith(file, "banner.jpg"): continue
                if endsWith(file, "fanart.jpg"): continue
                if endsWith(file, "logo.jpg"): continue
                if endsWith(file, "landscape.jpg"): continue
                if endsWith(file, "clearart.png"): continue
                if endsWith(file, "logo.png"): continue
                if endsWith(file, "tvshow.nfo"): continue

                parts = file.split("/")

                correct_series_name = startsWith(parts[-1], parts[-3])
                correct_series_name_nospaces = startsWith(parts[-1], parts[-3].replace(" ", ""))

                if not (correct_series_name or correct_series_name_nospaces):
                    print(file)
                else:
                    pass

def Scan(dir):
    tree = glob.glob(dir.rstrip('/') + '/*')
    if isinstance(tree, list):
        for file in tree:
            recursiveScan(file)

Scan("/series")
