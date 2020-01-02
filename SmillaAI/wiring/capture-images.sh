#!/bin/sh

#https://www.raspberrypi.org/documentation/raspbian/applications/camera.md

rm images/*.mp4
kill $(pgrep raspivid)
raspivid --output images/movie.mp4 --signal --split &
build/SenseLED 
kill $(pgrep raspivid)