# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import numpy as np, time, sys
import multiprocessing as mp

# display module
from phypidaq.mpTkDisplay import mpTkDisplay

class Display(object):
  '''configure and control graphical data displays'''

  def __init__(self, interval = 0.1, confdict = None):

    if confdict!=None: 
      self.confdict = confdict      
    else:
      self.confdict={}

# set options for graphical display
    if 'Interval' not in self.confdict:
      self.confdict['Interval'] = interval
    else:
      interval = self.confict['Interval']
    if interval < 0.05:
      print(" !!! read-out intervals < 0.05 s not reliable, setting to 0.05 s")
      self.confdict['Interval'] = 0.05

    if 'XYmode' not in self.confdict:  # default is XY mode off
      self.confdict['XYmode'] = False

    if 'DisplayModule' not in self.confdict: # default display is DataLogger
      self.confdict['DisplayModule'] = 'DataLogger'

    if 'startActive' not in self.confdict:  # default is to start in Paused mode
      self.confdict['startActive'] = False

# set channel properties
    if 'NChannels' not in self.confdict:  
      self.confdict['NChannels'] = 1

    if 'ChanLimits' not in self.confdict:
      self.confdict['ChanLimits'] = [ [0., 5.] ]

    if 'ChanNams' not in self.confdict:
      self.confdict['ChanNams'] = ['']*self.confdict['NChannels']

    if 'ChanUnits' not in self.confdict:
      self.confdict['ChanUnits'] = ['V']*self.confdict['NChannels']

    if 'ChanLabels' not in self.confdict:
      self.confdict['ChanLabesl'] = ['']*self.confdict['NChannels']

# set display control options
    if 'startActive' not in self.confdict:  # start with active data taking
      self.self.confdict['startActive'] = True

    if 'DAQCbtrk' not in self.confdict:  # no run control buttons
      self.confdict['DAQCntrl'] = False

  def init(self):
    '''create data transfer queue and start display process'''
 
    self.procs=[]
    cmdQ = None
    self.DmpQ = mp.Queue(1) # Queue for data transfer to sub-process
    DisplayModule = self.confdict['DisplayModule']
    self.procs.append(mp.Process(name=DisplayModule, target = mpTkDisplay, 
           args=(self.DmpQ, self.confdict, DisplayModule , cmdQ) ) )
#                   Queue      config       ModuleName    commandQ

    for prc in self.procs:
      prc.deamon = True
      prc.start()
      print(' -> starting subprocess ', prc.name, ' PID=', prc.pid)

  def show(self, dat): 
    self.DmpQ.put(dat)

  def close(self):
    for p in self.procs:
      if p.is_alive():
        p.terminate()
        print('    terminating ' + p.name)
        time.sleep(1.)

