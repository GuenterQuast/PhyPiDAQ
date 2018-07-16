# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import numpy as np, time, sys

# import relevant pieces from adafruit
import Adafruit_ADS1x15

class ADS1115Config(object):
  '''ADC ADS1115Config configuration and interface'''

  def __init__(self, confdict = None):
    if confdict==None: confdict={}
    
# -- number of Channels
    if 'NChannels' in confdict:
      self.NChannels = confdict['NChannels']
    else:
      self.NChannels = 1
      
# --  conversion factors for calculation of sensor value
    if "ConvFactors" in confdict:
      self.ConvFactors = confdict["ConvFactors"]
    else:
      self.ConvFactors = [1, 1]
      
# -- sample rate ADC ADS1115
    if "sampleRate" in confdict:
      self.sampleRate = confdict["sampleRate"]
    else:
      self.sampleRate = 860 # sample rate

# -- gain configuration ADC ADS1115
    if "Gain" in confdict:
      self.gain = confdict["Gain"]
      for i in range(self.NChannels):
        if self.gain[i] == '2/3':
          self.gain[i] = 2/3
    else:
      self.gain = [1., 1., 1., 1.]

# -- sample rate configuration of ADC ADS1115
    if "ADCChannels" in confdict:
      self.ADCChannels = confdict["ADCChannels"]  
    else:
      self.ADCChannels = [0, 1, 2, 3]

### --- determine reference voltage for ADC calculation
  # possible values reference voltage
    self.ADCVRef = [6.114, 4.096, 2.048, 1.024, 0.512, 0.256]
  # determine the corresponding index
    self.VRef = [0., 0., 0., 0.]
    self.posGain = [2/3, 1, 2 , 4, 8, 16]
    for i in range(self.NChannels):
      self.VRef[i] = self.ADCVRef[self.posGain.index(self.gain[i])]
    
  #   remove python 2 vs. python 3 incompatibility for gain: 2/3 (Adafruit_ADS1x15)
    for i in range(self.NChannels):
      if sys.version_info[:2] <=(2,7):
        if self.gain[i] == 2/3:
          self.gain[i] = int(self.gain[i])

  def init(self):
  #Hardware configuration:
    try:
      # Create an ADS1115 ADC (16-bit) instance.
      self.ADS = Adafruit_ADS1x15.ADS1115()
    except:
      print("ADS1115Config: Error initialising device - exit")
      sys.exit(1)

 # provide configuration parameters
    self.ChanNams = [ str(i) for i in range(self.NChannels) ]
    self.ChanLims = [ [0., self.VRef[i]] for i in range(self.NChannels) ]
    print(self.ChanLims)
      
  def acquireData(self, buf): 
    # read data from ADC
    for i in range(self.NChannels):
      buf[i] = self.ADS.read_adc(self.ADCChannels[i], gain = self.gain[i],
                            data_rate = self.sampleRate)*self.VRef[i]*self.ConvFactors[i]/32767

  def closeDevice(self):
   # nothing to do here
   pass
