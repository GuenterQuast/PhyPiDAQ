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
    self.ChanNams = ConfDict['ChanNams']
    self.ChanColors = ConfDict['ChanColors']
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
    if self.XYmode and len(self.ChanLabels) < 2:
       print(' *==* DataGraphs: need more than 1 Channel Label in XY mode')
       self.ChanLabels.append('???')

# assign Chanels to Axes
    self.NAxes = min(2, len(self.ChanLabels))
    if 'Chan2Axes' in ConfDict:
      self.Chan2Axis = ConfDict['Chan2Axes']
    else:
    # default: 0 -> ax0, >0 -> ax2 
      self.Chan2Axis = [0] + [self.NAxes-1] * (self.NChan - 1)

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
      fig.subplots_adjust(left=0.2, bottom=0.08, right=0.8, top=0.94,
                  wspace=None, hspace=.25)

    axes=[]
    if not self.XYmode:  # only history plot
      axes.append(plt.subplot2grid((6,1),(4,0), rowspan=2) )
    else:                # also include XY display
      axes.append(plt.subplot2grid((6,5),(4,0), rowspan=2, colspan=2) )
    if self.NAxes > 1:
      axes.append(axes[0].twinx())

    # history plot
    for i, C in enumerate(self.ChanNams):
      if i < self.NAxes:
        axes[i].set_ylim(*self.ChanLim[i])
        axes[i].set_ylabel('Chan ' + C + ' ' + self.ChanLabels[i],
                         color=self.ChanColors[i])
        axes[i].grid(True, color=self.ChanColors[i], linestyle = '--', alpha=0.3)
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
    axbar[0].set_ylabel(self.ChanNams[0] + ' ' + self.ChanLabels[0],
                      size='x-large',  color = self.ChanColors[0])
    axbar[0].grid(True, color=self.ChanColors[0], linestyle = '--', alpha=0.3)
    if self.NAxes > 1:
      axbar.append(axbar[0].twinx() )
      axbar[1].set_frame_on(False)
      axbar[1].axvline(self.NChan, color = self.ChanColors[1])
      axbar[1].set_ylim(*self.ChanLim[1])
      axbar[1].set_ylabel(self.ChanNams[1] + ' ' + self.ChanLabels[1],
                        size='x-large', color = self.ChanColors[1])
      axbar[1].grid(True, color=self.ChanColors[1], linestyle = '--', alpha=0.3)
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
      axXY.set_xlim(*self.ChanLim[0])
      axXY.set_ylim(*self.ChanLim[1])
      axXY.set_xlabel('Chan ' + self.ChanNams[0] + ' ' + self.ChanLabels[0], 
         size='x-large', color=self.ChanColors[0])
      axXY.set_ylabel('Chan ' + self.ChanNams[1] + ' ' + self.ChanLabels[1], 
         size='x-large', color=self.ChanColors[1])
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
    for i, C in enumerate(self.ChanNams):
      iax = self.Chan2Axis[i]
      if i >= len(self.ChanColors): 
        colr = None
      else:
        colr = self.ChanColors[i]
      bg, = self.axbar[iax].bar(self.ind[i], 0. , self.bwidth,
                        align='center', color = colr, alpha=0.5) 
      self.bgraphs += (bg,)

  # history graphs
    self.graphs=()
    for i, C in enumerate(self.ChanNams):
      iax = self.Chan2Axis[i]
      if i >= len(self.ChanColors): 
        colr = None
      else:
        colr = self.ChanColors[i]
   # intitialize with graph outside range
      g,= self.axes[iax].plot(self.Ti, np.zeros(self.Npoints), 
                              color=colr)
      self.graphs += (g,)

  # Voltage in Text form
    self.animtxt = self.axtxt.text(0.01, 0.025 , ' ',
              transform=self.axtxt.transAxes,
              size='large', color='darkblue')
  
    self.XYgraphs = ()
    if self.XYmode:
      # plot XY-graph(s)
      for i in range(1, self.NChan):
        if i >= len(self.ChanColors): 
          colr = None
        else:
          colr = self.ChanColors[i]
        XYg, = self.axes[-1].plot( [0.], [0.], color=colr )
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
      for i, C in enumerate(self.ChanNams):
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
          txt += '  %s:   %.3gV' % (C, self.Vhist[i,k]) + endl 
    # update bar chart
          self.bgraphs[i].set_height(dat[i])
          self.animtxt.set_text(txt)
    # -- end if != None
    return self.bgraphs + self.graphs + self.XYgraphs + (self.animtxt,)  
#- -end def DataGraphs.__call__
#-end class DataGraphs
