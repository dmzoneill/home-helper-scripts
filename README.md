# Home Helper Scripts

A personal collection of scripts for looking after a home media server.

## Contents

The filename prefix shows what each script works on:

- `deluge_*`: move completed torrents and pause completed public
  torrents through the Deluge RPC API.
- `fs_*`: check and fix TV series folder names, find duplicate films
  and series, report video dimensions, transcode with ffmpeg, dump
  ffprobe data and make thumbnails.
- `organise_*`: check film, series and music libraries for missing
  artwork and hidden files, and set custom folder icons with GIO.
- `lidarr_*`, `radarr_*` and `sonarr_*`: use the Lidarr, Radarr
  and Sonarr APIs to remove corrupt music, import missing albums, find
  missing episodes and fetch films by actor.
- `screensaver-*`: check whether audio is playing before the screen
  saver starts.

## Tech

- Python 3, PHP and Bash
- deluge-client, Jackett, ffmpeg and PyGObject

## Usage

Each script runs on its own. Paths such as `/smb/films` and
`/series/` are hardcoded, and API keys and passwords are read from
environment variables such as `DELUGE_PASSWORD` and `JACKETT_KEY`.

## License

Licensed under the Apache License 2.0. See [LICENSE](LICENSE).
