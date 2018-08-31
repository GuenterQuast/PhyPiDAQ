# PhyPiDAQ

Data Acquisition and analysis for Physics education with Raspberry Pi

This *python3*  code provides some basic functionality for data acquisition and visualization like data logger, bar-chart, XY- or oscilloscope display. The visualization depends on *matplotlib.pyplot*, *Tkinter* and *pyQt5*.

In addition to the GPIO inputs/outputs of the Raspberry Pi, the analog-to-digital converters MCP3008 and ADS1115 and PicoScope USB-Oscilloscopes are supported as input devices for analog data, as well as a number of digital sensors using protocols like I²C or SPI. 

## Quick-start guide

After installation - see below - a number of unified classes for data acquisition is available from the sub-directory `./phypidaq`.
Each device needs a specific configuration, which is read from configuration files in subdirectory `./config`. The overall configuration is given in files of type `.daq`, specifying which devices and display modules to use, the readout rate, calibrations or analytical formulae to be applied to recorded data, or ranges and axis labels of the graphical output. 

A graphical user interface `phypi.py` aids in the administration of the configuration options and can be used to start data acquisition. In this case, configurations and produced data files are stored in a dedicated subdirecotry in `$HOME/PhyPi`.The name is derived from a user-defined tag and the current date and time.

Data acquisition may also be started via the command line:

    run_phypi.py <config_file_name>.daq

If no configuration file is given, the default `PhyPiConf.daq` is used.

The sub-directory `./examples` contains a number of simple *python* scripts illustrating the usage of data acquisition and display modules with minimalist code. 

## Installation

This package relies on code from some other packages that need to be installed first:

```html
- Adafruit Pyhon MCP3008 library, <https://github.com/adafruit/Adafruit_Python_MCP3008>
- Adafruit Python ADX1x15 library, <https://github.com/adafruit/Adafruit_Python_ADS1x15>
- http://github.com/GuenterQuast/picoDAQ
- the  *python* bindings of the *pico-python* project by Colin O'Flynn  
   <https://github.com/colinoflynn/pico-python> and
- the low-level drivers contained in the Pico Technology Software Development Kit,
  <https://www.picotech.com/downloads>
```

For conveniencs, installation files for external packages in pip wheel format are provided in subrirectory *.whl*.

After setting up your Raspberry Pi with the actual
stable debian release *stretch*, the following steps should be taken to update and install all necessary packages:

```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-scipy
sudo apt-get install python3-matplotlib
sudo apt-get install python3-pyqt5

sudo pip3 install pyyaml

# PicoTech base drivers for picoScope usb devices
#   see https://www.picotech.com/support/topic14649.html
# after inclusion of the picotech raspbian repository:  
sudo apt-get install libps2000a

# get PhyPiDAQ code and dependencies
mkdir git
cd git
git clone https://GuenterQuast/PhyPiDAQ
cd PhyPicDAQ/whl
sudo pip3 install *.whl
```
## Recommended Sensors and Devices

## Description of the examples
