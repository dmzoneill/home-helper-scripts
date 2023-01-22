#!/bin/bash -x

IFS=$'\n'

for X in `ls /series`; do echo $X; cp -v $HOME/bin/.hidden "/series/$X/"; done

for X in `ls /films`; do echo $X; cp -v $HOME/bin/.hidden "/films/$X/"; done

for X in `find /music/ -type d -print`; do 
  echo $X;
  cp -v $HOME/bin/.hidden $X/
done

for X in `find /series/ -type d -name "Season*" -print`; do 
  echo $X;
  cp -v $HOME/bin/.hidden $X/
done
