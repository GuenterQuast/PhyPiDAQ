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

# assign Channels to Axes
    self.NAxes = min(2, len(self.ChanLabels))
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

# config data needed throughout the class
    self.Npoints = 120  # number of points for history
    self.Ti = self.dT* np.linspace(-self.Npoints+1, 0, self.Npoints) 
    self.bwidth = 0.5   # width of bars
    self.ind = self.bwidth + np.arange(self.NChan) # bar position
  # 
    self.Vhist = np.zeros( [self.NChan, self.Npoints] )
    self.d = np.zeros( [self.NChan, self.Npoints] ) 

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
      axes[i].set_ylabel('Chan ' + self.ChanNams[Cidx] + ' ' + self.AxisLabels[i],
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
    axbar[0].set_xlim(0., self.NChan)
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
      axbar[1].axvline(self.NChan, color = self.ChanColors[1])
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
    axtxt.set_title('Voltmeter', size='xx-large')

  # XY display
    if self.XYmode:
      axes.append(plt.subplot2grid((6,5),(0,2), rowspan=6, colspan=3) )
      axXY = axes[-1]
      axXY.set_xlim(*self.ChanLim[self.Cidx0])
      axXY.set_ylim(*self.ChanLim[self.Cidx1])
      axXY.set_xlabel('Chan ' + self.ChanNams[self.Cidx0] + ' ' + self.AxisLabels[0], 
         size='x-large', color=self.ChanColors[self.Cidx0])
      axXY.set_ylabel('Chan ' + self.ChanNams[self.Cidx1] + ' ' + self.AxisLabels[1], 
         size='x-large', color=self.ChanColors[self.Cidx1])
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
    self.animtxt = self.axtxt.text(0.01, 0.025 , ' ',
              transform=self.axtxt.transAxes,
              color='darkblue')
  
    self.XYgraphs = ()
    if self.XYmode:
      # plot XY-graph(s)
      for i in range(1, self.NChan):
        XYg, = self.axes[-1].plot( [0.], [0.], color=self.ChanColors[i] )
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
    # update XY display
          if self.XYmode and i>0:
            self.XYgraphs[i-1].set_data(self.d[0], self.d[i]) 
    # update text display
          endl = ''
          if i%2: endl = '\n'
          txt += '  %s:   %.3g %s'% (self.ChanNams[i], self.Vhist[i,k], self.ChanUnits[i]) + endl 
    # update bar chart
          self.bgraphs[i].set_height(dat[i])
          self.animtxt.set_text(txt)
    # -- end if != None
    return self.bgraphs + self.graphs + self.XYgraphs + (self.animtxt,)  
#- -end def DataGraphs.__call__
#-end class DataGraphs
