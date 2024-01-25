#!/bin/bash

days_ago=7  # Specify the number of days ago for file creation date

target_date=$(date -d "$days_ago days ago" +%s)  # Calculate the target date in seconds since epoch

search_videos() {
    local current_path="$1"
    local current_date=$(stat -c %Y "$current_path")

    if [[ -f "$current_path" && $(file -b --mime-type "$current_path") =~ video/ ]]; then
        echo "Video file found: $current_path"
    fi

    if [[ -d "$current_path" && $current_date -ge $target_date ]]; then
        for item in "$current_path"/*; do
            search_videos "$item"
        done
    fi
}

search_videos "/films"
search_videos "/series"
