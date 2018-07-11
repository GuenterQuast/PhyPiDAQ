# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import numpy as np, time, sys

# import relevant pieces from picodaqa ...
from picodaqa.picoConfig import PSconfig

class PSConfig(object):
  '''PicoScope configuration and interface'''

  def __init__(self, confdict = None):
    if confdict == None:
      print('No configuration specified for PicoScope - exiting')
      sys.exit(1) 
    self.confdict = confdict

  def init(self):
    # initialize PicoScope and retreive config parameters
    self.PS = PSconfig(self.confdict)
    self.PS.init()
 
# data buffer for PicoScope driver
    self.buf = np.zeros( (self.PS.NChannels, self.PS.NSamples) )
    self.NSamples = self.PS.NSamples
    self.PSconfDict = self.PS.OscConfDict
 
  def acquireData(self, sig): 
    # read data from PicoScope

    self.PS.acquireData(self.buf) # read data from PicoScope
    for i, b in enumerate(self.buf): # process data 
      #sig[i] = np.sqrt (np.inner(b, b) / self.NSamples)    # eff. Voltage
      sig[i] = b.sum() / self.NSamples          # average

  def closeDevice(self):
    self.PS.closeDevice()
