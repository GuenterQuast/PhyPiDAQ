# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import numpy as np, time, sys

# driver class contained below

# import relevant pieces from adafruit
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI

class MCP3x08Config(object):
  '''ADC MCP3008/3208 configuration and interface'''

  def __init__(self, confdict = None):
    if confdict==None: confdict={}

    if 'ADCChannels' in confdict:
      self.ADCChannels = confdict['ADCChannels']
    else:
      self.ADCChannels = [0]
    self.NChannels = len(self.ADCChannels)

    if 'DifModeChan' in confdict:
       self.DifModeChan = confdict['DifModeChan']
    else:
      self.DifModeChan = [false] * self.NChannels

    if 'VRef' in confdict:
      self.VRef = confdict['VRef']
    else:
      self.VRef = 5.0

    if 'NBits' in confdict:
      self.NBits = confdict['NBits']
    else:
      self.NBits = 10

    self.ADCmax = float( (1 << self.NBits) - 1)
    self.Vfac = self.VRef / self.ADCmax

  def init(self):
  #Hardware SPI configuration:
    SPI_PORT   = 0
    SPI_DEVICE = 0
    try:
      self.MCP = MCP3x08(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), 
        bits = self.NBits )
    except Exception as e:
      print("MCP3x08Config: Error initialising device - exit")
      print(str(e))
      sys.exit(1)

# provide configuration parameters
    self.ChanNams = []
    self.ChanLims = []
    for i, c  in enumerate(self.ADCChannels):
      isdifferential = self.DifModeChan[i]
      if isdifferential:
        if c%2:
          d= str( c) + '-' + str(c-1) 
        else:
          d= str( c) + '-' + str(c+1) 
      else:
        d = str(c)
      self.ChanNams.append(d) 
      self.ChanLims.append(  [- isdifferential * self.VRef , self.VRef])
      
  def acquireData(self, buf): 
    # read data from ADC
    for i, c  in enumerate(self.ADCChannels):
      if self.DifModeChan[i]:
        # need two readings or pair of channels, e.g.:   v = adc(0-1)  - adc(1-0)
        cb=c - c%2    # get lowest channel of pair
        v = (self.MCP.read_adc_difference(cb)\
                      - self.MCP.read_adc_difference(cb+1)) * self.Vfac
        if c%2:  v *= -1  # correct sign if odd channel number given    
        buf[i] = v 
      else:
        buf[i] = self.MCP.read_adc(c) * self.Vfac

  def closeDevice(self):
   # nothing to do here
   pass


"""code to configure and read out MPC3008/3208 analog to digital converter

# modified from original version by Tony DiCola, 
#       Copyright (c) 2016 Adafruit Industries
#   by GuenterQuast@online.de to also support MCP3208
#
# original License:
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""

class MCP3x08(object):
    """Class to represent an MCP3008/3208 analog to digital converter.
       MCP3008: 10 bit resolution (default)
       MCP3208: 12 bit resolution
    """

    def __init__(self, 
      clk=None, cs=None, miso=None, mosi=None, spi=None, gpio=None, bits = 10):
        """Initialize software SPI on the specified CLK, CS, and DO pins.  
        Alternatively can specify hardware SPI by sending an
        Adafruit_GPIO.SPI.SpiDev device in the spi parameter.
        """
        self._spi = None
        # Handle hardware SPI
        if spi is not None:
            self._spi = spi
        elif clk is not None and cs is not None and miso is not None and mosi is not None:
            # Default to platform GPIO if not provided.
            if gpio is None:
                gpio = GPIO.get_platform_gpio()
            self._spi = SPI.BitBang(gpio, clk, mosi, miso, cs)
        else:
            raise ValueError('Must specify either spi for for hardware SPI or clk, cs, miso, and mosi for softwrare SPI!')
        self._spi.set_clock_hz(1000000)
        self._spi.set_mode(0)
        self._spi.set_bit_order(SPI.MSBFIRST)

# 10 bit (MCP3008) or 12 bit (MCP3208) resolution 
        if( bits == 10):
          self.parseMCPResponse = self.parse10bit
        elif( bits == 12):
          self.parseMCPResponse = self.parse12bit
        else:
          print(' !!! MCP3x08: %i bits not supported'%(bits) )

     
    def read_adc(self, adc_number):
        """Read the current value of the specified ADC channel (0-7).  The values
        can range from 0 to 1023 (10-bits).
        """
        assert 0 <= adc_number <= 7, 'ADC number must be a value of 0-7!'
        # Build a single channel read command.
        # For example channel zero = 0b11000000
        command = 0b11 << 6                  # Start bit, single channel read
        command |= (adc_number & 0x07) << 3  # Channel number (in 3 bits)
        # Note the bottom 3 bits of command are 0, this is to account for the
        # extra clock to do the conversion, and the low null bit returned at
        # the start of the response.
        resp = self._spi.transfer([command, 0x0, 0x0])
        return self.parseMCPResponse(resp)

    def read_adc_difference(self, differential):
        """Read the difference between two channels.  Differential should be a
        value of:
          - 0: Return channel 0 minus channel 1
          - 1: Return channel 1 minus channel 0
          - 2: Return channel 2 minus channel 3
          - 3: Return channel 3 minus channel 2
          - 4: Return channel 4 minus channel 5
          - 5: Return channel 5 minus channel 4
          - 6: Return channel 6 minus channel 7
          - 7: Return channel 7 minus channel 6
        """
        assert 0 <= differential <= 7, 'Differential number must be a value of 0-7!'
        # Build a difference channel read command.
        command = 0b10 << 6                  # Start bit, differential read
        command |= (differential & 0x07) << 3  # Channel number (in 3 bits)
        # Note the bottom 3 bits of command are 0, this is to account for the
        # extra clock to do the conversion, and the low null bit returned at
        # the start of the response.
        resp = self._spi.transfer([command, 0x0, 0x0])
        return self.parseMCPResponse(resp)

    def parse10bit(self, r):
            # Parse out the 10 bits of response data and return it.
        res = (r[0] & 0x01) << 9
        res |= (r[1] & 0xFF) << 1
        res |= (r[2] & 0x80) >> 7
        return res & 0x3FF

    def parse12bit(self, r):
        # Parse out the 12 bits of response data and return it.
        res = (r[0] & 0x01) << 11
        res |= (r[1] & 0xFF) << 3
        res |= (r[2] & 0x80) >> 5
        return res & 0xFFF
