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

   # get relevant settings from PhyPiConfDict
    self.dT = ConfDict['Interval'] 

   # number of points for history
    if 'NHistoryPoints' in ConfDict:
      self.Npoints = min(ConfDict['NHistoryPoints'], 250)
    else:
      self.Npoints = 120

    self.NChan = ConfDict['NChannels']

    self.ChanLim = ConfDict['ChanLimits']

    Nc = self.NChan
    self.ChanNams = [''] * self.NChan 
    if 'ChanNams' in ConfDict:
      v = ConfDict['ChanNams']
      self.ChanNams[0:min(len(v),Nc)] = v[0:min(len(v),Nc)]      
      
    ColorList=['C'+str(i) for i in range(Nc)] 
    if 'ChanColors' in ConfDict:
      self.ChanColors = ConfDict['ChanColors']
      if len(self.ChanColors) < self.NChan:
        self.ChanColors += ColorList[0: self.NChan - len(self.ChanColors)]
    else:
      self.ChanColors = ['darkblue','sienna'] + ColorList[0 : Nc-2]

    # Channel Labels are not shown, only support two axis labels
    self.ChanLabels = [''] * self.NChan
    if 'ChanLabels' in ConfDict:
      v = ConfDict['ChanLabels']
      self.ChanLabels[0:min(len(v),Nc)] = v[0:min(len(v),Nc)]      

    self.ChanUnits = [''] * Nc
    if 'ChanUnits' in ConfDict:
      v = ConfDict['ChanUnits']
      self.ChanUnits[0:min(len(v),Nc)] = v[0:min(len(v),Nc)]      

    if 'XYmode' in ConfDict:
      self.XYmode = ConfDict['XYmode']
    else:
      self.XYmode = False
    if Nc < 2: 
      self.XYmode = False

    # assign Channels to axes
    self.NAxes = min(2, Nc)
    if 'Chan2Axes' in ConfDict:
      self.Chan2Axes = ConfDict['Chan2Axes']
    else:
    # default: 0 -> ax0, >0 -> ax2 
      self.Chan2Axes = [0] + [self.NAxes-1] * (Nc - 1)
    self.Cidx0 = self.Chan2Axes.index(0)  # 1st Channel axis0
    try:
      self.Cidx1 = self.Chan2Axes.index(1)    # 1st Channel axis1
    except:
      self.NAxes = 1
      self.Cidx1 = self.Cidx0
    cu0= '('+self.ChanUnits[self.Cidx0]+')' if self.ChanUnits[self.Cidx0] else ''
    cu1= '('+self.ChanUnits[self.Cidx1]+')' if self.ChanUnits[self.Cidx1] else ''
    self.AxisLabels = [self.ChanLabels[self.Cidx0] + cu0, 
                       self.ChanLabels[self.Cidx1] + cu1 ]

    # define xy plots
    if 'xyPlots' in ConfDict:
      self.xyPlots = ConfDict['xyPlots']
    else:
      # plot chan1 vs. chan0, chan2 vs. chan0, ..., last chan vs cha0
      self.xyPlots = [ [0,i] for i in range(1,Nc)]

    self.graphs_initialized = False
    
    # data structures needed throughout the class
    self.Vhist = np.zeros( [Nc, self.Npoints] )
    self.h = np.zeros( [Nc, self.Npoints] ) 


# create matplotlib figure object
    if self.XYmode:
      self.fig = plt.figure("DataLogger", figsize=(6.3, 6.) )
      self.fig.subplots_adjust(left=0.2, bottom=0.15, right=0.95, top=0.95,
                  wspace=None, hspace=.25)
    else:
      self.fig = plt.figure("DataLogger", figsize=(6., 3.) )
      self.fig.subplots_adjust(left=0.15, bottom=0.15, right=0.85, top=0.95,
                  wspace=None, hspace=.25)
