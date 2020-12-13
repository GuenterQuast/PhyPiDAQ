# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import numpy as np, time, sys, spidev, math


class MAX31865Config(object):
  '''RTD-to-Digital Converter - configuration and interface'''

  def __init__(self, confdict = None):
    if confdict==None: confdict={}
          
# -- number of wires PT100
    if "NWires" in confdict:
      self.NWires = confdict["NWires"]  
    else:
      self.NWires = 3
      
# -- number of Channels
    self.NChannels = 1
    
# -- reference resistor
    if 'Rref' in confdict:
      self.Rref = confdict['Rref']
    else:
      self.Rref = 430
      
# -- resistance of PT100 at 0°C
    if 'R0' in confdict:
      self.R0 = confdict['R0']
    else:
      self.R0 = 100.
      
# -- paramters for Callendar-Van Dusen equation
    # for more informations read:
    # http://www.analog.com/media/en/technical-documentation/application-notes/AN709_0.pdf
    # for T > 0
    # T(R) = (-A + sqrt(A²-4B(a-R/R0)))/2B
    # T(R) = (Z1 + sqrt(Z2+Z3*R)/Z4
    self.A = 3.9083e-3
    self.B = -5.775e-7
    self.C = -4.183e-12
    self.Z1 = -self.A
    self.Z2 = self.A*self.A-4*self.B
    self.Z3 = 4*self.B/self.R0
    self.Z4 = 2*self.B
    # for T < 0
    # using a best fit polynomial expression for RTD (using mathematica) from the link above
    # for calculation see acquireData(self, buf)

  def init(self):
  #Hardware configuration:
    try:
      # create an spi instance for MAX31865
      #/CS = CE0(GPIO8), SDO = MISO(GPIO9), SDI = MOSI(GPIO10), CLK = SCLK(GPIO11)
      self.spi = spidev.SpiDev()
      self.spi.open(0,0) 
      self.spi.mode = 1
      # setting SPI-frequenz to 5 MHz
      self.spi.max_speed_hz = 5000000
      # determine configuration register and write it to MAX31865       
      self.SPIMessage = [0x80] # write address
      # config register
      # ---------------
      # bit 7: Vbias -> 1 (ON)
      # bit 6: Conversion mode -> 1 (AUTO)
      # bit 5: 1-shot = 0 (auto)
      # bit 4: 3-wire RTD -> 1
      #        2-wire or 4-wire RTD -> 0
      # bit 3 and 2: ault detection cyle -> 0 (none)
      # bit 1: fault status clear -> 1 (clear any fault)
      # bit 0: 50/60 Hz filter select -> 1 (50 Hz)
      # for 3-wire RTD: 0b11010011 = 0xD3
      # for 2-wire or 4-wire RTD: 0b11000011 = 0xC3
      if self.NWires == 2 or self.NWires == 4:
        self.SPIMessage.append(0xC3)
      elif self.NWires == 3:
        self.SPIMessage.append(0xD3)
      else:
        print("MAX31865Config: configuration error (incorrect number of wires")
        sys.exit(1)
      self.spi.writebytes(self.SPIMessage)
      time.sleep(0.1)
      
    except Excpetion as e:
      print("MAX31865Config: Error initialising device - exit")
      print(str(e))
      sys.exit(1)

 # provide configuration parameters
    self.ChanLims = [[-10., 110.]]
    self.ChanNams = [str(1)]
      
  def acquireData(self, buf): 
    self.Data = self.spi.readbytes(9)
    del self.Data[0] # delete first empy byte
    self.ADCdata = (self.Data[1] << 8 | self.Data[2]) >> 1 # 15-bit ADC Data
    # calculation of resistant PT100
    self.RPT100 = (self.ADCdata * self.Rref) / 32767
    # calculation for T > 0
    if self.RPT100 > 100:
      buf[0] = (self.Z1 + math.sqrt(self.Z2 + self.Z3 * self.RPT100)) / self.Z4

    # calculation for T < 0
    else:
      buf[0] = -242.02 + 2.2228*self.RPT100 + 2.5859e-3 * self.RPT100 ** 2 - 4.8260e-6 * self.RPT100**3 -2.8183e-8 * self.RPT100 **4 + 1.5243e-10 * self.RPT100**5
    
  def closeDevice(self):
   # nothing to do here
   pass

  if __name__== "__main__":
    import MAX31865Config
    sig = [0]
    max = MAX31865Config.MAX31865Config()
    max.init()
    for i in range(10):
      max.acquireData(sig)
      time.sleep(1)
