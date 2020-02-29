FROM greensheep/plex-server-docker-rpi:latest

ENV PLEX_PATH=/opt/plex/Application

WORKDIR ${PLEX_PATH}

ADD mount.sh mount.sh

CMD ["sh", "mount.sh"]
