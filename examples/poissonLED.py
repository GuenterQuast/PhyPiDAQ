#!/usr/bin/python
"""PoissonLED
   LED flashing according to a random Poission Process
"""
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import time, sys, math, random
import RPi.GPIO as gpio

import threading

gpio.setmode(gpio.BCM)

pLED=26
gpio.setup(pLED,  gpio.OUT)

tau=0.05
tflash=0.005

def LEDflash(pin, dt):
  gpio.output(pin, 1)
  time.sleep(dt)
  gpio.output(pin, 0)

try:
  while True:
    flashThread=threading.Thread(target=LEDflash, args=(pLED, tflash,))
    flashThread.start()
    # generate exponentially distributed waiting time
    dt = -tau * math.log(random.uniform(0., 1.) )
    time.sleep(dt)
                     
except  KeyboardInterrupt:
    print ("keyboard interrupt - ending")

finally:
  gpio.cleanup()
  sys.exit(0)

