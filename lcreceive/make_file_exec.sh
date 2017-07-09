#!/bin/bash

git clone https://github.com/PavloMykhailyshyn/LocalChat_-LC-

cd LocalChat_-LC-

chmod +x lcreceive.py
chmod +x lcsend.py
chmod +x daemon.py

path_to_receive=$(pwd)/lcreceive.py
path_to_send=$(pwd)/lcsend.py
path_to_daemon=$(pwd)/daemon.py

cd ..
cd /bin

sudo ln -s $path_to_receive
sudo ln -s $path_to_send
sudo ln -s $path_to_daemon
