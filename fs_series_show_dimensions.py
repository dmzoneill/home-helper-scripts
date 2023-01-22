#!/usr/bin/python
import os
import sys
import subprocess
import pprint
import argparse
import ffmpeg

todo = []
delete = []


def query_video(the_file, width, video_path, i):
    try:
        probe = ffmpeg.probe(video_path)
        video_streams = [
            stream for stream in probe["streams"] if stream["codec_type"] == "video"
        ]

        vwidth_str = str(
            video_streams[0]["coded_width"] if "coded_width" in video_streams[0] else 0
        )
        vheight_str = str(
            video_streams[0]["coded_height"]
            if "coded_height" in video_streams[0]
            else 0
        )
        cwidth_str = str(
            video_streams[0]["width"] if "width" in video_streams[0] else 0
        )
        cheight_str = str(
            video_streams[0]["height"] if "height" in video_streams[0] else 0
        )

        line = "{file: <{fwidth}} {vwidth_str: >{vwidth}} {vheight_str: >{vheight}} {cwidth_str: >{cwidth}} {cheight_str: >{cheight}}".format(
            file=video_path,
            vwidth_str=vwidth_str,
            vheight_str=vheight_str,
            cwidth_str=cwidth_str,
            cheight_str=cheight_str,
            fwidth=width,
            vwidth=5,
            vheight=5,
            cwidth=5,
            cheight=5,
        )

        csv_line = (
            '"{file}",{vwidth_str},{vheight_str},{cwidth_str},{cheight_str}'.format(
                file=video_path,
                vwidth_str=vwidth_str,
                vheight_str=vheight_str,
                cwidth_str=cwidth_str,
                cheight_str=cheight_str,
            )
        )

        print(str(i) + ": " + line)
        the_file.write(csv_line + "\n")
    except Exception as e:
        print(e)


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")


def transcode_video(filename):
    # for i in *.divx;   do name=`echo $i | cut -d'.' -f1`;   echo $name;   ffmpeg -i "$i" -c:v libx264 -preset fast "${name}.mkv"; done
    # print("Transcoding " + filename)
    file_name = os.path.splitext(filename)[0]
    command = [
        "/usr/bin/ffmpeg",
        "-i",
        '"' + filename + '"',
        "-c:v",
        "libx264",
        "-preset",
        "fast",
        '"' + file_name + '.mkv"',
    ]
    # print(' '.join(command))
    p1 = subprocess.Popen(" ".join(command), shell=True, stdout=subprocess.PIPE)
    p1.wait()

    if p1.returncode == 0 and os.path.isfile(file_name + ".mkv"):
        # os.remove(filename)
        delete.append(filename)
        return True

    return False


def transcode_folder(folder):
    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in filenames:
            file_extension = os.path.splitext(filename)[1]
            fullpath = os.path.join(dirpath, filename)
            allowed_exts = [".mp4", ".avi", ".mkv"]

            if file_extension not in allowed_exts:
                print("Selected " + fullpath)
                todo.append(fullpath)

    if query_yes_no("Transcode?"):
        for filename in todo:
            transcode_video(filename)


def inspect_path(folder):
    inspect = []
    inspected_width = 0

    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in filenames:
            file_extension = os.path.splitext(filename)[1]
            fullpath = os.path.join(dirpath, filename)
            allowed_exts = [".mp4", ".avi", ".mkv"]

            if file_extension.lower() in allowed_exts:
                inspect.append(fullpath)

                if len(fullpath) > inspected_width:
                    inspected_width = len(fullpath)

    with open("list.csv", "w") as the_file:
        i = len(inspect)
        for video in inspect:
            query_video(the_file, inspected_width + 2, video, i)
            i = i - 1


def show_deleted():
    for filename in delete:
        print('rm "' + filename + '"')


def main(parser, args):
    if args.list != None:
        if os.path.isdir(args.list):
            return inspect_path(args.list)
        else:
            print("Not a folder, check your path")
            return 1

    if args.transcode_directory != None:
        if os.path.isdir(args.transcode_directory):
            return transcode_folder(args.transcode_directory)
        else:
            print("Not a folder, check your path")
            return 1

    if args.transcode_video != None:
        if os.path.isfile(args.transcode_video):
            return transcode_folder(args.transcode_video)
        else:
            print("Not a file, check your path")
            return 1

    parser.print_help(sys.stderr)
    return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find, list and convert videos using ffmpeg"
    )
    parser.add_argument("-l", dest="list", help="folder to scan")
    parser.add_argument("-d", dest="transcode_directory", help="folder to transcode")
    parser.add_argument("-f", dest="transcode_video", help="video to transcode")

    args = parser.parse_args()
    sys.exit(main(parser, args))
