# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import numpy as np, yaml, time, sys, Adafruit_ADS1x15

class SensorConfig(object):
  '''set Sensor configuration'''

  def __init__(self, confdict=None):
    if confdict==None: confdict={}

# set configuration parameters
# -- Sensor model
    if "SensorModel" in confdict: 
      self.SensorModel = confdict["SensorModel"]
    else:
      self.SensorModel = 'ADS1115'
# -- unit
    if "Units" in confdict: 
      self.Units = confdict["Units"]
    else:
      self.Units = ['Volt', 'Volt']      
# -- channels to be used
    if "Channels" in confdict: 
      self.Channels = confdict["Channels"]
    else:
      self.Channels = ['A, B'] # channels
    self.NChannels = len(self.Channels)

# -- signal height:
    if "ChanRanges" in confdict:
      self.ChanRanges = confdict["ChanRanges"]
    else:
      self.ChanRanges = [5.0, 5.0] # voltage range
    if "ChanOffsets" in confdict: 
      self.ChanOffsets = confdict['ChanOffsets']
    else:
      self.ChanOffsets= [0. for i in range(self.NChannels)]
    self.ChanLims = []
    for i in range(self.NChannels):
      self.ChanLims.append( (0, self.ChanRanges[i]-self.ChanOffsets[i]))
    
    
# -- signal timing
    if "Nsamples" in confdict:
      self.NSamples = confdict["Nsamples"]
    else:
      self.NSamples = 1  # number of samples to take
    if "Interval" in confdict: 
      self.Interval=confdict["Interval"]
    else:
      self.Interval = 0.1

# --  conversion factors for calculation of sensor value
    if "ConversionFactors" in confdict:
      self.ConvFactors = confdict["ConversionFactors"]  
    else:
      self.ConvFactors = [1, 1]
      
# -- gain configuration ADC ADS1115
    if "Gain" in confdict:
      self.gain = confdict["Gain"]
      for i in range(self.NChannels):
        if self.gain[i] == '2/3':
          self.gain[i] = 2/3
    else:
      self.gain = [1, 1]      # gain
    if "sampleRate" in confdict:
      self.sampleRate = confdict["sampleRate"]
    else:
      self.sampleRate = 860 # sample rate

# --  configuration channel ADS1115
    if "ADCChannels" in confdict:
      self.ADCChannels = confdict["ADCChannels"]  
    else:
      self.ADCChannels = [0, 1]     # number of channel ADS1115

# control printout, colors, ...
    if "ChanColors" in confdict: 
      self.ChanColors=confdict["ChanColors"]
    else:
      self.ChanColors = ['darkblue', 'darkslategrey', 'darkred', 'darkgreen']


# - end Sensor.__init__()

  def init(self):
# configuration parameters only known after initialisation

    self.XYmode = True
   
    try: 
      self.sensorIni() # run initialisation routine for device  
    except:
      print("SensorConfig: Error initialising device - exit")
      sys.exit(1)

   # store configuration parameters in dictionary
    self.SensorConfDict = {'Channels' : self.Channels,
                          'NChannels' : self.NChannels,
                          'NSamples' : self.NSamples,
                          'Interval' : self.Interval,
                          'RSampling' : self.sampleRate,
                          'CRanges' : self.ChanRanges,
                          'ChanOffsets': self.ChanOffsets,
                          'ChanLimits' : self.ChanLims,
                          'ChanNams' : self.Channels,
                          'ADCChannels' : self.ADCChannels,
                          'ConvFactors' : self.ConvFactors,
                          'Units': self.Units,
                          'Gain' : self.gain,
                          'XYmode': self.XYmode,
                          'ChanColors': self.ChanColors}
    #print('\Configuration:')
    #print(yaml.dump(self.SensorConfDict))
# - end Sensor.init()

  def sensorIni(self):
    ''' initialise device controlled by class SensorConfig '''


# -- end def sensorIni

  def closeDevice(self):
    '''
      Close down hardware device
    '''
    time.sleep(0.5)


