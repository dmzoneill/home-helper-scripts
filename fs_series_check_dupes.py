from os import listdir
from os.path import isfile, join
from pprint import pprint
import collections
import ffmpeg
import os

ignored = [
    'jpg',
    'hidden',
    'xattr',
    'nfo',
    'idx',
    'sub',
    'srt',
    'ts',
    'smi'
]

mypath = "/series"
total_dupes = 0
extensions = []

seriesdirs = sorted([f for f in listdir(mypath) if not isfile(join(mypath, f))])

def determine_delete(season_path, dupes, episodes):
    for dupe in dupes:
        dupelist = [f for f in episodes if dupe in f]
        widths = []
        heights = []   
        tempdupes = [] 
        try:    
            for item in dupelist:
                pos = item.rfind(".")
                extension = item[pos+1:len(item)]
                if extension in ignored:
                    continue

                # print(season_path + '/' + item)
                probe = ffmpeg.probe(season_path + '/' + item)
                video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
                width = int(video_stream['width'])
                height = int(video_stream['height'])
                widths.append(width)
                heights.append(height)
                tempdupes.append(item)

            max_height = max(heights)
            max_index = heights.index(max_height)
            accurrances = heights.count(max_height)

            pprint(tempdupes)
            #if accurrances > 1:
                #tempdupes.pop(max_index)

                #pprint(tempdupes)
                #for Y in tempdupes:
                #    print("rm -f \"" + season_path + "/" + Y + "\"")

                #e1 = dupelist[0].endswith('mkv')
                #e2 = dupelist[1].endswith('mkv')
                #if e1 or e2:
                #    if not e1:
                #        print("rm -f \"" + season_path + "/" + dupelist[0] + "\"")
                #    else:
                #        print("rm -f \"" + season_path + "/" + dupelist[1] + "\"")
                #else:
                #    print("not sure: " + dupelist[0] + " " + str(heights[0]) + "  " + str(heights[1]))
                #    print("not sure: " + dupelist[1] + " " + str(heights[1]) + "  " + str(heights[0]))
            #else:
            #    print("more than 1")
        except:
            pprint(tempdupes)

for series in seriesdirs:
    series_path = mypath + '/' + series
    # print(series_path)
    seasondirs = sorted([f for f in listdir(series_path) if not isfile(join(series_path, f))])

    for season in seasondirs:
        season_path = series_path + '/' + season
        # print(season_path)
        episodes = sorted([f for f in listdir(season_path) if isfile(join(season_path, f))])
    	
        cleaned = []
        for episode in episodes:
            pos = episode.rfind(".")    	     
            if pos != -1:
                extension = episode[pos+1:len(episode)]
                extensions.append(extension)
                if extension not in ignored:
                    title = episode[0:pos]
                    cleaned.append(title)
    	            # print(title)

        dupes = [item for item, count in collections.Counter(cleaned).items() if count > 1]

        if len(dupes) > 0:
            #print(season_path)
            #pprint(sorted(dupes))
            determine_delete(season_path, dupes, episodes)
            total_dupes += len(dupes)
    	    
print(total_dupes)
pprint(list(dict.fromkeys(extensions)))
