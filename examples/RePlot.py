#!/usr/bin/python3
# -*- coding: utf-8 -*-
''' script RePlot.py
    usage: RePlot.py [filename] [[channel numbers]]

    Read data exported by run_phypi.py and show plot   
'''

from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import numpy as np, time, sys, os
import matplotlib.pyplot as plt, numpy as np

if len(sys.argv)>=2:
  fnam = sys.argv[1]
else:
  fnam = "PhyPiData.csv"
print('*==* ', sys.argv[0], ' Lese Daten aus Datei', fnam)

Channels=[]   
if len(sys.argv)>=3:
  for i in range(len(sys.argv)-2):
    Channels.append(int(sys.argv[i+2]))

# read data from file
f = open(fnam)
txtdata = f.read().splitlines()
f.close

# read and analyze header
h0 = txtdata[0][2:] # remove leading '#'
h1 = txtdata[1][2:]
h2 = txtdata[2][2:]
dT = float(h1.split(' ')[-1])
tags = h2.split(',')
# read data part 
data = np.loadtxt(txtdata, dtype=np.float32,
                           delimiter=',',
                           unpack=True)    
Ndat = len(data[0])   # number of data points in file

print('Data set header:')
print(h0)
print(h1)
print(h2)
print('Data set info:')
print('  columns: ', len(tags), '  data points: ', Ndat)
print('\ngenerating graph ...')

# check if only selected channels wanted
if len(Channels)==0:
  NChannels = len(tags)
  Channels = range(NChannels)
else:
  NChannels = len(Channels)
  
# create a figure
fig = plt.figure("PhyPiData", figsize=(6., 3.) )
fig.subplots_adjust(left=0.15, bottom=0.15, right=0.85, top=0.95,
                  wspace=None, hspace=.25)
axes = []
axes.append(fig.add_subplot(1,1,1, facecolor='ivory'))                 
if NChannels > 1:                 
  axes.append(axes[0].twinx())                 
Naxes = len(axes)
ChanColors = ['darkblue', 'sienna'] + ['C'+str(i) for i in range(NChannels-2)] 
                 
if dT < 60:
  tUnit = 's'
  tUnitFactor = 1.
elif dT < 3600:
  tUnit = 'min'
  tUnitFactor = 1./60.
else:
  tUnit = 'h'
  tUnitFactor = 1./3600.
Ti = dT * np.linspace(-Ndat+1, 0, Ndat)*tUnitFactor

# find suitable plot ranges
def getlims(mn0, mx0):
  # general algorithm to find y-range for plotting
  if mn0 < 0.: mn = 1.05 * mn0
  else: mn = 0.95 * mn0 
  if mx0 < 0.: mx = 0.95 * mx0
  else: mx = 1.05 * mx0
  r = mx - mn
  if abs(mn) < 0.05 * r: mn = 0.
  if abs(mx) < 0.05 * r: mx = 0.
  return [mn, mx]

# limits for axes
ylims = []
for i in range(NChannels):
  ic = Channels[i]
  ylims.append(getlims(min(data[ic]), max(data[ic]) ) )  
# channels >1 are mapped to axis 1, find min, max 
ymn0 = ylims[0][0]
ymx0 = ylims[0][1]
if NChannels > 1:
  ymn1 = min(ylims[:][0])
  ymx1 = max(ylims[:][1])
# avoid different axes if limits are close
  yr2 = ymx1 - ymn1
  if abs(ymn1 - ymn0) < 0.1 * yr2:
    ylims[0][0] = min(ymn0, ymn1)
    ylims[1][0] = min(ymn0, ymn1)
  else:
    ylim[1][0] = ymx1  
  if abs(ymx1 - ymx0) < 0.1 * yr2:
    ylims[0][1] = max(ymx0, ymx1)
    ylims[1][1] = max(ymx0, ymx1)
  else:
    ylims[1][1] = ymx1
  
# set options for axes 
for i in range(Naxes):
  axes[i].set_xlim(Ti[0], Ti[-1])
  axes[i].set_ylim( ylims[i][0], ylims[i][1])
  axes[i].set_ylabel(tags[i], color=ChanColors[i])
  axes[i].grid(True, linestyle = '--', alpha=0.3)
axes[0].set_xlabel('History (' + tUnit + ')')

# plot data  
for i in range(NChannels):
  ic = Channels[i]
  if i==0: iax=0
  else: iax=1
  axes[iax].plot(Ti, data[ic], color = ChanColors[i])

plt.show()
