#!/bin/sh
key_name="id_rsa-rpi-remote"
remote_host="raspberrypi.home"

ssh-keygen -t rsa -b 4096 -f ~/.ssh/$key_name
ssh-copy-id -i ~/.ssh/$key_name.pub $remote_host
