#!/bin/sh
docker run --name="motioneye" -p 8765:8765 --hostname="motioneye" \
    -v /etc/localtime:/etc/localtime:ro \
    -v /opt/motioneye/conf:/etc/motioneye \
    -v /opt/motioneye/data:/var/lib/motioneye \
    --device=/dev/video0 \
    --restart="always" \
    --detach=true \
    ccrisan/motioneye:master-armhf
