import os
import subprocess
import urllib.parse
import traceback

delete = False
special = False
gio = True

ignored = [
    "poster.jpg",
    "banner.jpg",
    "folder.jpg",
    "landscape.jpg",
    ".hidden",
    ".xattr",
]

root = "/series"

suggested_series_rename = {}
specials = []


def set_folder_art(series_name):
    gio_cmd = (
        'gio set -t unset "' + root + "/" + series_name + '" metadata::custom-icon'
    )
    if os.path.exists(root + "/" + series_name + "/folder.jpg"):
        gio_cmd = (
            'gio set "'
            + root
            + "/"
            + series_name
            + '" metadata::custom-icon "file://'
            + root
            + "/"
            + urllib.parse.quote(series_name)
            + '/folder.jpg"'
        )
    # os.system(gio_cmd)
    proc = subprocess.Popen(gio_cmd, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    print(gio_cmd)
    if out.decode("ascii").strip() != "":
        print("Out: " + out.decode("ascii"))
    if err is not None:
        print("Err: " + err.decode("ascii"))


def set_folder_art_season(series_name, season):
    gio_cmd = (
        'gio set -t unset "'
        + root
        + "/"
        + series_name
        + "/"
        + season
        + '" metadata::custom-icon'
    )
    if os.path.exists(root + "/" + series_name + "/" + season + "/folder.jpg"):
        gio_cmd = (
            'gio set "'
            + root
            + "/"
            + series_name
            + "/"
            + season
            + '" metadata::custom-icon "file://'
            + root
            + "/"
            + urllib.parse.quote(series_name)
            + "/"
            + urllib.parse.quote(season)
            + '/folder.jpg"'
        )
    # os.system(gio_cmd)
    proc = subprocess.Popen(gio_cmd, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    print(gio_cmd)
    if out.decode("ascii").strip() != "":
        print("Out: " + out.decode("ascii"))
    if err is not None:
        print("Err: " + err.decode("ascii"))


def check_file(series_name, season, episode):
    try:
        season_parts = season.split()
        season_num = season_parts[1]
        if episode.startswith(series_name + " - " + season_num) is False:
            if "special" in episode.lower():
                if special is True:
                    print(
                        "Special: "
                        + series_name
                        + " - "
                        + season_num
                        + " != "
                        + episode
                    )
                return
            print(series_name + " - " + season_num + " != " + episode)
            episode_parts = episode.split(" - ")
            suggested_series_rename[series_name] = episode_parts[0]
            # print("filebot -rename --db TheTVDB -non-strict --action move \"" + root + "/" + series_name + "/Season" + season + "/" + suggested_series_rename[rename_from] + "\"" );
            if delete:
                os.remove(root + "/" + series_name + "/" + season + "/" + episode)
    except Exception as e:
        print(traceback.format_exc())
        print(e)
        print("Except: " + series_name + " - " + season)


def check_season(series_name, season):
    season_directory = root + "/" + series_name + "/" + season
    season_directory = os.fsencode(season_directory)
    for season_file in os.listdir(season_directory):
        season_file_decoded = os.fsdecode(season_file)
        if season_file_decoded not in ignored:
            check_file(series_name, season, season_file_decoded)


def check_series(series_name):
    series_directory = root + "/" + series_name
    series_directory_encoded = os.fsencode(series_directory)
    for season in os.listdir(series_directory_encoded):
        if os.path.isdir(series_directory + "/" + os.fsdecode(season)):
            check_season(series_name, os.fsdecode(season))
            if gio is True:
                set_folder_art_season(os.fsdecode(series_name), os.fsdecode(season))


def iterate_series():
    directory = os.fsencode(root)
    for series_name in os.listdir(directory):
        if os.path.isdir(root + "/" + os.fsdecode(series_name)):
            check_series(os.fsdecode(series_name))
            if gio is True:
                set_folder_art(os.fsdecode(series_name))

    for rename_from in suggested_series_rename:
        if rename_from != suggested_series_rename[rename_from]:
            print(
                'mv "'
                + rename_from
                + '" "'
                + suggested_series_rename[rename_from]
                + '.1"'
            )
            print(
                'mv "'
                + suggested_series_rename[rename_from]
                + '.1" "'
                + suggested_series_rename[rename_from]
                + '"'
            )


if __name__ == "__main__":
    iterate_series()
