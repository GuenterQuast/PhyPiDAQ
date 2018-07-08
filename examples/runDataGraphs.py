#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''Data visualisation
     this script reads data samples from PicoScope and 
     displays data as effective voltage, history display and xy plot

     Usage: ./runVoltmeter.py [<Oscilloscpope_config>.yaml Interval]
'''

from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import sys, time, yaml, numpy as np, threading, multiprocessing as mp

# import relevant pieces from picodaqa
import picodaqa.picoConfig
from picodaqa.mpDataGraphs import mpDataGraphs

# helper functions

def kbdInput(cmdQ):
  ''' 
    read keyboard input, run as backround-thread to aviod blocking
  '''
# 1st, remove pyhton 2 vs. python 3 incompatibility for keyboard input
  if sys.version_info[:2] <=(2,7):
    get_input = raw_input
  else: 
    get_input = input
 
  while ACTIVE:
    kbdtxt = get_input(20*' ' + 'type -> P(ause), R(esume), E(nd) or s(ave) + <ret> ')
    cmdQ.put(kbdtxt)
    kbdtxt = ''

def stop_processes(proclst):
  '''
    Close all running processes at end of run
  '''
  for p in proclst: # stop all sub-processes
    if p.is_alive():
      print('    terminating '+p.name)
      if p.is_alive(): p.terminate()
      time.sleep(1.)

if __name__ == "__main__": # - - - - - - - - - - - - - - - - - - - - - -

  print('\n*==* script ' + sys.argv[0] + ' running \n')

# check for / read command line arguments
  # read DAQ configuration file
  if len(sys.argv) >= 2:
    PSconfFile = sys.argv[1]
  else: 
    PSconfFile = 'PSVoltMeter.yaml'
  print('    PS configuration from file ' + PSconfFile)

  if len(sys.argv)==3:
    interval = float(sys.argv[2])
  else: 
    interval = 0.5

  if interval < 0.05:
    print(" !!! read-out intervals < 0.05 s not reliable, setting to 0.05 s")
    interval = 0.05

  # read scope configuration file
  print('    Device configuration from file ' + PSconfFile)
  try:
    with open(PSconfFile) as f:
      PSconfDict=yaml.load(f)
  except:
    print('     failed to read scope configuration file ' + PSconfFile)
    exit(1)

# configure and initialize PicoScope
  PSconf=picodaqa.picoConfig.PSconfig(PSconfDict)
  PSconf.init()
  # copy some of the important configuration variables
  NChannels = PSconf.NChannels # number of channels in use
  TSampling = PSconf.TSampling # sampling interval
  NSamples = PSconf.NSamples   # number of samples
  buf = np.zeros( (NChannels, NSamples) ) # data buffer for PicoScope driver

  thrds=[]
  procs=[]
  deltaT = interval * 1000.   # update interval in ms
  cmdQ =  mp.Queue(1) # Queue for command input
  DGmpQ =  mp.Queue(1) # Queue for data transfer to sub-process
  XY = True  # display Channel A vs. B if True
  procs.append(mp.Process(name='DataGraphs', target = mpDataGraphs, 
    args=(DGmpQ, PSconf.OscConfDict, deltaT, '(Volt)', XY, cmdQ) ) )
#                Queue            config                      interval    name

  thrds.append(threading.Thread(name='kbdInput', target = kbdInput, 
               args = (cmdQ,)  ) )
#                           Queue       

# start subprocess(es)
  for prc in procs:
    prc.deamon = True
    prc.start()
    print(' -> starting process ', prc.name, ' PID=', prc.pid)

  ACTIVE = True # thread(s) active 
  # start threads
  for thrd in thrds:
    print(' -> starting thread ', thrd.name)
    thrd.deamon = True
    thrd.start()

  DAQ_ACTIVE = True  # Data Acquisition active    
# -- LOOP 
  sig = np.zeros(NChannels)
  try:
    cnt = 0
    T0 = time.time()
    while True:
      if DAQ_ACTIVE:
        cnt +=1
        PSconf.acquireData(buf) # read data from PicoScope
        # construct an "event" like BufferMan.py does and send via Queue
        for i, b in enumerate(buf): # process data 
         # sig[i] = np.sqrt (np.inner(b, b) / NSamples)    # eff. Voltage
          sig[i] = b.sum() / NSamples          # average
        DGmpQ.put(sig)

   # check for keboard input
      if not cmdQ.empty():
        cmd = cmdQ.get()
        if cmd == 'E':
          DGmpQ.put(None)       # send empty "end" event
          print('\n' + sys.argv[0] + ': End command recieved - closing down')
          ACTIVE = False
          break
        elif cmd == 'P':
          DAQ_ACTIVE = False     
        elif cmd == 'R':
          DAQ_ACTIVE = True
        elif cmd == 's':  
          DGmpQ.put(None)       # send empty "end" event
          DAQ_ACTIVE = False     
          ACTIVE = False
          print('\n storing data to file, ending')
          pass # to be implemented ...
          break
 
  except KeyboardInterrupt:
    DAQ_ACTIVE = False     
    ACTIVE = False
    print('\n' + sys.argv[0]+': keyboard interrupt - closing down ...')

  finally:
    PSconf.closeDevice() # close down hardware device
    time.sleep(1.)
    stop_processes(procs)  # stop all sub-processes in list
    print('*==* ' + sys.argv[0] + ': normal end')
