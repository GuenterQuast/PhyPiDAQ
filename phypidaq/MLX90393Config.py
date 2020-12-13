# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import numpy as np, time, sys

## uses Adafruit circuit-python
import busio, board
# adafruit driver class
import adafruit_mlx90393

class MLX90393Config(object):
  '''digital magnetometer MLX90393 configuration and interface'''

  def __init__(self, confdict = None):
    if confdict==None: confdict={}
  # -- number of Channels
    self.NChannels = 3
    self.ChanNams = ['Bx','By','Bz']
    self.ChanUnits= ['mT','mT', 'mT']

    if 'Gain' in confdict:
     self.gain = confdict['Gain']
    else:
     self.gain = 1.
    if self.gain == 1.:
      gc = 0x7
    elif self.gain == 1.33:
      gc = 0x6
    elif self.gain == 1.67:
      gc = 0x5
    elif self.gain == 2.0:
      gc = 0x4
    elif self.gain == 2.5:
      gc = 0x3
    elif self.gain == 3.:
      gc = 0x2
    elif self.gain == 4.:
      gc = 0x1
    elif self.gain == 5.:
      gc = 0x0
    else:
      # invalid gain, set to 1.
      self.gain = 1.
      gc=7     
      print("MLX90393: invalid range - set to 1.0")

    self.mlx90393_gc = gc
    lm = 50./self.gain
    self.ChanLims = [[-lm, lm],[-lm, lm], [-lm, lm]]

  def init(self):
    I2C_BUS = busio.I2C(board.SCL, board.SDA)
    try:
      self.sensor = adafruit_mlx90393.MLX90393(I2C_BUS,
                         gain = self.mlx90393_gc)
    except Exception as e:      
      print("MLX90393: Error setting up device - exit")
      print(str(e))
      sys.exit(1)
      
  def acquireData(self, buf): # in units of mT
    buf[0],buf[1], buf[2] = self.sensor.magnetic
    buf[0] /= 1000.
    buf[1] /= 1000.
    buf[2] /= 1000.

  def closeDevice(self):
   # nothing to do here
    pass



