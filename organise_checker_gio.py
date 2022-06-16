#!/usr/bin/env python

import os
from gi.repository import Gio

debug = True
films = "/smb/films/Entertainment/Films"
series = "/smb/series/Entertainment/Series"
attribute = "metadata::custom-icon"
ignore = [".DS_Store", ".hidden"]

def debug(s, override = False):
    if debug and not override:
        print(s)

def unset_folder_art(path):
    debug("Unset: " + path)
    folder = Gio.File.new_for_path(path)
    info = folder.query_info(attribute, 0, None)
    info.set_attribute(attribute, Gio.FileAttributeType.INVALID, 0)
    folder.set_attributes_from_info(info, 0, None)

def set_folder_art(path, icon):
    debug("Set: " + path)
    folder = Gio.File.new_for_path(path)
    icon_file = Gio.File.new_for_path(icon)
    info = folder.query_info(attribute, 0, None)
    icon_uri = icon_file.get_uri()
    info.set_attribute_string(attribute, icon_uri)
    folder.set_attributes_from_info(info, 0, None)

def update_folder_art(path):
    if os.path.exists(path + "/folder.jpg"):
        set_folder_art(path, path + "/folder.jpg")
    else:
        unset_folder_art(path)    

def update(direct):
    for name in sorted(os.listdir(direct)):
        update_folder_art(direct + "/" + name)

def show_empty_folder_art(path):
    folder = Gio.File.new_for_path(path)
    info = folder.query_info(attribute, 0)
    if info.get_attribute_string(attribute) is None:
        debug(attribute + " unset: " + path)
    if len(os.listdir(path)) <= 1:
        debug("Delete empty folder: " + path)
        try:
            os.remove(path + "/.hidden")
        except Exception as error:
            debug(str(error), True)
        try:
            os.rmdir(path)
        except Exception as error:
            debug(str(error), True)

def show_unset(direct):
    for name in sorted(os.listdir(direct)):
        if name in ignore:
            continue
        show_empty_folder_art(direct + "/" + name)

if __name__ == "__main__":
    update(films)
    update(series)
    show_unset(films)
    show_unset(series)
