# PhyPiDAQ

Data Acquisition and analysis for Physics education with Raspbery Pi

This *python3*  code provides some basic functionality for data acquisition
and  visualisation like data logger, bar-chart or XY-display. The visualization
depends on *matplotlib.pyplot* and **Tkinter*.

The code has been tested with various sensors and the PicoScope USB-Oscilloscope.
Examples are provided below.

##Installation

This package relies on code from some other packages that need to be installed first:

    - http://github.com/GuenterQuast/picoDAQ
    - the  *python* bindings of the *pico-python* project by Colin O'Flynn  
       <https://github.com/colinoflynn/pico-python> and
    - the low-level drivers contained in the Pico Technology Software Development Kit,
      <https://www.picotech.com/downloads>

After setting up your Raspberry Pi, the following steps should be taken to update and  
install all necessary packages:

```
sudo apt-get update
sudo apt-get upgrade

sudo pip3 install --upgrade numpy
sudo pip3 install scipy
sudo pip3 install matplotlib
sudo pip3 install pyyaml
sudo apt-get install pyqt5-dev
sudo apt-get install pyqt5-tools

sudo apt-get install at-spi2-core

# following needs Pico Tech drivers for picoScope usb devices
# see https://www.picotech.com/support/topic14649.html

# get picoCosmo code and dependencies
mkdir git
cd git
git pull https://github.com/GuenterQuast/PhyPiDAQ
cd PhyPiDAQ/whl
sudo pip3 install *.whl
```
## Recommended Sensors and Devices

##Description of the examples
