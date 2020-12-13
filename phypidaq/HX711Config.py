# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import numpy as np, time, sys, RPi.GPIO as GPIO

class HX711Config(object):
  '''ADC HX711Config configuration and interface'''

  def __init__(self, confdict = None):
    if confdict==None: confdict={}

    self.OFFSET = 0
    self.GAIN = 0
      
# -- chosen DT-GPIO
    if 'DT' in confdict:
      self.DT = confdict['DT']
    else:
      self.DT = 5
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.DT, GPIO.IN)

# -- chosen SCK-GPIO
    if 'SCK' in confdict:
      self.SCK = confdict['SCK']
    else:
      self.SCK = 6
    GPIO.setup(self.SCK, GPIO.OUT)

# -- gain configuration HX711
    if "Gain" in confdict:
      self.gain = confdict["Gain"]
    else:
      self.gain = 128
      
  def init(self):
  # Hardware configuration:
    try:
        # resetting HX711
        self.reset()
        # setting gain
        self.setGain()
        # setting offset
        self.OFFSET = self.readAverage()
        self.setOffset(self.OFFSET)
    except Exception as e:
        print("HX711Config: Error initialising device - exit")
        print(str(e))
        sys.exit(1)

 # provide configuration parameters
    self.NChannels = 1
    self.ChanNams = [ str(i) for i in range(self.NChannels) ]
    self.ChanLims = [ [-8388607, 8388607] for i in range(self.NChannels) ]

  def isReady(self):
    return GPIO.input(self.DT) == 0

  def readData(self):
    while not self.isReady():
    #print("WAITING")
      pass
  
    # creating 3 byte for data
    dataBit = [np.zeros(8, dtype = bool), np.zeros(8, dtype = bool), np.zeros(8, dtype = bool)]
    # reading 3 byte data from HX711
    for j in range(3):
      for i in range(8):
        GPIO.output(self.SCK, True)
        dataBit[j][i] = GPIO.input(self.DT)
        GPIO.output(self.SCK, False)
        
    # setting channel and gain factor for next reading
    for i in range(self.GAIN):   
      GPIO.output(self.SCK, True)
      GPIO.output(self.SCK, False)

    # packing eight bit to one byte
    dataByte = np.packbits(dataBit)

    # check if the result is negative (two's complement)    
    if dataByte[0] & 0b10000000:
      # shifting bytes in right order and transforming two's complement (inverting each bit and adding 1)
      # to an negative int32 in python
      lastValue = - np.int32((~dataByte[0] << 16) | (~dataByte[1]<<8) | ~dataByte[2]) + 1
    else:
      # shifting bytes in right order and transforming to an int32
      lastValue = np.int32((dataByte[0] << 16) | (dataByte[1]<<8) | dataByte[2])  
    return lastValue

  def setGain(self):
    if self.gain == 128:
      # sending 25 pulses, 24 (getting data) + 3(setting gain 128 for next reading)
      self.GAIN = 24
    elif self.gain == 64:
      # sending 27 pulses, 24 (getting data) + 3(setting gain 64 for next reading)
      self.GAIN = 3
    elif self.gain == 32:
      # sending 26 pulse, 24 (getting data) + 2(setting gain 32 for next reading)
      self.GAIN = 2
    else:
      print("HX711Config: Error gain configuration - exit")
    GPIO.output(self.SCK, False)
    # setting gain by calling self.acquireData()
    self.readData()

  def readAverage(self, times = 10):
    values = 0
    for i in range(times):
      values += self.readData()
    return values // times
                      
  def setOffset(self, offset):
    self.OFFSET = offset
      
  def acquireData(self, buf): 
    # read data from HX711
    buf[0] = self.readData()-self.OFFSET
                        
# -- HX711 datasheet states that setting the SCK pin on high for >60 microseconds would power off the chip
  def powerDown(self):
    GPIO.output(self.SCK, False)
    GPIO.output(self.SCK, True)
    time.sleep(0.0001)

  def powerUp(self):
    GPIO.output(self.SCK, False)
    time.sleep(0.0001)
                      
# -- reset
  def reset(self):
    self.powerDown()
    self.powerUp()
                      
# -- set offset
  def setOffset(self, offset):
    self.OFFSET = offset
                      

  def closeDevice(self):
   GPIO.cleanup()
   pass
