#!/usr/bin/python
"""Frequency generator 
"""
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import time, sys, math, random
import RPi.GPIO as gpio
gpio.setmode(gpio.BCM)
import threading

dt=0.02
tflash=0.005
GPIOpin = 19

gpio.setup(GPIOpin, gpio.OUT)

def pulse(pin, dt):
  gpio.output(pin, 1)
  time.sleep(dt)
  gpio.output(pin, 0)

try:
  while True:
    flashThread=threading.Thread(target=pulse, args=(GPIOpin, tflash,))
    flashThread.start()
    time.sleep(dt)
                     
except  KeyboardInterrupt:
  print ("keyboard interrupt - ending")

finally:
  gpio.cleanup()
  sys.exit(0)
