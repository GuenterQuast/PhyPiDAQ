# PhyPiDAQ

Data Acquisition and analysis for Physics education with Raspbery Pi

This *python3*  code provides some basic functionality for data acquisition
and  visualization like data logger, bar-chart, XY- or oscilloscope display. The
visualization depends on *matplotlib.pyplot* and **Tkinter*.

In addition to the GPIO inputs/outputs of the Raspberry Pi, the analog-to-digital
converters MCP3008 and ADS1115 and PicoScope USB-Oscilloscopes are 
supported as input devices for analog data, as well as a number of digital
sensors using 1-wire protocols of the  I²C or SPI bus protocols. 

##Installation

This package relies on code from some other packages that need to be installed first:
    - Adafruit Pyhon MCP3008 library, <https://github.com/adafruit/Adafruit_Python_MCP3008>
    - Adafruit Python ADX1x15 library, <https://github.com/adafruit/Adafruit_Python_ADS1x15>
    - http://github.com/GuenterQuast/picoDAQ
    - the  *python* bindings of the *pico-python* project by Colin O'Flynn  
       <https://github.com/colinoflynn/pico-python> and
    - the low-level drivers contained in the Pico Technology Software Development Kit,
      <https://www.picotech.com/downloads>

For conveniencs, installation files for external packages in pip wheel format are provided 
in subrirectory *.whl*.

After setting up your Raspberry Pi, the following steps should be taken to update and  
install all necessary packages:

```
sudo apt-get update
sudo apt-get upgrade

sudo pip3 install --upgrade numpy
sudo pip3 install scipy
sudo pip3 install matplotlib
sudo pip3 install pyyaml

# PicoTech base drivers for picoScope usb devices
#   see https://www.picotech.com/support/topic14649.html

# get picoCosmo code and dependencies
mkdir git
cd git/PhyPicDAQ/whl
sudo pip3 install *.whl
```
## Recommended Sensors and Devices

##Description of the examples
