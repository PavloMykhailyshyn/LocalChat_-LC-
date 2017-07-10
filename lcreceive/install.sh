#!/bin/bash

chmod +x lcreceive
chmod +x lcsend
chmod +x daemon

path_to_receive=$(pwd)/lcreceive
path_to_send=$(pwd)/lcsend
path_to_daemon=$(pwd)/daemon

cd ..
cd /bin

sudo ln -s $(path_to_receive)
sudo ln -s $(path_to_send)
sudo ln -s $(path_to_daemon)


