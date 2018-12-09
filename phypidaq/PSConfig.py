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
    self.PSconfDict = self.PS.OscConfDict

# collect configuration parameters
    self.NChannels = self.PS.NChannels
    self.ChanNams = self.PSconfDict['Channels']
    CRanges = self.PSconfDict['CRanges']
    COffsets = self.PSconfDict['ChanOffsets']
    self.ChanLims = []
    for i in range(self.NChannels):
     self.ChanLims.append( (-CRanges[i]-COffsets[i], 
                        CRanges[i]-COffsets[i]) )
# RMS or mean of samples ?
    self.AvModes = self.NChannels * [0]
    if 'ChanAverages' in self.confdict:
      ChanAvs = self.confdict['ChanAverages']
      if type(ChanAvs) is not type([]): ChanAvs = [ChanAvs]      
      for i, m in enumerate(ChanAvs):
        if m == 'rms': self.AvModes[i] = 1
        print('Channel %i: averaging mode= %s'%(i,m))
         
# data buffer for PicoScope driver
    self.NSamples = self.PS.NSamples
    self.buf = np.zeros( (self.PS.NChannels, self.PS.NSamples) )

    
  def acquireData(self, sig): 
    # read data from PicoScope

    self.PS.acquireData(self.buf) # read data from PicoScope
    for i, b in enumerate(self.buf): # process data 
      if self.AvModes[i]:
        sig[i] = np.sqrt (np.inner(b, b) / self.NSamples)    # eff. Voltage
      else:
        sig[i] = b.sum() / self.NSamples          # average

  def closeDevice(self):
    self.PS.closeDevice()
