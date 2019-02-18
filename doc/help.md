# PhyPiDAQ

## Data Acquisition and analysis for Physics education with Raspberry Pi

This *python3*  code provides some basic functionality for data acquisition and visualisation like data logger, bar-chart, XY- or oscilloscope display and data recording on disk.  

In addition to the GPIO inputs/outputs of the Raspberry Pi, the analog-to-digital converters ADS1115 and MCP3008 and PicoScope USB-oscilloscopes are supported as input devices for analog data, as well as a number of digital sensors using protocols like I²C or SPI.

This graphical user interface helps manage configuration options and can be used to start data collection. The configurations and generated data files are stored in a dedicated sub-directory in *$HOME/PhyPi*. The respective file names are derived from a user-defined day and the current date and time.


## Operating instructions
In the tab **Control**, the main configuration file of the type *.daq* is set - the default is
*$HOME/PhyPi/ phypi.daq*. This file specifies at least one additional configuration file containing the configuration for the sensor or ADC used (hereafter referred to as 'Device'). Furthermore, the working directory (default *$HOME/PhyPi/*) and a tag for the measurement project can be specified in this tab. 
With the Start button we start the script `run_phypi.py`, which controls the data acquisition.

The **Configuration** tab displays the content of the configuration files, which and can be edited and saved after activating the `EditMode` button. The file name used for the main configuration is the name set in the Control tab as the tag; the names for the device configuration files are the file names specified in the main configuration, including any given file paths.

The tab **Help/Hilfe** gives instructions for use in English or German language.