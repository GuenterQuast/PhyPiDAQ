# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import sys, time, numpy as np
from scipy import interpolate 

def generateCalibrationFunction(calibd):
  '''
   interpolate calibration table t= true, r = raw values ; 
   if only one number for trueVals given, then this is 
   interpreted as a simple calibration factor
 
   Args: 
     calibd:   calibration data
         either a single number as calibration factor: fc
         or a list or two arrays: [ [true values], [raw values] ]    
   Returns: interpolation function
  ''' 
  try:
    iter(calibd)
    # if no error, input is an array
    r = calibd[1]
    t = calibd[0]
  except:
   # input is only one number
    r = [0., 1.]
    t = [0., calibd]    
  # check input
  if len(t) != len(r):
    print('!!! generateCalibrationFunction: lengths of input arrays not equal - exiting') 
    exit(1)
  # make sure raw values are sorted - and simultaneously sort true values
  r, t = zip(*sorted(zip(r, t) ) )
  # perform spline interpolation of appropriate order k
  return interpolate.UnivariateSpline(r, t, k = min(3, len(t)-1), s = 0 )

def stop_processes(proclst):
  '''
    Close all running processes at end of run
  '''
  for p in proclst: # stop all sub-processes
    if p.is_alive():
      print('    terminating ' + p.name)
      if p.is_alive(): p.terminate()
      time.sleep(1.)

def kbdwait(prompt = None):
  ''' 
    wait for keyboard input
  '''
  # 1st, remove pyhton 2 vs. python 3 incompatibility for keyboard input
  if sys.version_info[:2] <=(2,7):
    get_input = raw_input
  else: 
    get_input = input
 #  wait for input
  if prompt == None:
    return get_input(50*' '+'type <ret> to exit -> ')
  else:
    return get_input(prompt)


class DAQwait(object):
  '''class implementing sleep corrected wiht system time
  '''
  def __init__(self, dt):
    '''Args:
         dt: wait time in seconds
    '''
    self.dt = dt
    self.lag = False # indicate occurrence of time lag
    self.T0 = time.time()
    
  def __call__(self, T0=None):
    '''gurantee correct timing  
       Args: 
         TO:   start time of action to be timed     
                 if not given, take end-time of last wait
    '''
    if T0 != None: self.T0 = T0    
    dtcor = self.dt - time.time() + self.T0
    if dtcor > 0. :  
      time.sleep(dtcor) 
      self.lag=False
    else:
      self.lag=True
    self.T0=time.time() # end of sleep = start of next interval   

class RingBuffer(object):
  '''ring buffer to store N objcts
  '''

  # implemented as a simple list, where old entries
  #  are overwritten if lenght of list is exceeded

  def __init__(self, N):
    '''
      N: size of buffer
    '''
    self.N = N
    self.B = [None] * N # initialize a list 
    self.full = False 
    self.k = -1

  def store(self, d):
    '''
      d: data object
    '''
 
    # increment index, eventually overwrite oldest data
    self.k += 1
    if self.k == self.N:
      self.k = 0
      self.full = True
    # store data 
    self.B[self.k] = d


  def read(self):
    '''return all data'''

    if self.full:
      return self.B[self.k : ] + self.B[ : self.k]
    else:
      return self.B[ : self.k]
