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
    ColorList=['C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12'] 
    if 'ChanColors' in ConfDict:
      self.ChanColors = ConfDict['ChanColors']
      if len(self.ChanColors) < self.NChan:
        self.ChanColors += ColorList[0: self.NChan - len(self.ChanColors)]
    else:
      self.ChanColors = ['darkblue','sienna'] + ColorList[0 : self.NChan]

    # Channel Labels are not shown, only support two axis labels
    if 'ChanLabels' in ConfDict:
      self.ChanLabels = ConfDict['ChanLabels']
    else:
      self.ChanLabels = [''] * self.NChan

    if 'ChanUnits' in ConfDict:
      self.ChanUnits = ConfDict['ChanUnits']
    else:
      self.ChanUnits = [''] * self.NChan

    if 'XYmode' in ConfDict:
      self.XYmode = ConfDict['XYmode']
    else:
      self.XYmode = False
    if self.NChan < 2: 
      self.XYmode = False

    # assign Channels to axes
    self.NAxes = min(2, self.NChan)
    if 'Chan2Axes' in ConfDict:
      self.Chan2Axes = ConfDict['Chan2Axes']
    else:
    # default: 0 -> ax0, >0 -> ax2 
      self.Chan2Axes = [0] + [self.NAxes-1] * (self.NChan - 1)
    self.Cidx0 = self.Chan2Axes.index(0)  # 1st Channel axis0
    try:
      self.Cidx1 = self.Chan2Axes.index(1)    # 1st Channel axis1
    except:
      self.NAxes = 1
      self.Cidx1 = self.Cidx0
    self.AxisLabels = [self.ChanLabels[self.Cidx0] + ' ('+self.ChanUnits[self.Cidx0]+')', 
                       self.ChanLabels[self.Cidx1] + ' ('+self.ChanUnits[self.Cidx1]+')']

   # data structures needed throughout the class
    self.Ti = self.dT* np.linspace(-self.Npoints+1, 0, self.Npoints) 
    self.Vhist = np.zeros( [self.NChan, self.Npoints] )
    self.d = np.zeros( [self.NChan, self.Npoints] ) 

# set up a figure to plot actual voltage(s)
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
      if self.NAxes > 1:
        axes.append(axes[0].twinx())
      for i in range(self.NAxes):
        Cidx = self.Chan2Axes.index(i)
        axes[i].set_ylim(*self.ChanLim[Cidx])
        axes[i].set_ylabel('Chan ' + self.ChanNams[Cidx] + ' ' + self.AxisLabels[i], 
                           color=self.ChanColors[Cidx])
        axes[i].grid(True, color=self.ChanColors[Cidx], linestyle = '--', alpha=0.3)
      axes[0].set_xlabel('History (s)')
    else:
  # XY plot
      axes.append(fig.add_subplot(1,1,1, facecolor='ivory'))
      axXY = axes[-1]
      axXY.set_xlim(*self.ChanLim[self.Cidx0])
      axXY.set_ylim(*self.ChanLim[self.Cidx1])
      axXY.set_xlabel('Chan ' + self.ChanNams[self.Cidx0] + ' ' + self.AxisLabels[0], 
                      size='x-large', color=self.ChanColors[self.Cidx0])
      axXY.set_ylabel('Chan ' + self.ChanNams[self.Cidx1] + ' ' + self.AxisLabels[1], 
                      size='x-large', color=self.ChanColors[self.Cidx1])
      axXY.set_title('XY-View', size='xx-large')
      axXY.grid(True, color='grey', linestyle = '--', alpha=0.3)
  
    self.fig = fig
    self.axes = axes
# -- end def __init__

  def init(self):
  # initialize objects to be animated

    self.graphs=()
  # history graphs
    if not self.XYmode:
      for i in range(self.NChan):
        iax = self.Chan2Axes[i]
        if i >= len(self.ChanColors): 
          colr = None
        else:
          colr = self.ChanColors[i]
   # intitialize with graph outside range
        g,= self.axes[iax].plot(self.Ti, 
                      self.ChanLim[iax][1] * 1.1 * np.ones(self.Npoints), color= colr)
        self.graphs += (g,)
    else:
      # plot XY-graph(s)
      for i in range(1, self.NChan):
        g, = self.axes[-1].plot( [0.], [0.], color=self.ChanColors[i] )
        self.graphs += (g,)

    return self.graphs
# -- end DataLogger.init()

  def __call__( self, data ):

    if data !=None: 
      n, dat = data

      k = n % self.Npoints
      for i in range(self.NChan):
        self.Vhist[i, k] = dat[i]
        self.d[i] = np.concatenate((self.Vhist[i, k+1:], 
                                    self.Vhist[i, :k+1]), axis=0)
      if not self.XYmode:       
      # update history graph(s) 
        for i in range(self.NChan):
          if n>1: # !!! fix to avoid permanent display of first object in blit mode
            self.graphs[i].set_data(self.Ti, self.d[i])
      else:
      # update XY display 
          if self.XYmode:
            for i in range(1, self.NChan):
                self.graphs[i-1].set_data( self.d[0], self.d[i])
    return self.graphs
#- -end def DataLogger.__call__
#-end class DataLogger
