#!/bin/bash
ls /series/
filebot -script fn:artwork.tvdb -non-strict /series/
ls /films/
filebot -script fn:artwork.tmdb -non-strict /films/
