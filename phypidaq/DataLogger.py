from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import numpy as np, matplotlib.pyplot as plt

class DataLogger(object):
  ''' history of input data

    forked from picoDAQ.DataLogger
  '''

  def __init__(self, ConfDict, sigName):
    '''Args:  Wtime: waiting time between updates
              conf: PicoScope Configuration dictionary
    '''
   # collect relevant configuration parameters
    self.Npoints = 120  # number of points for history

   # get relevant settings from PhyPiConfDict
    self.dT = ConfDict['Interval'] 
    self.NChan = ConfDict['NChannels']
    self.ChanLim = ConfDict['ChanLimits']
    self.ChanNams = ConfDict['ChanNams']
    self.ChanColors = ConfDict['ChanColors']

   # data structures needed throughout the class
    self.Ti = self.dT* np.linspace(-self.Npoints+1, 0, self.Npoints) 
    self.Vhist = np.zeros( [self.NChan, self.Npoints] )

# set up a figure to plot actual voltage and samplings from Picoscope
    fig = plt.figure("DataLogger", figsize=(6., 3.) )
    fig.subplots_adjust(left=0.15, bottom=0.2, right=0.85, top=0.95,
                  wspace=None, hspace=.25)
    axes=[]
  # history plot
    axes.append(fig.add_subplot(1,1,1, facecolor='ivory'))
    if self.NChan > 1:
      axes.append(axes[0].twinx())
    for i, C in enumerate(self.ChanNams):
      if i > 1:
        break # works for a maximum of 2 Channels only
      axes[i].set_ylim(*self.ChanLim[i])
      axes[i].set_ylabel('Chan ' + C + ' ' + sigName, color=self.ChanColors[i])
      axes[i].grid(True, color=self.ChanColors[i], linestyle = '--', alpha=0.3)
    axes[0].set_xlabel('History (s)')

    self.fig = fig
    self.axes = axes
# -- end def __init__

  def init(self):
  # initialize objects to be animated

  # history graphs
    self.graphs=()
    for i, C in enumerate(self.ChanNams):
      if i > 1:
        break  # max. of 2 channels
   # intitialize with graph outside range
      g,= self.axes[i].plot(self.Ti, 
          self.ChanLim[i][1] * 1.1 * np.ones(self.Npoints), 
          color=self.ChanColors[i])
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
    # update history graph
        if n>1: # !!! fix to avoid permanent display of first object in blit mode
          self.graphs[i].set_data(self.Ti,
            np.concatenate((self.Vhist[i, k+1:], self.Vhist[i, :k+1]), axis=0) )

    return self.graphs
#- -end def DataLogger.__call__
#-end class DataLogger
