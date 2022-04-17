#!/usr/bin/env python3
import re
from os import listdir, remove, rename
from os.path import isfile, join, getsize
from pprint import pprint

path = r'/films'

ignored = [
    'jpg',
    'hidden',
    'xattr',
    'nfo',
    'idx',
    'sub',
    'srt',
    'ts',
    'smi',
    'png',
    'sup'
]


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


pattern = "([a-zA-Z0-9,\-\.&! ]*|[a-zA-Z0-9',\-\.&! ]*) (\([0-9]{4}\))\.(avi|mkv|mp4|m4v)"


def iterate_films():

    film_dirs = sorted([f for f in listdir(path) if not isfile(join(path, f))])

    for filmdir in film_dirs:
        films = sorted([f for f in listdir(path + "/" + filmdir) if isfile(join(path + "/" + filmdir, f))])
        to_check = []

        for file in films:
            pos = file.rfind(".")
            extension = file[pos+1:len(file)]
            if extension not in ignored:
                to_check.append(file)
        
        if len(to_check) <= 1:
            continue

        if len(to_check) > 2:
            print(bcolors.WARNING + ">>>>>> Wobble <<<<<<<" + bcolors.ENDC)
            pprint(to_check)
            continue

        size0 = getsize(path + "/" + filmdir + "/" + to_check[0])
        size1 = getsize(path + "/" + filmdir + "/" + to_check[1])
        name0 = to_check[0]
        name1 = to_check[1]
        fullname0 = path + "/" + filmdir + "/" + to_check[0]
        fullname1 = path + "/" + filmdir + "/" + to_check[1]

        if re.match(pattern, name0):
            print(bcolors.OKGREEN + name0 + bcolors.ENDC)
            print(bcolors.BOLD + name1 + bcolors.ENDC)
            print(size0)
            print(size1)

            if size0 >= size1:
                remove(fullname1)
                print("keep 0 name and size are good")
            else:
                remove(fullname0)
                print(bcolors.FAIL + "1 is better, larger file size" + bcolors.ENDC)
                rename(fullname1, fullname0)

            print("")
            continue

        if re.match(pattern, name1):
            print(bcolors.OKGREEN + name1 + bcolors.ENDC)
            print(bcolors.BOLD + name0 + bcolors.ENDC)
            print(size0)
            print(size1)

            if size1 >= size0:
                remove(fullname0)
                print("keep 1 name and size are good")
            else:
                remove(fullname1)
                print(bcolors.FAIL + "0 is better, larger file size" + bcolors.ENDC)
                rename(fullname0, fullname1)

            print("")
            continue

        print("no match")
        print(fullname0)
        print(fullname1)



if __name__ == "__main__":
    iterate_films()
