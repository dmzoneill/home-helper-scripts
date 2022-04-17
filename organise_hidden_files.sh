#!/bin/bash -x

IFS=$'\n'

cd /series
for X in `ls`; do cp -v $HOME/bin/.hidden "$X/"; done

cd /films
for X in `ls`; do cp -v $HOME/bin/.hidden "$X/"; done

cd /music
for X in `find . -type d -print`; do 
  cp -v $HOME/bin/.hidden $X/
done

cd /series
for X in `find . -type d -name "Season*" -print`; do 
  cp -v $HOME/bin/.hidden $X/
done
