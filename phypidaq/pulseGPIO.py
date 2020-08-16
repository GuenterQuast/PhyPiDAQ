# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import numpy as np, time, sys
import RPi.GPIO as gpio
from multiprocessing import Process, Queue

class pulseGPIO(object):
  '''Set Signal on Raspberry Pi GPIO pin'''

  def pulseGPIOpin(self):
    # sub-process to pulse GPIO pin
    while True:

      ton = self.Q.get() # wait for entry in Queue
      # ton > 0: pin on for ton sec
      # ton = 0: pin on
      # ton < 0: pin off

      if ton == 0:
        gpio.output(self.pin, 1)
      elif ton > 0:
        gpio.output(self.pin, 1)
        time.sleep(ton)
        gpio.output(self.pin, 0)
      else:
        gpio.output(self.pin, 0)

  def __init__(self, pin = None):
    '''Args: pin: GPIO pin number
             cmdQ: multiprocessing queue'''
    gpio.setmode(gpio.BCM)
    if pin == None:
      print("pulseGPIO config error: no GPIO Pin specified - exiting")
      sys.exit(1)
    self.pin = pin
    self.Q = Queue(1)

    try:
      gpio.setup(pin, gpio.OUT)  # initialize GPIO pin for output
    except Exception as e:
      print("pulseGPIO Error setting up GPIO output")
      print(e)       

    # start pulser as background process
    self.subprocs = []
    self.subprocs.append(Process(name='pulseGPIOpin',
                                 target=self.pulseGPIOpin))
    for p in self.subprocs:
      p.daemon = True
      p.start()    

  def pulse(self, ton=None):
    # produce one pulse of duration <ton>
    #  default ton=0.05 sec
    #    ton > 0: pin on for ton sec
    #    ton = 0: pin on
    #    ton < 0: pin off
    if ton==None: ton = 0.05
    if self.Q.empty(): self.Q.put(ton)
    
  def close(self):
    for p in self.subprocs:
      if p.is_alive():
        p.terminate()
    self.cmdQ.close()
    gpio.cleanup(self.pin)
