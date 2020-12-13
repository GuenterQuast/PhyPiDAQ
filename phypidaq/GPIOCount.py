# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import numpy as np, time, sys

# import GPIO libray
import RPi.GPIO as GPIO

class GPIOCount(object):
  '''Pulse Counting on GPIO pins, configuration and interface'''

  def __init__(self, confdict = None):
    if confdict==None: confdict={}

    if 'GPIOpins' in confdict:
      self.GPIOpins = confdict['GPIOpins']
    else:
      self.GPIOpins = [21]
    self.NChannels = len(self.GPIOpins)

    if 'Modes' in confdict:
       self.Modes = confdict['Modes']
    else:
      self.Modes = [0] * self.NChannels

  # inner Class for callback mechanism
  class Count:
    def __init__(self, gp):
      self.gp = gp     # pin number for this function
      self.counts = np.int64(0) 
      self.lastcount = np.int64(0)
      print(' GPIOCount: initialised callback for GPIO pin ', self.gp)

    def __call__(self, gp):
      if gp != self.gp:
         print(' initialised for pin ', self.gp, ', but received ', gp)
      self.counts +=1

  def init(self):
    # set up GPIO pins 
    try:
      GPIO.setmode(GPIO.BCM)    # use Raspberry numbering scheme
      self.cbf = []                  # callback functions
      for i, gp in enumerate(self.GPIOpins):
        # configure as inputs, no pull-up / -down
        GPIO.setup(gp, GPIO.IN)   
        # create an instance of Count function for each pin 
        self.cbf.append(self.Count(gp))  
        # set call-back functions on each active pin
        bounce_time = 1 # time for debouncing 
        if self.Modes[i]:  
          GPIO.add_event_detect(gp, GPIO.FALLING, bouncetime=bounce_time) 
        else: 
          GPIO.add_event_detect(gp, GPIO.RISING, bouncetime=bounce_time)
        # set callback function
        GPIO.add_event_callback(gp, self.cbf[i])     
    except:
      print("GPIOCount: failed to initialise GPIO - exit")
      sys.exit(1)

    # set names and channel-range limits
    self.ChanNams = []
    self.ChanLims = []
    for i, c in enumerate(self.GPIOpins):
      self.ChanNams.append(str(c))
      # some guessing here - upper range to be overwritten in calling function
      self.ChanLims.append( [0., 100.] ) 

  def acquireData(self, buf): 
    # return number of counts since last called
    for i, gp in enumerate (self.GPIOpins):
      c = self.cbf[i].counts
      buf[i] = c - self.cbf[i].lastcount       
      self.cbf[i].lastcount = c      

  def closeDevice(self):
   # clean callback functions and free used GPIO pins
   for gp in self.GPIOpins:
     GPIO.remove_event_detect(gp)
     GPIO.cleanup(gp)
