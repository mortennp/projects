#!/bin/sh
backup_filename="motioneye-config.tar.gz"
config_dir="config"
cd $config_dir
tar -czf $backup_filename *
mv $backup_filename ~/Downloads/