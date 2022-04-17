#!/usr/bin/python
import os
import sys
import gi
import threading
import time

threads = []

gi.require_version('GnomeDesktop', '3.0')
from gi.repository import Gio, GnomeDesktop

def make_thumbnail(factory, filename):
    mtime = os.path.getmtime(filename)
    # Use Gio to determine the URI and mime type
    f = Gio.file_new_for_path(filename)
    uri = f.get_uri()
    info = f.query_info(
        'standard::content-type', Gio.FileQueryInfoFlags.NONE, None)
    mime_type = info.get_content_type()

    if factory.lookup(uri, mtime) is not None:
        print "FRESH       %s" % uri
        return False

    if not factory.can_thumbnail(uri, mime_type, mtime):
        print "UNSUPPORTED %s" % uri
        return False

    thumbnail = factory.generate_thumbnail(uri, mime_type)
    if thumbnail is None:
        print "ERROR       %s" % uri
        return False

    print "OK          %s" % uri
    factory.save_thumbnail(thumbnail, uri, mtime)
    return True

def thumbnail_folder(factory, folder):
    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in filenames:
            t = threading.Thread(target=make_thumbnail, args=(factory,os.path.join(dirpath, filename),))
            threads.append(t)
            t.start()

            while len(threads) > 4:
                time.sleep(0.05)
                i = 0
                while i < len(threads):
                    if threads[i].is_alive():
                        i = i + 1
                    else:
                        del threads[i]


def main(argv):
    factory = GnomeDesktop.DesktopThumbnailFactory()
    for filename in argv[1:]:
        if os.path.isdir(filename):
            thumbnail_folder(factory, filename)
        else:
            make_thumbnail(factory, filename)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
