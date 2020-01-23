#!/bin/sh
docker run \
-d \
--name plex \
-p 32400:32400/tcp \
-p 3005:3005/tcp \
-p 8324:8324/tcp \
-p 32469:32469/tcp \
-p 1900:1900/udp \
-p 32410:32410/udp \
-p 32412:32412/udp \
-p 32413:32413/udp \
-p 32414:32414/udp \
-e TZ="Europe/Copenhagen" \
-e PLEX_CLAIM="claim-zVUn7LcxPvF3uf2mP-sq" \
-e ADVERTISE_IP="http://192.168.1.39:32400/" \
-h raspberrypi \
-v /opt/plex/database:/config \
-v /opt/plex/transcode:/transcode \
-v /opt/plex/data:/data \
plexinc/pms-docker