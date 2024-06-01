#!/usr/bin/env python

import os
import re

path = '/series/'
real_path = os.path.realpath(path)
path_split_count = len(path.split("/"))
objects = os.walk(real_path)

mmm = []

def create_season_dir(split, name):
    matches = re.match(r' ([0-9]{1,2})x[0-9]{1,2} ', name)
    if matches is None:
        return None
    
    season_dir = split[:-1]
    make_dir = os.path.join(*season_dir) + "/Season " + matches.group(1)
    print(make_dir)
    if os.path.isdir(make_dir):
        return make_dir
    elif os.mkdir(make_dir):
        return make_dir
    return None

def move_file_season_folder(name):
    global path_split_count
    
    split = name.split("/")
    split_count = len(split)
    
    if split_count < path_split_count + 2:
        move_dir = create_season_dir(split, name)
        if move_dir is None:
            print(f"Dirty: {name}")
            return False
        
        if os.rename(name, move_dir + "/" + split[-1]):
            return move_dir + "/" + split[-1]
        
        print(f"Rename failed: {name}")
        return False
    
    return name

def check_filename_format(name):
    global path_split_count, mmm
    
    split = name.split("/")
    season = split[path_split_count].split(" ")[1]
    mmm.append(season)
    
    split_count = len(split)
    
    if split_count < path_split_count + 2:
        move_dir = create_season_dir(split, name)
        if move_dir is None:
            print(f"Dirty: {name}")
            return
        
        os.rename(name, move_dir + "/" + split[-1])

for root, dirs, files in objects:
    for file in files:
        name = os.path.join(root, file)
        
        if os.path.isdir(name):
            continue
        
        skip = ['jpg', 'nfo', 'png', 'hidden', 'srt', 'idx', 'sub', 'smi']
        delete = ['DS_Store', 'txt']
        inspect = ['metadata', 'filename']
        info = os.path.splitext(name)
        
        if info[1][1:] in delete:
            os.unlink(name)
            print(f"Delete: {name}")
            continue
        
        if info[1][1:] in skip:
            continue
        
        correct_name = move_file_season_folder(name)
        if correct_name == False:
            continue
        
        check_filename_format(correct_name)

print(list(set(mmm)))
