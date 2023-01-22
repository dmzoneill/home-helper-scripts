#!/bin/bash
export PATH=/home/dave/.local/bin:/home/dave/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games:/snap/bin
/home/dave/bin/organise_fixmedia.sh
#/usr/bin/python3 /home/dave/bin/organise_checker.py
/usr/bin/python3 /home/dave/bin/organise_checker_gio.py
/usr/bin/python3 /home/dave/bin/organise_series_checker.py
/usr/bin/python3 /home/dave/bin/organise_music_checker.py
/home/dave/bin/organise_hidden_files.sh
