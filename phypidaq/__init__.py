"""

.. moduleauthor:: Guenter Quast <guenter.quast@online.de>

.. module PhyPiDAQ
   :synopsis: data acquisition and analysis with Raspberry Pi

.. moduleauthor:: Guenter Quast <g.quast@kit.edu>

**phypidaq**
    *data acquisition and analysis with Raspberry Pi for Physics*  

    a collction of toos to aquire data from hardware devices
    and to display and analyze data 
"""

# Import version info
from ._version_info import *
# and set version 
_version_suffix = 'dev0'  # for suffixes such as 'rc' or 'beta' or 'alpha'
__version__ = _version_info._get_version_string()
__version__ += _version_suffix

# Import components to be callable at package level
__all__ = [ "helpers", "Display", "DataLogger", "DataRecorder", "DataGraphs",
            "ReplayConfig", "ToyDataConfig", 
            "PSConfig", "MCP3x08Config", "ADS1115Config", "groveADCConfig", "GPIOCount",
            "HX711Config", "MAX31865Config", "DS18B20Config", "INA219Config", 
            "MAX31855Config", "BMP180Config", "BMPx80Config", "MMA8451Config", 
            "VL53LxConfig", "TCS34725Config", "AS7262Config", "AS7265xConfig",
            "GDK101Config", "MLX90393Config" ]
