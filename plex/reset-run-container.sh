#!/bin/sh
docker stop plex
docker rm plex
#rm -rf /opt/plex/config
#rm -rf /opt/plex/transcode
#docker build --tag plex https://github.com/greensheep/plex-server-docker-rpi.git
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
    -v $(pwd):/scripts \
    plex \
#    /bin/bash -c '/scripts/mount.sh'
#    -v /dev/sda1:/mnt/usb1/FLAC \
#    -v /dev/sdb1:/mnt/usb2/FLAC \
docker exec plex mkdir -p /mnt/usb1/FLAC
docker exec plex mount /dev/sda1 /mnt/usb1/FLAC
docker exec plex ls /mnt/usb1/FLAC
docker exec plex mkdir -p /mnt/usb2/FLAC
docker exec plex mount /dev/sdb1 /mnt/usb2/FLAC
docker exec plex ls /mnt/usb2/FLAC

# !!!!!!!!!! IMPORTANT !!!!!!!!!!
# Now VNC into RPi and use Chromium to sign-in to localhost:32400 using credentials from plex.tv!
# vncserver
# vncserver kill :1

# BACKUP
#cd /opt/plex
#sudo tar -zcvf plex-config.tar.gz config
#sudo tar -zcvf plex-transcode.tar.gz transcode
#sudo mv *.tar.gz ~/Downloads