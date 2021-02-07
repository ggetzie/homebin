#! /bin/bash

sudo supervisord
sudo service nginx start
sudo service postgresql start
sudo service redis-server start
sudo mkdir /var/run/screen
sudo chmod 777 /var/run/screen
