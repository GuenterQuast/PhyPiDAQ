#!/bin/bash
#
# script to install libraries PhyPiDAQ depends on
#
# -------------------------------------------------


sudo apt-get install python3-yaml
sudo apt-get install python3-scipy
sudo apt-get install python3-matplotlib
sudo apt-get install python3-pyqt5
sudo apt-get install libatlas-base-dev # needed to build nupmy
sudo pip3 install installlibs/whl/*.whl
sudo dpkg -i installlibs/picoscopelibs/*.deb

sudo usermod -a -G tty pi # grant acces to USB for user pi

