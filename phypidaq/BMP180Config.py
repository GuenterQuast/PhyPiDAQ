# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import numpy as np, time, sys

# import relevant pieces for Bosch BMP180 temperature and pressure sensor
import Adafruit_BMP.BMP085 as BMP085

class BMP180Config(object):
  '''digital thermometer DS18B20Config configuration and interface'''

  def __init__(self, confdict = None):
    if confdict==None: confdict={}
          
# -- number of Channels
    self.NChannels = 2
    self.ChanLims = [[-40., 85.],[300., 1100.]]
    self.ChanNams = [['Temperature'],['Pressure']]
    self.ChanUnits= [['°C'],['hPa']]


  def init(self):

    try:
      self.sensor = BMP085.BMP085()
      #self.sensor = BMP085.BMP085(busnum=2)

      # BMP085 mode: one of 
      #   BMP085_ULTRALOWPOWER,
      #   BMP085_STANDARD
      #   BMP085_HIGHRES, or 
      #   BMP085_ULTRAHIGHRES.  See the BMP085
      #self.sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)
    except EXEPTION as e:      
       print("BMP180: Error initialising device - exit")
       print(str(e))
       sys.exit(1)
      
  def acquireData(self, buf):

    buf[0] = self.sensor.read_temperature()
    if self.NChannels > 1:
      buf[1] = self.sensor.read_pressure()/100. # in hPa

    #  buf[2] = sensor.read_altitude()))
    #  buf[3] = sensor.read_sealevel_pressure()))

  def closeDevice(self):
   # nothing to do here
    pass
