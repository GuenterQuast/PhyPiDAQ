from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import numpy as np, matplotlib.pyplot as plt

class DataLogger(object):
  ''' history of input data

    forked from picoDAQ.DataLogger
  '''

  def __init__(self, ConfDict):
    '''Args:  ConfDict: configuration dictionary
    '''
   # collect relevant configuration parameters
    self.Npoints = 120  # number of points for history

   # get relevant settings from PhyPiConfDict
    self.dT = ConfDict['Interval'] 
    self.NChan = ConfDict['NChannels']
    self.ChanLim = ConfDict['ChanLimits']
    if 'ChanNams' in ConfDict: 
      self.ChanNams = ConfDict['ChanNams']
    else:
      self.ChanNams = [''] * self.NChan 
    if 'ChanClolors' in ConfDict:
      self.ChanColors = ConfDict['ChanColors']
    else:
      self.ChanColors = ['darkblue','sienna']
    if 'ChanLabels' in ConfDict:
      self.ChanLabels = ConfDict['ChanLabels']
    else:
      self.ChanLabels = [''] * self.NChan

    if 'XYmode' in ConfDict:
      self.XYmode = ConfDict['XYmode']
    else:
      self.XYmode = False
    if self.NChan < 2: 
      self.XYmode = False

   # data structures needed throughout the class
    self.Ti = self.dT* np.linspace(-self.Npoints+1, 0, self.Npoints) 
    self.Vhist = np.zeros( [self.NChan, self.Npoints] )
    self.d = np.zeros( [self.NChan, self.Npoints] ) 

# set up a figure to plot actual voltage and samplings from Picoscope
    if self.XYmode:
      fig = plt.figure("DataLogger", figsize=(6.3, 6.) )
      fig.subplots_adjust(left=0.2, bottom=0.15, right=0.95, top=0.95,
                  wspace=None, hspace=.25)
    else:
      fig = plt.figure("DataLogger", figsize=(6., 3.) )
      fig.subplots_adjust(left=0.15, bottom=0.15, right=0.85, top=0.95,
                  wspace=None, hspace=.25)

    axes=[]
    if not self.XYmode:
  # history plot
      axes.append(fig.add_subplot(1,1,1, facecolor='ivory'))
      if self.NChan > 1:
        axes.append(axes[0].twinx())
      for i, C in enumerate(self.ChanNams):
        if i > 1:
          break # works for a maximum of 2 Channels only
        axes[i].set_ylim(*self.ChanLim[i])
        axes[i].set_ylabel('Chan ' + C + ' ' + self.ChanLabels[i], 
            color=self.ChanColors[i])
        axes[i].grid(True, color=self.ChanColors[i], 
                     linestyle = '--', alpha=0.3)
      axes[0].set_xlabel('History (s)')
    else:
  # XY plot
      axes.append(fig.add_subplot(1,1,1, facecolor='ivory'))
      axXY = axes[-1]
      axXY.set_xlim(*self.ChanLim[0])
      axXY.set_ylim(*self.ChanLim[1])
      axXY.set_xlabel('Chan ' + self.ChanNams[0] + ' ' + self.ChanLabels[0], 
         size='x-large', color=self.ChanColors[0])
      axXY.set_ylabel('Chan ' + self.ChanNams[1] + ' ' + self.ChanLabels[1], 
         size='x-large', color=self.ChanColors[1])
      axXY.set_title('XY-View', size='xx-large')
      axXY.grid(True, color='grey', linestyle = '--', alpha=0.3)
  
    self.fig = fig
    self.axes = axes
# -- end def __init__

  def init(self):
  # initialize objects to be animated

  # history graphs
    self.graphs=()
    if not self.XYmode:
      for i, C in enumerate(self.ChanNams):
        if i > 1:
          break  # max. of 2 channels
   # intitialize with graph outside range
        g,= self.axes[i].plot(self.Ti, 
            self.ChanLim[i][1] * 1.1 * np.ones(self.Npoints), 
            color=self.ChanColors[i])
        self.graphs += (g,)
    else:
      g, = self.axes[-1].plot([0.], [0.], color='firebrick')
      self.graphs += (g,)

    return self.graphs
# -- end DataLogger.init()

  def __call__( self, data ):

    if data !=None: 
      n, dat = data

      k = n % self.Npoints
      for i, C in enumerate(self.ChanNams):
        if i > 1: 
          break  # works for 2 channels only
        self.Vhist[i, k] = dat[i]
        self.d[i] = np.concatenate((self.Vhist[i, k+1:], self.Vhist[i, :k+1]), axis=0)

      if not self.XYmode:       
      # update history graph(s) 
        for i in range(self.NChan):
          if n>1: # !!! fix to avoid permanent display of first object in blit mode
            self.graphs[i].set_data(self.Ti, self.d[i])
      else:
      # update XY display 
          if self.XYmode:
            self.graphs[-1].set_data( self.d[0], self.d[1])
    return self.graphs
#- -end def DataLogger.__call__
#-end class DataLogger
