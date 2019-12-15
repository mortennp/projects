#!/bin/sh
backup_filename="motioneye-config.tar.gz"
config_dir="config"
mv ~/Downloads/$backup_filename $config_dir/
cd $config_dir
tar -xzf $backup_filename --overwrite
rm $backup_filename


