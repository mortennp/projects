#!/bin/sh
docker stop plex
docker rm plex
rm -rf /opt/plex/config
rm -rf /opt/plex/transcode
./run-greensheep-container.sh