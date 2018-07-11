#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''Data Logger 
     reads samples from ADS1115 and display xy-plot

     Usage: ./runXYPlotter.py [<XYPlotter_config>.yaml Interval]

'''

from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import sys, time, yaml, numpy as np, threading, multiprocessing as mp, Adafruit_ADS1x15
sys.path.append('..')

# import relevant pieces from phypidaq
from XYPlotterConfig import SensorConfig
from phypidaq.mpXYPlotter import mpXYPlotter

# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

# helper functions

def kbdInput(cmdQ):
  ''' 
    read keyboard input, run as backround-thread to aviod blocking
  '''
# 1st, remove python 2 vs. python 3 incompatibility for keyboard input
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
      print('    terminating ' + p.name)
      p.terminate()
      time.sleep(1.)

if __name__ == "__main__": # - - - - - - - - - - - - - - - - - - - - - -

  print('\n*==* script ' + sys.argv[0] + ' running \n')

# check for / read command line arguments
  # read DAQ configuration file
  if len(sys.argv)>=2:
    SensorConfFile = sys.argv[1]
  else: 
    SensorConfFile = 'XYPlotter.yaml'
  print('    ADS1115 configuration from file ' + SensorConfFile)

  if len(sys.argv)==3:
    interval = float(sys.argv[2])
  else: 
    interval = 0.1

  if interval < 0.05:
    print(" !!! read-out intervals < 0.05 s not reliable, setting to 0.05 s")
    interval = 0.05

  # read scope configuration file
  print('    Device configuration from file ' + SensorConfFile)
  try:
    with open(SensorConfFile) as f:
      SensorConfDict=yaml.load(f)
      print(SensorConfDict)
  except:
    print('     failed to read scope configuration file ' + SemsorConfFile)
    exit(1)

# configure and initialize Sensor
  SensorConf=SensorConfig(SensorConfDict)
  SensorConf.init()
  # copy some of the important configuration variables
  NChannels = SensorConf.NChannels # number of channels in use
  NSamples = SensorConf.NSamples   # number of samples
  Units = SensorConf.Units # physical unit
  GAIN = SensorConf.gain # programmable gain ADS1115
  RSampling = SensorConf.sampleRate # sample rate ADS1115
  ADCChannels = SensorConf.ADCChannels # ADC-Channels ADS1115
  ConvFactors = SensorConf.ConvFactors # conversion factors for calculation of sensor value

### --- determine reference voltage for ADC calculation
# possible values reference voltage
  ADCRefVolt = [6.114, 4.096, 2.048, 1.024, 0.512, 0.256]
# determine the corresponding index
  RefVolt = [0, 0]
  posGain = [2/3, 1, 2 , 4, 8, 16]
  for i in range(NChannels):
    RefVolt[i] = ADCRefVolt[posGain.index(GAIN[i])]
    
# remove python 2 vs. python 3 incompatibility for gain: 2/3 (Adafruit_ADS1x15)
  for i in range(NChannels):
      if sys.version_info[:2] <=(2,7):
        if GAIN[i] == 2/3:
          GAIN[i] = int(GAIN[i])

  def getData():
    # read data sample from ADS1115
    global sig
    for i in range(NChannels):
      sig[i] = adc.read_adc(ADCChannels[i], gain = GAIN[i],
                            data_rate = RSampling)*RefVolt[i]*ConvFactors[i]/32767
    return sig

### --- general code
  thrds=[]
  procs=[]
  cmdQ = mp.Queue(1) # Queue for command input

  DGmpQ =  mp.Queue(1) # Queue for data transfer to sub-process
  procs.append(mp.Process(name='DataGraphs', target = mpXYPlotter, 
    args=(DGmpQ, SensorConf.SensorConfDict, Units, cmdQ) ) )
#         Queue     config            Sigln.name  CommandQ

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

  DAQ_ACTIVE = True  # Data Acquistion active    
  # -- LOOP
  sig = np.zeros(NChannels)
  try:
    cnt = 0
    while True:
      if DAQ_ACTIVE:
        cnt += 1
        sig = getData()
        DGmpQ.put(sig)
        
# check for keboard input
      if not cmdQ.empty():
        cmd = cmdQ.get()
        if cmd == 'E':          # E(nd)  
          DGmpQ.put(None)       # send empty "end" event
          print('\n' + sys.argv[0] + ': End command recieved - closing down')
          ACTIVE = False
          break
        elif cmd == 'P':       # P(ause)
          DAQ_ACTIVE = False     
        elif cmd == 'R':       # R(esume)
          DAQ_ACTIVE = True    
        elif cmd == 's':       # s(ave)
          DAQ_ACTIVE = False     
          ACTIVE = False
          print('\n storing data to file, ending')
          pass # to be implemented ...
          break

  except KeyboardInterrupt:
     print(sys.argv[0]+': keyboard interrupt - closing down ...')
     DAQ_ACTIVE = False     
     ACTIVE = False
  finally:
    SensorConf.closeDevice() # close down hardware device
    time.sleep(1.)
    stop_processes(procs)  # stop all sub-processes in list
    print('*==* ' + sys.argv[0] + ': normal end \n')

