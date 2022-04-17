#!/bin/bash
IFS=$'\n'

cd /smb/synology/Entertainment/Series/.

if [ $? -eq 1 ]; then
    exit 1
fi

for X in `find . -type f  | grep -viP "\d{1,2}x\d{1,2}" | grep -v 'jpg\|png\|.hidden\|nfo\|DS_Store'`; do 
    echo $X; 
    filebot -rename -non-strict --db TheTVDB --action move "$X";
done

curl -s http://192.168.0.30:8989/api/command -H 'X-Api-Key: 7d4c6788b05948a58f2423f6e795532b' --data-binary '{ "name": "rescanSeries" }'
