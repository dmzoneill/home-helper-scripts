#!/bin/bash

IFS=$'\n'

function make_thumb {
   echo $1;
   uri=$(echo "$1" | perl -MURI::file -e 'print URI::file->new(<STDIN>)');
   echo $uri
   SUM=$(echo -n "$uri" | md5sum | awk '{print $1}')
   echo $SUM
   cover-thumbnailer "$1" /home/dave/.cache/thumbnails/large/$SUM.png
   echo /home/dave/.cache/thumbnails/large/$SUM.png
   xdg-open /home/dave/.cache/thumbnails/large/$SUM.png
}

function make_thumbs {
  cd $1
  for X in `ls`; do
   echo $X;
   uri=$(echo "$1/$X" | perl -MURI::file -e 'print URI::file->new(<STDIN>)');
   echo $uri
   SUM=$(echo -n "$uri" | md5sum | awk '{print $1}')
   echo $SUM
   if [ ! -f /home/dave/.cache/thumbnails/large/$SUM.png ]; then
     cover-thumbnailer "$1/$X" /home/dave/.cache/thumbnails/large/$SUM.png
   fi
   if [ $1 == "/smb/series/Entertainment/Series" ]; then
     cd $1/$X/
     for Y in `ls -d */`; do
       echo $Y;
       uri=$(echo "$1/$X/$Y" | perl -MURI::file -e 'print URI::file->new(<STDIN>)');
       echo $uri
       SUM=$(echo -n "$uri" | md5sum | awk '{print $1}')
       echo $SUM
       if [ ! -f /home/dave/.cache/thumbnails/large/$SUM.png ]; then
         cover-thumbnailer "$1/$X/$Y" /home/dave/.cache/thumbnails/large/$SUM.png
       fi
     done
     cd $1
   fi
  done
}

if [ $# -eq 1 ]; then
  make_thumb "$1"
else
  make_thumbs /smb/series/Entertainment/Series
  make_thumbs /smb/films/Entertainment/Films
fi


