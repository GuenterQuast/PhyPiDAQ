#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''Data visualisation
     this script reads data samples from PicoScope and 
     displays data as effective voltage, history display and xy plot

     Usage: ./run_phypi.py [<PhyPiConf_file>.daq] [Interval]
'''

from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import sys, os, time, yaml, numpy as np, threading, multiprocessing as mp

# display module
from phypidaq.Display import *

# more imports from phypidaq depend on configuration options

from phypidaq.helpers import generateCalibrationFunction, stop_processes,kbdwait

# ----- helper functions --------------------

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

def decodeCommand(cmdQ):
  global ACTIVE, DAQ_ACTIVE
  '''
    evaluate keyboard commands
    returns:  0 invalid command
              1 status change
              2 exit
  '''

  cmd = cmdQ.get()
  rc = 0
  if cmd == 'E':
    #DGmpQ.put(None)       # send empty "end" event
    print('\n' + sys.argv[0] + ': End command received')
    ACTIVE = False
    rc = 2
  elif cmd == 'P':
    DAQ_ACTIVE = False
    rc = 1     
  elif cmd == 'R':
    DAQ_ACTIVE = True
    rc = 1
  elif cmd == 's':  
    #DGmpQ.put(None)       # send empty "end" event
    DAQ_ACTIVE = False     
    ACTIVE = False
    # print('\n storing data to file, ending')
    print('\n storing data to file not yet implemented, ending')
    # still to be implemented ...
    rc = 2

  return rc


def setup():
# set up data source, display module and options

  global interval, PhyPiConfDict, DEVs, ChanIdx_ofDevice, NHWChannels, \
         CalibFuncts, Formulae, NFormulae, DatRec 
  ''' 
    interval:            sampling interval
    PhyPiConfDict:       dictionary with config options
    DEVs:                list of instances of device classes
    ChanIdx_ofDevice:    index to store 1st chanel of device i
    NHWChannels          number of active hardware channels
    CalibFuncts:         functions for calibration of raw channel readings
    Formulae             list of formulae to apply to hardware channels
    NFormlae             number of forulae 
    DatRec:              instance of DataRecorder
  '''

# check for / read command line arguments
  if len(sys.argv) >=3:
    interval = float(sys.argv[2])
  else: 
    interval = 0.5

  # read PhyPiDAQ configuration file
  if len(sys.argv) >= 2:
    PhyPiConfFile = sys.argv[1]
  else:
    PhyPiConfFile = 'PhyPiConf.daq'

  # read DAQ configuration file
  print('  Configuration from file ' + PhyPiConfFile)
  try:
    with open(PhyPiConfFile) as f:
      PhyPiConfDict = yaml.load(f)
  except Exception as e:
    print('!!! failed to read configuration file ' + PhyPiConfFile)
    print(str(e))
    exit(1)

# set default options:
  if 'Interval' not in PhyPiConfDict:
    PhyPiConfDict['Interval'] = interval
  else:
    interval = PhyPiConfDict['Interval']
  if PhyPiConfDict['Interval'] < 0.05:
    print(" !!! read-out intervals < 0.05 s not reliable, setting to 0.05 s")
    PhyPiConfDict['Interval'] = 0.05

  if 'XYmode' not in PhyPiConfDict:  # default is XY mode off
    PhyPiConfDict['XYmode'] = False

  if 'DataFile' not in PhyPiConfDict:  # default is not to write output file
    PhyPiConfDict['DataFile'] = None

  if 'DisplayModule' not in PhyPiConfDict: # default display is DataLogger
    PhyPiConfDict['DisplayModule'] = 'DataLogger'

  if 'startActive' not in PhyPiConfDict:  # default is to start in Paused mode
    PhyPiConfDict['startActive'] = False

# read Device configuration(s) and instantiate device handler(s)
  if 'DeviceFile' in PhyPiConfDict:
    DevFiles = PhyPiConfDict['DeviceFile']
  elif "DAQModule" in PhyPiConfDict: 
    DevFiles = PhyPiConfDict["DAQModule"] + '.yaml' 
  else:
    DevFiles = 'ADS1115Config.yaml'
    print("Configuring for ADC ADS1115")

  # if not a list, make it one
  if type(DevFiles) != type([]):
    DevFiles = [DevFiles]
  NDevices = len(DevFiles)

  # open all device config files
  DEVconfDicts = []
  for fnam in DevFiles:  
    try:
      f = open(fnam)
      DEVconfDicts.append(yaml.load(f))
      f.close()
    except Exception as e:
      print('!!! failed to read configuration file ' + fnam)
      print(str(e))
      # kbdwait()
      exit(1)

# configure and initialize all Devices
  DEVNames = []               # device names
  NHWChannels = 0             # total number of hardware channels
  ChanNams = []               # names of HW channels
  ChanLims = []               # limits
  ChanIdx_ofDevice = []       # first channel of each device

  DEVs = []
  for i in range(NDevices):
    if 'DAQModule' in DEVconfDicts[i]:
      DEVNames.append(DEVconfDicts[i]['DAQModule'])
    elif 'DAQModule' in PhyPiConfDict:
      DEVNames.append(PhyPiConfDict['DAQModule'])
    else:  # try to derive from name of Device Config File
      cdir, cfnam = os.path.split(DeviceFiles[i])
      DEVNames.append(cfnam.split('.')[0])

    print('  configuring device ' + DEVNames[i])
    # import device class ...
    exec('from phypidaq.' + DEVNames[i] +  ' import ' + DEVNames[i])
    # ...  and instantiate device handler
    exec('global DEVs;  DEVs.append(' + DEVNames[i] + '(DEVconfDicts[i]) )' )
    DEVs[i].init()
    ChanIdx_ofDevice.append(NHWChannels)
    nC = DEVs[i].NChannels  
    NHWChannels += nC
    ChanNams += DEVs[i].ChanNams[0 : nC]
    ChanLims += DEVs[i].ChanLims[0 : nC]

# set up calibration Functions
  CalibFuncts = None
  if 'ChanCalib' in PhyPiConfDict:
    CalibFuncts = [None] * NHWChannels    
    calibData = PhyPiConfDict['ChanCalib']
    print('  Calibrating channels:')   
    for ic in range( NHWChannels): 
      print('   Chan ', ic, '   ', calibData[ic])   
      if calibData[ic] is not None: 
        CalibFuncts[ic] = generateCalibrationFunction(calibData[ic])

# Apply Formula(e) to calibrated channel reading(s)
  Formulae = None
  NFormulae = 0
  if 'ChanFormula' in PhyPiConfDict:
    Formulae = PhyPiConfDict['ChanFormula']
    NFormulae = len(Formulae)
    print('applying fromulae:')
    for ifc in range( NFormulae): 
      if Formulae[ifc]: print('   FChan ', ifc, '   ', Formulae[ifc])   

# number of channels may be greater than number of hardware channels
  NChannels = max(NHWChannels, NFormulae)
  PhyPiConfDict['NChannels'] = NChannels

# Add information for graphical display(s) to PhyPiConfDict
  if 'ChanNams' not in PhyPiConfDict:
    PhyPiConfDict['ChanNams' ] = ChanNams 
    if NFormulae > NHWChannels:
      ChanNams += (NFormulae-NHWChannels) * ['F']
      for ifc in range( NFormulae): 
        if Formulae[ifc]: ChanNams[ifc] = 'F' + str(ifc)
     
  if 'ChanLimits' not in PhyPiConfDict:
    if NFormulae > 0:
      print('PhyPiDAQ: forumla(e) defined, but no ChanLimits supplied ')  
      print('     results may become unpredictable - exiting')  
      exit(1)
    PhyPiConfDict['ChanLimits'] = ChanLims # take from devices if not set

# start data recording to disk if required
  if PhyPiConfDict['DataFile'] != None:
    FName = PhyPiConfDict['DataFile']
    from phypidaq.DataRecorder import DataRecorder
    DatRec = DataRecorder(FName, PhyPiConfDict)
  else:
    DatRec = None

  print ('\nPhyPiDAQ Configuration:')
  print (yaml.dump(PhyPiConfDict) )

def apply_calibs():
  global data
  '''
    apply calibration functions to hardware channels    

    input: Calibration Functions as calucated by 
           generateCalibrationFunctions() from interpolated 
           values in calibration table calibData[]

    output: calibrated channel values
  '''

  for i in range(NHWChannels):
    if CalibFuncts[i] is not None:
      data[i] = CalibFuncts[i](data[i])

def apply_formulae():
  global data
  '''
    calculate new quantities from hardware channels c0, c1, ...
     replace entries in data by calculated quantities
  
    input:  - data from hardware channels
            - list of formulae 
            data in hw channels c0, c1, ...

    formula expressions are valid python expressions, where
    all functions from math package can be used

    output: calcuated quantities by applying formula 
            f1(c0, c1 ...), f2(c0, c1, ...), ...

    number of formulae may exceed number of hardware channels
  '''

  #  copy data from hardware channels
  for ifc in range(NFormulae):
    exec('c'+str(ifc) + '=data['+str(ifc)+']')

  #  apply formulae to signal data
  for ifc in range(NFormulae):
    if Formulae[ifc]:
        data[ifc] = eval(Formulae[ifc])


if __name__ == "__main__": # - - - - - - - - - - - - - - - - - - - - - -

  print('\n*==* script ' + sys.argv[0] + ' running \n')


  longInterval = 2. # definiton of a "long" readout interval
  setup()
  NChannels = PhyPiConfDict['NChannels']
  DisplayModule = PhyPiConfDict['DisplayModule']
  if Formulae: from math import *   # make math functions available


  cmdQ =  mp.Queue(1) # Queue for command input
  datQ =  mp.Queue(1) # Queue to spy on data transfer inside class Display
  if 'startActive' not in PhyPiConfDict:  # start in paused-mode
    PhyPiConfDict['startActive'] = False
  if 'DAQCntrl' not in PhyPiConfDict:  # enable run control buttons
    PhyPiConfDict['DAQCntrl'] = True

  display = Display(interval = 0.1, 
                    confdict = PhyPiConfDict, 
                    cmdQ = cmdQ,
                    datQ = datQ )
  display.init()
  ACTIVE = True #  background process(es) active

  if PhyPiConfDict['startActive']:
    DAQ_ACTIVE = True # Data Acquisition active
  else:
  # start in paused-mode
    DAQ_ACTIVE = False # Data Acquisition inactive  # start threads
    print('  starting in Paused mode - type R to resume')

# start keyboard control
  kbdthrd=threading.Thread(name='kbdInput', target = kbdInput, args = (cmdQ,)  )
#                                                                      Queue       
  kbdthrd.daemon = True
  kbdthrd.start()  

  # set up space for data
  data = np.zeros(NChannels)

#  DAQ_ACTIVE = True  # Data Acquisition active    
# -- LOOP 
  try:
    cnt = 0
    T0 = time.time()
    brk = False

    while ACTIVE:
         
      # regularly check for command input for long intervals
      if interval > longInterval and DAQ_ACTIVE:
        cmd = 0 
        while not datQ.empty():  # check for command input
          if not cmdQ.empty():
            cmd = decodeCommand(cmdQ)  
            if cmd: break # got valid command
          time.sleep( min(interval/100., 0.2) )
        if cmd >= 2: break  # end command received

      if DAQ_ACTIVE:
        cnt +=1
      # read data
        for i, DEV in enumerate(DEVs):
          DEV.acquireData(data[ChanIdx_ofDevice[i]:])
      # calibrate raw readings
        if CalibFuncts: apply_calibs()
      # apply fromula(e) 
        if Formulae: apply_formulae()

      # display data ...
        display.show(data)

      # ... and record data to disc
        if DatRec: DatRec(data)

      else:   # paused mode
        time.sleep( min(interval/10., 0.2) )

      # check for control input (from keyboard or display module)
      if not cmdQ.empty(): decodeCommand(cmdQ)

    # -- end while ACITVE 
    #print('\n' + sys.argv[0] + ': normal end') 
 
  except KeyboardInterrupt:
    DAQ_ACTIVE = False     
    ACTIVE = False
    print('\n' + sys.argv[0] +': keyboard interrupt - closing down ...')

  #except Exception as e:
  #  print('!!! ' + sys.argv[0] + 'got Exception %s \n closing down'(str(e)) )

  except:
    # 'except Exception as e' leaves some errors unnoted
    print('\n!!! ' + sys.argv[0] + ': exception in data-taking loop' )
    print(sys.exc_info()[1])
  finally:
    ACTIVE = False
    if DatRec: DatRec.close()
    for DEV in DEVs:
      DEV.closeDevice() # close down hardware device
    display.close()
    time.sleep(1.)
     
    print('*==* ' + sys.argv[0] + ': end -      press <ret>')
    sys.exit()
