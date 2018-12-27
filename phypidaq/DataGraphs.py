# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import time, numpy as np
import matplotlib.pyplot as plt

class DataGraphs(object):
  ''' Bar graph display, history plot and XY-display

         forked from picoDAQ.DataGraphs
  '''

  def __init__(self, ConfDict):
    '''Args:   confDict: Configuration dictionary
    '''
 
   # get relevant settings from PhyPiConfDict
    self.dT = ConfDict['Interval'] 
    self.NChan = ConfDict['NChannels']
    self.ChanLim = ConfDict['ChanLimits']
    
    if 'Title' in ConfDict:
     self.Title = ConfDict['Title']
    else:
     self.Title= 'Voltmeter'

    Nc = self.NChan
    self.ChanNams = [''] * Nc
    if 'ChanNams' in ConfDict:
      v = ConfDict['ChanNams']
      self.ChanNams[ 0 : min(len(v),Nc)] = v[0 : min(len(v),Nc)]
      
    ColorList=['C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12'] 
    if 'ChanColors' in ConfDict:
      self.ChanColors = ConfDict['ChanColors']
      if len(self.ChanColors) < Nc:
        self.ChanColors += ColorList[0: Nc - len(self.ChanColors)]
    else:
      self.ChanColors = ['darkblue','sienna'] + ColorList[0 : Nc]

    self.ChanLabels = [''] * Nc
    if 'ChanLabels' in ConfDict:
      v = ConfDict['ChanLabels']
      self.ChanLabels[0: min(len(v),Nc)] = v[0: min(len(v),Nc)] 

    self.ChanUnits = [''] * Nc
    if 'ChanUnits' in ConfDict:
      v = ConfDict['ChanUnits']
      self.ChanUnits[0: min(len(v),Nc)] = v[0:min(len(v),Nc)]

    if 'XYmode' in ConfDict:
      self.XYmode = ConfDict['XYmode']
    else:
      self.XYmode = False
    if Nc < 2: 
      self.XYmode = False

# assign Channels to Axes
    self.NAxes = min(2, len(self.ChanLabels))
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
    cu0= self.ChanUnits[self.Cidx0]
    cu1= self.ChanUnits[self.Cidx1]
    if cu0: cu0 = ' ('+ cu0 +')'
    if cu1: cu1 = ' ('+ cu1 +')'
    self.AxisLabels = [self.ChanLabels[self.Cidx0] + cu0, 
                       self.ChanLabels[self.Cidx1] + cu1 ]

    # define xy plots
    if 'xyPlots' in ConfDict:
      self.xyPlots = ConfDict['xyPlots']
    else:
      # plot chan1 vs. chan0, chan2 vs. chan0, ..., last chan vs cha0
      self.xyPlots = [ [0,i] for i in range(1,Nc)]
    
# config data needed throughout the class
    self.Npoints = 120  # number of points for history
    self.Ti = self.dT* np.linspace(-self.Npoints+1, 0, self.Npoints) 
    self.bwidth = 0.5   # width of bars
    self.ind = self.bwidth + np.arange(Nc) # bar position
  # 
    self.Vhist = np.zeros( [Nc, self.Npoints] )
    self.d = np.zeros( [Nc, self.Npoints] ) 

