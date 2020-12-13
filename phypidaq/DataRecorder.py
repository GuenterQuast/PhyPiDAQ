from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import sys, time, numpy as np

class DataRecorder(object):
  ''' store data to fle
  '''

  def __init__(self, Fname, ConfDict):
    '''Args:  

         Fname: file name
         ConfDict: configuration dictionary
         delim: field separator
    '''

    if 'CSVseparator' in ConfDict:
      self.sep = ConfDict['CSVseparator']
    else:
      self.sep = ','
    self.dT = ConfDict['Interval'] 
    self.NChan = ConfDict['NChannels']
    self.ChanLim = ConfDict['ChanLimits']
    ChanNams = ConfDict['ChanNams']
    if 'ChanLabels' in ConfDict:
      ChanLabels = ConfDict['ChanLabels']
    else:
      ChanLabels = [''] * self.NChan
    if 'ChanUnits' in ConfDict:
      ChanUnits = ConfDict['ChanUnits']
    else:
      ChanUnits = [''] * self.NChan

    self.ChanTags = []
    for i, c in enumerate(ChanNams):
      self.ChanTags.append( c + ':' + ChanLabels[i] + '('+ChanUnits[i]+')')

    fname = Fname.split('.')
    fnam = fname[0]
    if len(fname) > 1:
      fext = fname[1]
    else:
      fext = 'dat'
    datetime=time.strftime('%y%m%d-%H%M', time.localtime())
    self.f = open(fnam + '_' + datetime + '.' + fext, 'w')

    # write header:
    print('# PhyPiDAQ Data recorder ', datetime,
      file = self.f)
    print('#   logging interval {0:.3g}'.format(self.dT),
          file = self.f)
    print('# ', end = '', file = self.f)
    print(self.sep.join( self.ChanTags), 
          file = self.f)
    
  def __call__( self, data ):
    if data is not None:
      print(self.sep.join(['{0:.4g}'.format(d) for d in data]) ,
              file = self.f)

  def close(self):
  # explicit close method
    if not self.f.closed: self.f.close()

#  def __del__(self):
#  # define a destructor in case .close() is forgotten
#    if not self.f.closed: self.f.close()
      
#-end class DataRecorder
