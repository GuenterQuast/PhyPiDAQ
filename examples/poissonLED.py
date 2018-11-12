#!/usr/bin/python
"""PoissonLED
   LED flashing according to a random Poission Process
"""
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import time, sys, math, random, threading
import RPi.GPIO as gpio
gpio.setmode(gpio.BCM)

def LEDflash(pin, dt):
  # flash GPIO pin for time dt
  gpio.output(pin, 1)
  time.sleep(dt)
  gpio.output(pin, 0)

pLED=26
gpio.setup(pLED,  gpio.OUT)

tau = 1.  # 1 second default 
if len(sys.argv) > 1:
  tau = float(sys.argv[1])
tflash=0.0075

print('flashing GPIO pin %i randomly with tau= %.3gs' %(pLED, tau) )
try:
  dtcum = 0.
  T0 = time.time()
  while True:
    flashThread=threading.Thread(target=LEDflash, args=(pLED, tflash,))
    flashThread.start()
    # generate exponentially distributed waiting time
    dt = -tau * math.log(random.uniform(0., 1.) )
    dtcor = dt - time.time() + T0  + dtcum
    if dtcor > 0.: time.sleep(dtcor)
    dtcum += dt

except  KeyboardInterrupt:
    print ("keyboard interrupt - ending")

finally:
  gpio.cleanup()
  sys.exit(0)