# -- end def __init__()

  def initgraph(self, NPoints):
    fig=self.fig
    # set-up figure axes
    self.get_Ti(NPoints)
    axes=[]
    if not self.XYmode:
  # history plot
      axes.append(fig.add_subplot(1,1,1, facecolor='ivory', label='history'))
      if self.NAxes > 1:
        axes.append(axes[0].twinx())
      for i in range(self.NAxes):
        Cidx = self.Chan2Axes.index(i)
        axes[i].set_xlim(self.Ti[0], self.Ti[-1])
        axes[i].set_ylim(*self.ChanLim[Cidx])
        axes[i].set_ylabel(self.ChanNams[Cidx] + ' ' + self.AxisLabels[i], 
                           color=self.ChanColors[Cidx])
        axes[i].grid(True, color=self.ChanColors[Cidx], linestyle = '--', alpha=0.3)
      axes[0].set_xlabel('History (' + self.tUnit + ')')
      axes[0].axvline(0., color = 'yellow', alpha=0.5, lw=5) # highlight t=0

    else:
  # XY plot
      axes.append(fig.add_subplot(1,1,1, facecolor='ivory', label='xy'))
      axXY = axes[-1]
      cx = self.xyPlots[0][0]
      cy = self.xyPlots[0][1]
      axXY.set_xlim(*self.ChanLim[cx])
      axXY.set_ylim(*self.ChanLim[cy])
      cux = ' (' + self.ChanUnits[cx]+')'
      cuy = ' (' + self.ChanUnits[cy]+')'
      axXY.set_xlabel(self.ChanNams[cx] + ' ' + self.ChanLabels[cx] + cux, 
                      size='x-large', color=self.ChanColors[cx])
      axXY.set_ylabel(self.ChanNams[cy] + ' ' + self.ChanLabels[cy] + cuy, 
                      size='x-large', color=self.ChanColors[cy])
      axXY.set_title('XY-View', size='xx-large')
      axXY.grid(True, color='grey', linestyle = '--', alpha=0.3)
  
    self.graphs_initialized = True     
    self.axes = axes
# -- end def initgraph()

  def get_Ti(self, NPoints):
  # determine points on time-axis  
    if self.dT < 60:
      self.tUnit = 's'
      self.tUnitFactor = 1.
    elif self.dT < 3600:
      self.tUnit = 'min'
      self.tUnitFactor = 1./60.
    else:
      self.tUnit = 'h'
      self.tUnitFactor = 1./3600.
    self.Ti = self.dT * np.linspace(-NPoints+1, 0, NPoints) * self.tUnitFactor

  def init(self, NPoints=None):
  # initialize objects to be animated
    if NPoints==None: NPoints=self.Npoints
    if not self.graphs_initialized:
      self.initgraph(NPoints) # create matplotlib figure
    
    self.graphs=()
  # history graphs
    if not self.XYmode:
      for i in range(self.NChan):
        iax = self.Chan2Axes[i]
        if i >= len(self.ChanColors): 
          colr = None
        else:
          colr = self.ChanColors[i]
        g,= self.axes[iax].plot([], [], color= colr)
        self.graphs += (g,)
    else:
      # plot XY-graph(s)
      for i in range(len(self.xyPlots)):
        cx = self.xyPlots[i][0]
        cy = self.xyPlots[i][1]
        if cx < self.NChan and cy < self.NChan:
          g, = self.axes[-1].plot( [], [], color=self.ChanColors[cy] )
          self.graphs += (g,)
    return self.graphs
# -- end DataLogger.init()

  def __call__( self, data ):
    # add data for last point in time (for animated plot)
    if data !=None: 
      n, dat = data

      k = (n-1) % self.Npoints
      for i in range(self.NChan):
        self.Vhist[i, k] = dat[i]
        self.h[i] = np.concatenate((self.Vhist[i, k+1:], 
                                    self.Vhist[i, :k+1]), axis=0)
      if not self.XYmode:       
      # update history graph(s) 
        for i in range(self.NChan):
          #if n>1: # !!! fix to avoid permanent display of first object in blit mode
          self.graphs[i].set_data(self.Ti, self.h[i])
      else:
      # update XY display 
        for i in range(len(self.graphs)):
          cx = self.xyPlots[i][0]
          cy = self.xyPlots[i][1]  
          i1 = max(0, self.Npoints - n)           
          self.graphs[i].set_data( self.h[cx, i1:],
                                     self.h[cy, i1:] )
    return self.graphs
  #- -end def DataLogger.__call__

  def plotall( self, dat ):
    # plot data for all points in time at once (not for animation)
    if not self.XYmode:       
    # update history graph(s) 
      for i in range(self.NChan):
        self.graphs[i].set_data(self.Ti, dat[i])
    else:
    # update XY display 
      for i in range(len(self.graphs)):
        cx = self.xyPlots[i][0]
        cy = self.xyPlots[i][1]  
        self.graphs[i].set_data( dat[cx], dat[cy] )
    return self.graphs
  #- -end def DataLogger.plotall()

#-end class DataLogger
