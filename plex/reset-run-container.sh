#!/bin/sh
docker stop plex
docker rm plex
#rm -rf /opt/plex/config
#rm -rf /opt/plex/transcode
#docker build --tag plex .
docker run \
    -d \
    --name plex \
    --net host \
    -p 32400:32400 \
    --restart always \
    -v /opt/plex/config:/config \
    -v /opt/plex/transcode:/transcode \
    -v /opt/plex/data:/data \
    --device=/dev/sda1 \
    --device=/dev/sdb1 \
    --privileged \
    plex 

# !!!!!!!!!! IMPORTANT !!!!!!!!!!
# Now VNC into RPi and use Chromium to sign-in to localhost:32400 using credentials from plex.tv!
# vncserver
# vncserver kill :1

# BACKUP
#cd /opt/plex
#sudo tar -zcvf plex-config.tar.gz config
#sudo tar -zcvf plex-transcode.tar.gz transcode
#sudo mv *.tar.gz ~/Downloads
