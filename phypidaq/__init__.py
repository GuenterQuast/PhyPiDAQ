"""

.. moduleauthor:: Guenter Quast <guenter.quast@online.de>

.. module PhyPiDAQ
   :synopsis: data acquisition and analysis with Raspberry Pi

.. moduleauthor:: Guenter Quast <g.quast@kit.edu>

**phypidaq**
    *data qcquisition and analysis with Raspberry Pi for Physics*  

    a collction of toos to aquire data from a hardware device
    and to display and anayze data 
"""

# Import version info
from ._version_info import *
# and set version 
_version_suffix = ''  # for suffixes such as 'rc' or 'beta' or 'alpha'
__version__ = _version_info._get_version_string()
__version__ += _version_suffix

# Import components to be callable at package level
__all__ = [ "helpers", "Display", "DataLogger", "DataRecorder", "DataGraphs",
            "PSConfig", "MCP3x08Config", "ADS1115Config", "HX711Config", "MAX31865Config",
            "GPIOCount", "DS18B20Config", "MAX31855Config", "BMP180Config", "BMPx80Config", 
            "MMA8451Config, INA219Config"]
