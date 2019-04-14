#!/usr/bin/python
"""Frequency generator 
    uses pulse width modulation for signal periods < 0.013 s
    optional Arguments:
      $1: GPIO pin
      $2: signal period
      $3: duty cycle of signal 
"""

from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import time, sys, math, random
import RPi.GPIO as gpio
gpio.setmode(gpio.BCM)
import threading

# initialize defaults
GPIOpin = 19     # GPIO pin for output signal
dt=0.02          # signal Period
dc= 0.5          # signal duty cycle 

dtslow=0.013    # "slow signal"

if len(sys.argv) > 1:
  GPIOpin = int(sys.argv[1])
if len(sys.argv) > 2:
  dt = float(sys.argv[2])
if len(sys.argv) > 3:
  dc = float(sys.argv[3])

def pulse(pin, ton):
  gpio.output(pin, 1)
  time.sleep(ton)
  gpio.output(pin, 0)

def pwmpulse(pin, dt, dc=0.5):
  pwm = gpio.PWM(pin, 1./dt)
  pwm.start(dc)     # start with duty cycle dc


print('flashing GPIO pin %i with dt= %.3gs and duty cycle %.3g'%(GPIOpin, dt, dc) )
if dt<dtslow: print('         using gpio.PWM()')

try:
  gpio.setup(GPIOpin, gpio.OUT)  # initialize GPIO pin for output
  if dt >= dtslow: # use time.sleep for slow signals
    ton = dt * dc  # active time of signal 
    dtcum = 0.
    T0 = time.time()
    while True:
      flashThread=threading.Thread(target=pulse, args=(GPIOpin, ton,))
      flashThread.start()
      dtcor = dt - time.time() + T0  + dtcum
      if dtcor > 0.: time.sleep(dtcor)
      dtcum += dt

  else:  # use PWM for fast signals
    pwm = gpio.PWM(GPIOpin, 1./dt)
    pwm.start(dc)     # start with duty cycle dc
    while True:
      time.sleep(1.)

except  KeyboardInterrupt:
  print ("keyboard interrupt - ending")

finally:
  gpio.cleanup()
  sys.exit(0)
