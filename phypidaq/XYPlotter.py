# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import time, numpy as np
import matplotlib.pyplot as plt

class XYPlotter(object):
  ''' Bar graph display of average over samples 

    forked from picoDAQ.DataGraphs
  '''

  def __init__(self, ConfDict, sigName):
    '''Args:   Wtime: waiting time between updates
               confDict: PicoScope Configuration dictionary
               XYmode: bool, xy-display if True
    '''
 
  # collect relevant configuration parameters
    self.Npoints = 120  # number of points for history
    self.bwidth = 0.5   # width of bars

   # get relevant settings from PhyPiConfDict
    self.dT = ConfDict['Interval'] 
    self.NChan = ConfDict['NChannels']
    self.ChanLim = ConfDict['ChanLimits']
    self.ChanNams = ConfDict['ChanNams']
    self.ChanColors = ConfDict['ChanColors']
    self.XYmode = ConfDict['XYmode']
    self.sigName = sigName
    if self.NChan < 2: 
      self.XYmode = True

   # data structures needed throughout the class
    self.Ti = self.dT* np.linspace(-self.Npoints+1, 0, self.Npoints) 
    self.ind = self.bwidth + np.arange(self.NChan) # bar position for voltages
  # 
    self.Vhist = np.zeros( [self.NChan, self.Npoints] )
    self.d = np.zeros( [self.NChan, self.Npoints] ) 

# set up a figure to plot actual voltage and samplings from Picoscope
    if self.XYmode:
      fig = plt.figure("DataGraphs", figsize=(10., 5.5) )
      fig.subplots_adjust(left=0.09, bottom=0.1, right=0.975, top=0.94,
                          wspace=3.5, hspace=.25)
    else:
      fig = plt.figure("DataGraphs", figsize=(4., 5.3) )
      fig.subplots_adjust(left=0.2, bottom=0.08, right=0.8, top=0.94,
                  wspace=None, hspace=.25)

    axes=[]

  # history plot
    if self.XYmode:
      axes.append(plt.subplot2grid((6,5),(4,0), rowspan=2, colspan=2) )
    else:
      axes.append(plt.subplot2grid((6,1),(4,0), rowspan=2) )
    if self.NChan > 1:
      axes.append(axes[0].twinx())

    for i, C in enumerate(self.ChanNams):
      if i > 1:
        break # works for a maximum of 2 Channels only
      axes[i].set_ylim(*self.ChanLim[i])
      axes[i].set_ylabel('Chan ' + C + ' ' + '(' + sigName[i] +')', color=self.ChanColors[i])
      axes[i].grid(True, color=self.ChanColors[i], linestyle = '--', alpha=0.3)
    axes[0].set_xlabel('History (s)', size='x-large')

  # barchart
    if self.XYmode:
      axes.append(plt.subplot2grid((6,5),(1,0), rowspan=3, colspan=2) )
    else:
      axes.append(plt.subplot2grid((6,1),(1,0), rowspan=3) )
    axbar1 = axes[-1]
    axbar1.set_frame_on(False)
    if self.NChan > 1:
      axbar2=axbar1.twinx()
      axbar2.set_frame_on(False)
    axbar1.get_xaxis().set_visible(False)
    axbar1.set_xlim(0., self.NChan)
    axbar1.axvline(0, color = self.ChanColors[0])
    if self.NChan > 1:
      axbar1.axvline(self.NChan, color = self.ChanColors[1])
    axbar1.set_ylim(*self.ChanLim[0])
    axbar1.axhline(0., color='k', linestyle='-', lw=2, alpha=0.5)
    axbar1.set_ylabel('Chan ' + self.ChanNams[0] + ' ' + '(' + sigName[0] + ')', size='x-large', 
       color = self.ChanColors[0])
    axbar1.grid(True, color=self.ChanColors[0], linestyle = '--', alpha=0.3)
    if self.NChan > 1:
      axbar2.set_ylim(*self.ChanLim[1])
      axbar2.set_ylabel('Chan ' + self.ChanNams[1] + ' ' + '(' + sigName[1] + ')', size='x-large', 
          color = self.ChanColors[1])
      axbar2.grid(True, color=self.ChanColors[0], linestyle = '--', alpha=0.3)

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
      axXY.set_xlabel('Chan '+self.ChanNams[0]+' ' + '(' + sigName[0] +')', 
         size='x-large', color=self.ChanColors[0])
      axXY.set_ylabel('Chan '+self.ChanNams[1]+ ' ' + '(' + sigName[1] + ')', 
         size='x-large', color=self.ChanColors[1])
      axXY.set_title('XY-View', size='xx-large')
      axXY.grid(True, color='grey', linestyle = '--', alpha=0.3)
    else:
      axXY = None

    self.fig = fig
    self.axes = axes
    self.axbar1 = axbar1
    if self.NChan > 1:
      self.axbar2 = axbar2
    self.axtxt = axtxt
    self.axXY = axXY
