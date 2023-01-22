#!/usr/bin/python3
import os
import pyprobe
from pprint import pprint
import signal
import sys
import json

report = {}
rootdir = "/smb/series/Entertainment/Series/"
count = 0


def signal_handler(sig, frame):
    pprint(report)
    sys.exit(0)


def read_video(file):
    global count
    count = count + 1
    parts = file.split("/")
    show = parts[5] if len(parts) > 4 else None
    season = parts[6] if len(parts) > 5 else None
    try:
        parser = pyprobe.VideoFileParser(
            ffprobe="/usr/bin/ffprobe", includeMissing=True, rawMode=False
        )
        data = parser.parseFfprobe(file)
        if show not in report:
            report[show] = {}
        if season not in report[show]:
            report[show][season] = []

        report[show][season].append(data)
        print(file)
        print(count)
    except:
        print("Error :" + file)


def main():
    for subdir, dirs, files in os.walk(rootdir):
        for filename in files:
            filepath = subdir + os.sep + filename
            if (
                filepath.endswith(".mkv")
                or filepath.endswith(".avi")
                or filepath.endswith(".mp4")
            ):
                read_video(filepath)

    json_object = json.dumps(report)
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()
