# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import numpy as np, sys

class ToyDataConfig(object):
  '''generate artificial data to test/debug PhyPiDAQ
  '''

  def __init__(self, confdict = None):
    if confdict==None: confdict={}
          
# -- number of Channels
    if "NChannels" in confdict:
      self.NChannels = confdict["NChannels"]
    else:
      self.NChannels = 1

  def init(self):

  # provide configuration parameters
    self.ChanLims = [[0., 1.]] * self.NChannels
    self.ChanNams = ['c'+str(i) for i in range(self.NChannels)]

    self.count=0.
    self.offset = 1./(self.NChannels+1.)
    self.amplitude = 0.1
    self.noise = 0.33     # 33% noise
    self.omega = 1./20.
    
  def acquireData(self, buf):
    '''fill random data
    '''
    self.count += 1
    for i in range(self.NChannels):
      buf[i]= (i+1) * self.offset\
        + self.amplitude * (np.sin(self.count*self.omega*(i+1)*np.pi-i*np.pi/3.)\
        + self.noise * np.random.rand())
      
  def closeDevice(self):
   # nothing to do here
    pass