# set up a figure to plot voltage(s)
    if self.XYmode:
      fig = plt.figure("DataGraphs", figsize=(10., 5.5) )
      fig.subplots_adjust(left=0.09, bottom=0.1, right=0.975, top=0.94,
                          wspace=3.5, hspace=.25)
    else:
      fig = plt.figure("DataGraphs", figsize=(4., 5.3) )
      fig.subplots_adjust(left=0.2, bottom=0.1, right=0.8, top=0.94,
                  wspace=None, hspace=.25)

    axes=[]
    if not self.XYmode:  # only history plot
      axes.append(plt.subplot2grid((6,1),(4,0), rowspan=2) )
    else:                # also include XY display
      axes.append(plt.subplot2grid((6,5),(4,0), rowspan=2, colspan=2) )
    if self.NAxes > 1:
      axes.append(axes[0].twinx())

    # history plot
    for i in range(self.NAxes):
      Cidx = self.Chan2Axes.index(i)
      axes[i].set_ylim(*self.ChanLim[Cidx])
      axes[i].set_ylabel(self.ChanNams[Cidx] + ' ' + self.AxisLabels[i],
                           color=self.ChanColors[Cidx])
      axes[i].grid(True, color=self.ChanColors[Cidx], linestyle = '--', alpha=0.3)
    axes[0].set_xlabel('History (s)', size='x-large')

    if self.XYmode:
      axes.append(plt.subplot2grid((6,5),(1,0), rowspan=3, colspan=2) )
    else:
      axes.append(plt.subplot2grid((6,1),(1,0), rowspan=3) )

    axbar = []
  # barchart
    axbar.append(axes[-1])
    axbar[0].set_frame_on(False)
    axbar[0].get_xaxis().set_visible(False)
    axbar[0].set_xlim(0., Nc)
    axbar[0].axvline(0, color = self.ChanColors[0])
    axbar[0].set_ylim(*self.ChanLim[0])
    axbar[0].axhline(0., color='k', linestyle='-', lw=2, alpha=0.5)
    axbar[0].set_ylabel(self.ChanNams[0] + ' ' + self.AxisLabels[0],
                      size='x-large',  color = self.ChanColors[0])
    axbar[0].grid(True, color=self.ChanColors[0], linestyle = '--', alpha=0.3)
    if self.NAxes > 1:
      axbar.append(axbar[0].twinx() )
      axbar[1].set_frame_on(False)
      Cidx = self.Chan2Axes.index(1)
      axbar[1].axvline(Nc, color = self.ChanColors[1])
      axbar[1].set_ylim(*self.ChanLim[Cidx])
      axbar[1].set_ylabel(self.ChanNams[Cidx] + ' ' + self.AxisLabels[1],
                          size='x-large', color = self.ChanColors[Cidx])
      axbar[1].grid(True, color=self.ChanColors[Cidx], 
                    linestyle = '--', alpha=0.3)
  # Voltage in Text format
    if self.XYmode:
      axes.append(plt.subplot2grid((6,5), (0,0), rowspan=1, colspan=2) )
    else:
      axes.append(plt.subplot2grid((6,1), (0,0)) )
    axtxt=axes[-1]
    axtxt.set_frame_on(False)
    axtxt.get_xaxis().set_visible(False)
    axtxt.get_yaxis().set_visible(False)
    axtxt.set_title(self.Title, size='xx-large')

  # XY display
    if self.XYmode:
      axes.append(plt.subplot2grid((6,5),(0,2), rowspan=6, colspan=3) )
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
    else:
      axXY = None

    self.fig = fig
    self.axes = axes
    self.axbar = axbar
    self.axtxt = axtxt
    self.axXY = axXY
# -- end def grVMeterIni

  def init(self):
  # initialize objects to be animated

  # bar graph for voltages
    self.bgraphs = ()
    for i in range(self.NChan):
      iax = self.Chan2Axes[i]
      bg, = self.axbar[iax].bar(self.ind[i], 0. , self.bwidth,
            align='center', color = self.ChanColors[i], alpha=0.5) 
      self.bgraphs += (bg,)

  # history graphs
    self.graphs=()
    for i in range(self.NChan):
      iax = self.Chan2Axes[i]
   # intitialize with graphs outside range
      offset = self.ChanLim[i][0] - 0.1*(self.ChanLim[i][1] - self.ChanLim[i][0]) 
      g, = self.axes[iax].plot(self.Ti, offset*np.ones(self.Npoints), 
                              color=self.ChanColors[i])
      self.graphs += (g,)

  # Voltage in Text form
    self.animtxt = self.axtxt.text(0.01, 0.025 , ' ', size='large',
              transform=self.axtxt.transAxes,
              color='darkblue')
  
    self.XYgraphs = ()
    if self.XYmode:
      # plot XY-graph(s)
      for i in range(len(self.xyPlots)):
        cy = self.xyPlots[i][1]
        XYg, = self.axes[-1].plot( [0.], [0.], color=self.ChanColors[cy] )
        self.XYgraphs += (XYg,)

    self.t0=time.time() # remember start time

    return self.bgraphs + self.graphs + self.XYgraphs + (self.animtxt,)  
# -- end DataGraphs.init()

  def __call__( self, data ):
    # update graphics with actual data
    if data != None: 
      n, dat = data
      if n == 0:
        return self.init()

      k = n % self.Npoints
      txt=''
      for i in range(self.NChan):
        self.Vhist[i, k] = dat[i]
    # update history graph
        self.d[i] = np.concatenate((self.Vhist[i, k+1:], self.Vhist[i, :k+1]), axis=0)
        if n > 1: # !!! fix to avoid permanent display of first object in blit mode
          self.graphs[i].set_data(self.Ti, self.d[i])
    # update text display
          if i%2:
            bgn = '  ' 
            end = '\n'
          else:
            bgn = ''
            end = ''
          txt += bgn + '%s: % #.4g%s'% (self.ChanNams[i], self.Vhist[i,k], 
            self.ChanUnits[i]) + end 
    # update bar chart
          self.bgraphs[i].set_height(dat[i])
          self.animtxt.set_text(txt)
      if self.XYmode:
    # update XY display 
        for i in range(len(self.xyPlots)):
          cx = self.xyPlots[i][0]
          cy = self.xyPlots[i][1]            
          self.XYgraphs[i].set_data( self.d[cx], self.d[cy])
    # -- end if != None
    return self.bgraphs + self.graphs + self.XYgraphs + (self.animtxt,)  
#- -end def DataGraphs.__call__
#-end class DataGraphs
