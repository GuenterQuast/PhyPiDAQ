# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import numpy as np, time, sys, os

import pkgutil

class ReplayConfig(object):
  '''replay data from file 
  '''

  def __init__(self, confdict = None):
    if confdict==None: confdict={}
          
    if "csvFile" in confdict:
      self.csvFile = confdict["csvFile"]
    else:
      self.csvFile = None

    if "csvSepatator" in confdict:
      self.csvSeparator = confdict["csvSeparator"]
    else:
      self.csvSeparator = ',' # field separator used in csv file

      
# -- number of Channels is defined in input file
    if "NChannels" in confdict:
      self.NChannels = confdict["NChannels"]
    else:
      self.NChannels = None

  def init(self):

# open data file
    if self.csvFile == None:
      d = pkgutil.get_data('phypidaq', 'PhyPiDemoData.csv').decode('utf-8')
    else:      
      f = open(os.path.expanduser(self.csvFile),'r')
      d = f.read()
      f.close()
    rdata = d.splitlines() 
# read header
    h0 = rdata[0][1:] # remove leading '#'
    h1 = rdata[1][1:]
    tags = rdata[2][1:].split(self.csvSeparator)
    if self.NChannels == None: self.NChannels = len(tags)

    self.data = np.loadtxt(rdata, dtype=np.float32,
                           delimiter=self.csvSeparator,
                           unpack=True)    # read data part of file
    self.Ndat = len(self.data[0]) # number of data points in file
    
  # provide configuration parameters
    self.ChanLims = [ [0., 1.], [0., 1.] ] * self.NChannels
    for i in range(self.NChannels):
      mn = min(self.data[i]).tolist() # .tolist() needed to
      mx = max(self.data[i]).tolist() #   store as python floats
      d = (mx - mn)*0.05
      self.ChanLims[i] = [mn-d, mx+d]
    self.ChanNams = [tags[i].split(':')[0] for i in range(self.NChannels)]

    self.idx = 0   # initialize index to data             
                     
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
