#!/bin/bash
#
# script to install libraries PhyPiDAQ depends on
#
# -----------------------------------------------

sudo apt-get install python3-yaml
sudo apt-get install python3-scipy
sudo apt-get install python3-matplotlib
sudo apt-get install python3-pyqt5
sudo apt-get install libatlas-base-dev # needed to build nupmy

# some python packages for IO
sudo pip3 install i2cdev
sudo pip3 install spidev
sudo pip3 install pyusb
sudo pip3 install smbus2

sudo pip3 install installlibs/whl/*.whl # python wheels

sudo pip3 install installlibs/tgz/*.tar.gz # python packages 

sudo dpkg -i installlibs/picoscopelibs/*.deb # picoscope 
sudo usermod -a -G tty pi # grant acces to USB for user pi

