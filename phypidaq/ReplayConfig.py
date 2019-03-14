# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import numpy as np, time, sys

class ReplayConfig(object):
  '''replay data from file 
  '''

  def __init__(self, confdict = None):
    if confdict==None: confdict={}
          
    if "csvFile" in confdict:
      self.csvFile = confdict["csvFile"]
    else:
      self.csvFile = "ToyData.csv"

# -- number of Channels is defined in input file
    if "NChannels" in confdict:
      self.NChannels = confdict["NChannels"]
    else:
      self.NChannels = None

  def init(self):

# open data file
    f = open(self.csvFile,'r')
# read header
    h0 = f.readline()[1:] # remove leading '#'
    h1 = f.readline()[1:]
    tags = f.readline()[1:].split(',')
    if self.NChannels == None: self.NChannels = len(tags)

    self.data = np.loadtxt(f, dtype=np.float32, delimiter=',', unpack=True)    # read data part of file
    self.Ndat = len(self.data[0]) # number of data points in file
    f.close()
    
  # provide configuration parameters
    self.ChanLims = [ [min(self.data[i]), max(self.data[i]) ] for i in range(self.NChannels)]
    self.ChanNams = [tags[i].split(':')[0] for i in range(self.NChannels)]

    self.idx = 0                 
                     
  def acquireData(self, buf):
    '''return data 
    '''
    for i in range(self.NChannels):
      buf[i] = self.data[i][self.idx]
      self.idx += 1               
      if self.idx == self.Ndat: self.idx = 0
                     
  def closeDevice(self):
   # nothing to do here
    pass