# -- end def grVMeterIni

  def init(self):
  # initialize objects to be animated

  # a bar graph for the actual voltages
    self.bgraph1, = self.axbar1.bar(self.ind[0], 0. , self.bwidth,
       align='center', color = self.ChanColors[0], alpha=0.5) 
    if self.NChan > 1:
      self.bgraph2, = self.axbar2.bar(self.ind[1], 0. , self.bwidth,
          align='center', color = self.ChanColors[1], alpha=0.5) 
  # history graphs
    self.graphs=()
    for i, C in enumerate(self.ChanNams):
      if i > 1:
        break  # max. of 2 channels
      g,= self.axes[i].plot(self.Ti, np.zeros(self.Npoints), 
          color=self.ChanColors[i])
      self.graphs += (g,)
    self.animtxt = self.axtxt.text(0.01, 0.05 , ' ',
              transform=self.axtxt.transAxes,
              size='large', color='darkblue')
  
    if self.XYmode:
      g, = self.axXY.plot([0.], [0.], color='firebrick')
      self.graphs += (g,)

    self.t0=time.time() # remember start time

    if self.NChan > 1 :
      return (self.bgraph1,) + (self.bgraph2,) + self.graphs + (self.animtxt,)  
    else:
# -- end DataGraphs.init()
      return (self.bgraph1,) + self.graphs + (self.animtxt,)  

  def __call__( self, data ):
    # update graphics with actual data
    if data != None: 
      n, dat = data
      if n == 0:
        return self.init()

      k = n % self.Npoints
      txt=[]
      for i, C in enumerate(self.ChanNams):
        if i > 1: 
          break  # works for 2 channels only
        self.Vhist[i, k] = dat[i]
    # update history graph
        if n>1: # !!! fix to avoid permanent display of first object in blit mode
          self.d[i] = np.concatenate((self.Vhist[i, k+1:], self.Vhist[i, :k+1]), axis=0)
          self.graphs[i].set_data(self.Ti, self.d[i])
          if self.XYmode:
            self.graphs[-1].set_data(self.d[0], self.d[1])
        txt.append('  %s:   %.3g %s' % (C, self.Vhist[i,k], self.sigName[i]) )
    # update bar chart
      if n>1: # !!! fix to avoid permanent display of first object in blit mode
        self.bgraph1.set_height(dat[0])
        if self.NChan > 1:
          self.bgraph2.set_height(dat[1])
      else:  
        self.bgraph1.set_height(0.)
        if self.NChan > 1:
          self.bgraph2.set_height(0.)

      if self.NChan > 1:
        self.animtxt.set_text(txt[0] + '\n' + txt[1])
      else:
        self.animtxt.set_text(txt[0])
     # -- end if != None

    if self.NChan > 1 :
      return (self.bgraph1,) + (self.bgraph2,) + self.graphs + (self.animtxt,)
    else:
      return (self.bgraph1,) + self.graphs + (self.animtxt,)
#- -end def DataGraphs.__call__
#-end class VoltMeter
