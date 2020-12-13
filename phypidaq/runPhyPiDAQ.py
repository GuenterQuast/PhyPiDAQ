#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''Data visualisation
     this script reads data samples from PicoScope and 
     displays data as effective voltage, history display and xy plot

     Usage: ./runPhyPiDAQ.py [<PhyPiConf_file>.daq] [Interval]
'''

from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import sys, os, errno, time
import yaml, numpy as np, threading, multiprocessing as mp

# math module needed for formulae
from math import *
# interpolate needed for calibration
from scipy import interpolate 

# display module
from .Display import *

from .DataRecorder import DataRecorder
from .helpers import RingBuffer, DAQwait

# ----- helper functions --------------------

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
      # print('    terminating ' + p.name)
      if p.is_alive(): p.terminate()
      time.sleep(1.)

# ----- class for running data acquisition --------------------

class runPhyPiDAQ(object):

  def __init__(self,verbose = 1):
    self.verbose= verbose
    
  def kbdInput(self, cmdQ):
    ''' 
      read keyboard input, run as background-thread to aviod blocking
    '''
  # 1st, remove pyhton 2 vs. python 3 incompatibility for keyboard input
    if sys.version_info[:2] <=(2,7):
      get_input = raw_input
    else: 
      get_input = input
 
    while self.ACTIVE:
      kbdtxt = get_input(20*' ' + 'type -> P(ause), R(esume), E(nd) or s(ave) + <ret> ')
      cmdQ.put(kbdtxt)
      kbdtxt = ''

  def decodeCommand(self, cmdQ):
    '''
      evaluate keyboard commands
      returns:  0 invalid command
                1 status change
                2 exit
    '''

    cmd = cmdQ.get()
    rc = 0
    if cmd == 'E':
      if self.verbose > 1:
        print('\n' + sys.argv[0] + ': End command received')
      self.ACTIVE = False
      rc = 2
    elif cmd == 'P':
      self.DAQ_ACTIVE = False
      rc = 1     
    elif cmd == 'R':
      self.DAQ_ACTIVE = True
      rc = 1
    elif cmd == 's':  
      self.DAQ_ACTIVE = False 
      if self.RBuf is not None:
        print('\n storing data to file ', self.bufferFile, ' - now paused')
        print(42*' ' + '  -> R(esume), E(nd) + <ret> ', end='', flush=True)
        self.storeBufferData(self.bufferFile) 
      else:
        print('\n buffer storage not active - no action')
      rc=1

    return rc

  def storeBufferData(self, fnam):
     bufRec = DataRecorder(fnam, self.PhyPiConfDict)
     for d in self.RBuf.read():
       bufRec(d)
     bufRec.close()

  def setup(self):
    '''
      set up data source(s), display module and options
     
      interval:            sampling interval
      PhyPiConfDict:       dictionary with config options
      DEVs:                list of instances of device classes
      ChanIdx_ofDevice:    index to store 1st channel of device i
      NHWChannels          number of active hardware channels
      CalibFuncts:         functions for calibration of raw channel readings
      Formulae:            list of formulae to apply to hardware channels
      NFormulae:           number of formulae
      DatRec:              instance of DataRecorder
    '''

  # check for / read command line arguments
    if len(sys.argv) >=3:
      self.interval = float(sys.argv[2])
    else: 
      self.interval = 0.5

    # read PhyPiDAQ configuration file
    if len(sys.argv) >= 2:
      PhyPiConfFile = sys.argv[1]
    else:
      PhyPiConfFile = 'PhyPiConf.daq'

    # read DAQ configuration file
    if self.verbose:
      print('  Configuration from file ' + PhyPiConfFile)
    try:
      with open(PhyPiConfFile) as f:
        PhyPiConfDict = yaml.load(f, Loader=yaml.Loader)
    except Exception as e:
      print('!!! failed to read configuration file ' + PhyPiConfFile)
      print(str(e))
      exit(1)

  # set default options:
    if 'Interval' not in PhyPiConfDict:
      PhyPiConfDict['Interval'] = self.interval
    else:
      self.interval = PhyPiConfDict['Interval']
    if PhyPiConfDict['Interval'] < 0.05:
      print(" !!! read-out intervals < 0.05 s not reliable, setting to 0.05 s")
      PhyPiConfDict['Interval'] = 0.05

    if 'NHistoryPoints' not in PhyPiConfDict: # length of stored history
      PhyPiConfDict['NHistoryPoints'] = 120

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
    else:
      DevFiles = 'ADS1115Config.yaml'
      print("!!! no device config given - trying ADC ADS1115")

  # if not a list, make it one
    if type(DevFiles) != type([]):
      DevFiles = [DevFiles]
    NDevices = len(DevFiles)

    # open all device config files
    DEVconfDicts = []
    for fnam in DevFiles:  
      try:
        f = open(fnam)
        DEVconfDicts.append(yaml.load(f, Loader=yaml.Loader))
        f.close()
      except Exception as e:
        print('!!! failed to read configuration file ' + fnam)
        print(str(e))
        exit(1)

# configure and initialize all Devices
    DEVNames = []               # device names
    NHWChannels = 0             # total number of hardware channels
    ChanNams = []               # names of HW channels
    ChanUnits = []              # Units of HW channels
    ChanLims = []               # limits
    ChanIdx_ofDevice = []       # first channel of each device

    DEVs = []
    for i in range(NDevices):
      if 'DAQModule' in DEVconfDicts[i]:
        DEVNames.append(DEVconfDicts[i]['DAQModule'])
      else:  # try to derive from name of Device Config File
        cdir, cfnam = os.path.split(DeviceFiles[i])
        DEVNames.append(cfnam.split('.')[0])

      if self.verbose:  
        print('  configuring device ' + DEVNames[i])
      # import device class ...
      exec('from .' + DEVNames[i] +  ' import ' + DEVNames[i])
      # ...  and instantiate device handler
#      exec('global DEVs;  DEVs.append(' + DEVNames[i] + '(DEVconfDicts[i]) )' )
      exec('DEVs.append(' + DEVNames[i] + '(DEVconfDicts[i]) )' )
      DEVs[i].init()
      ChanIdx_ofDevice.append(NHWChannels)
      nC = DEVs[i].NChannels  
      NHWChannels += nC
      ChanNams += DEVs[i].ChanNams[0 : nC]
      ChanLims += DEVs[i].ChanLims[0 : nC]
      try:
        ChanUnits += DEVs[i].ChanUnits[0 : nC]
      except:
        ChanUnits = None

    self.DEVs = DEVs
    self.ChanIdx_ofDevice = ChanIdx_ofDevice 
    self.ChanLims = ChanLims
    self.ChanNams = ChanNams
    self.ChanUnits = ChanUnits
    self.NHWChannels = NHWChannels
      
  # set up calibration Functions
    CalibFuncts = None
    if 'ChanCalib' in PhyPiConfDict:
      CalibFuncts = [None] * NHWChannels    
      calibData = PhyPiConfDict['ChanCalib']
      if self.verbose > 1:
        print('  Calibrating channels:')   
        for ic in range( NHWChannels): 
          print('   Chan ', ic, '   ', calibData[ic])   
      for ic in range( NHWChannels): 
        if calibData[ic] is not None: 
          CalibFuncts[ic] = generateCalibrationFunction(calibData[ic])
    self.CalibFuncts = CalibFuncts
    
  # Apply Formula(e) to calibrated channel reading(s)
    Formulae = None
    NFormulae = 0
    if 'ChanFormula' in PhyPiConfDict:
      Formulae = PhyPiConfDict['ChanFormula']
      NFormulae = len(Formulae)
      if self.verbose > 1:
        print('applying fromulae:')
        for ifc in range( NFormulae): 
          if Formulae[ifc]: print('   FChan ', ifc, '   ', Formulae[ifc])   
    self.Formulae = Formulae
    self.NFormulae = NFormulae
    # re-set number of Channels if Formulae are defined       
    nc = NFormulae if NFormulae else NHWChannels
    PhyPiConfDict['NChannels'] = nc
    
  # Add information for graphical display(s) to PhyPiConfDict
    if 'ChanNams' not in PhyPiConfDict:
      if NFormulae > NHWChannels:
        self.ChanNams += (NFormulae-NHWChannels) * ['F']
      else:
        self.ChanNams = self.ChanNams[:nc] 
      for ifc in range( NFormulae): 
        if Formulae[ifc]: self.ChanNams[ifc] = 'F' + str(ifc)
      PhyPiConfDict['ChanNams' ] = self.ChanNams 

    if 'ChanUnits' not in PhyPiConfDict:
      if self.ChanUnits is not None:
        PhyPiConfDict['ChanUnits' ] = self.ChanUnits
      else:
        PhyPiConfDict['ChanUnits' ] = [''] * nc 
    l = len(PhyPiConfDict['ChanUnits']) 
    if l < nc:
      PhyPiConfDict['ChanUnits'] += (nc-l) * ['']

    if 'ChanLabels' not in PhyPiConfDict:
      PhyPiConfDict['ChanLabels' ] = [''] * nc 
    else:
      l = len(PhyPiConfDict['ChanLabels'])
      if l < nc:
        PhyPiConfDict['ChanLabels'] += (nc-l) * ['']

    if 'ChanLimits' not in PhyPiConfDict:
      if NFormulae > 0:
        print('PhyPiDAQ: forumla(e) defined, but no ChanLimits supplied ')  
        print('     results may become unpredictable - exiting')  
        exit(1)
      PhyPiConfDict['ChanLimits'] = ChanLims # take from hw devices if not set
      
  # start data recording to disk if required
    if PhyPiConfDict['DataFile'] is not None:
      FName = PhyPiConfDict['DataFile']
      self.DatRec = DataRecorder(FName, PhyPiConfDict)
      if self.verbose:  print('  storing data to file ',FName)
    else:
      self.DatRec = None
      PhyPiConfDict['DataFile'] = self.DatRec

  # buffer latest data (number of data points given by NHistoryPoints)
    if 'bufferData' in PhyPiConfDict:
      self.bufferFile = PhyPiConfDict['bufferData']      
    else:
      self.bufferFile = "PhyPiData"
      PhyPiConfDict['bufferData'] = self.bufferFile     
    # set-up a ring buffer 
    if self.bufferFile is not None:    
      self.RBuf = RingBuffer(PhyPiConfDict['NHistoryPoints'])
    else:
      self.RBuf = None

  # configure a fifo for data output
    if 'DAQfifo' in PhyPiConfDict:
      self.DAQfifo = PhyPiConfDict['DAQfifo']      
    else:
      self.DAQfifo = None
      PhyPiConfDict['DAQfifo'] = self.DAQfifo
    if self.DAQfifo:
      print('PhyPiDAQ: opening fifo ', self.DAQfifo)
      try:
        os.mkfifo(self.DAQfifo)
      except OSError as e:
        if e.errno != errno.EEXIST: raise
      self.fifo = open(self.DAQfifo, 'w', 1)
    else:
      self.fifo = None

  # LED indicators on GPIO pins
    if 'RunLED' in PhyPiConfDict or 'ReadoutLED' in PhyPiConfDict:      
      from .pulseGPIO import pulseGPIO
    if 'RunLED' in PhyPiConfDict:      
      self.RunLED = pulseGPIO(PhyPiConfDict['RunLED'])
    else:
      self.RunLED = None
    if 'ReadoutLED' in PhyPiConfDict:      
      self.ReadoutLED = pulseGPIO(PhyPiConfDict['ReadoutLED'])
    else:
      self.ReadoutLED = None
      
 # print configuration
    if self.verbose > 1:
      print ('\nPhyPiDAQ Configuration:')
      print (yaml.dump(PhyPiConfDict) )
    self.PhyPiConfDict = PhyPiConfDict


  def apply_calibs(self):
    '''
      apply calibration functions to hardware channels    

      input: Calibration Functions as calucated by 
             generateCalibrationFunctions() from interpolated 
             values in calibration table calibData[]

      output: calibrated channel values
    '''

    for i in range(self.NHWChannels):
      if self.CalibFuncts[i] is not None:
        self.data[i] = self.CalibFuncts[i](self.data[i])

  def apply_formulae(self):
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
    #for ifc in range(self.NFormulae):
    for ifc in range(self.NHWChannels):
      exec('c'+str(ifc) + ' = self.data['+str(ifc)+']')
      
    #  apply formulae to signal data
    for ifc in range(self.NFormulae):
      if self.Formulae[ifc] is not None:
        self.data[ifc] = eval(self.Formulae[ifc])

  
  def run(self):
    ''' run data acquisition as defined in configuration files
    '''  

    if self.verbose:
      print('*==* script ' + sys.argv[0] + ': data taking active \n')

    longInterval = 5. # definiton of a "long" readout interval

    interval = self.PhyPiConfDict['Interval']
    NChannels = self.PhyPiConfDict['NChannels']
    DisplayModule = self.PhyPiConfDict['DisplayModule']

    cmdQ =  mp.Queue(1) # Queue for command input
    datQ =  mp.Queue(1) # Queue to spy on data transfer inside class Display
    if 'startActive' not in self.PhyPiConfDict:  
      self.PhyPiConfDict['startActive'] = False  # start in paused-mode
    if 'DAQCntrl' not in self.PhyPiConfDict:  
      self.PhyPiConfDict['DAQCntrl'] = True  # enable run control buttons

    if DisplayModule is not None:  
      display = Display(interval = None, 
                    confdict = self.PhyPiConfDict, 
                    cmdQ = cmdQ,
                    datQ = datQ )
      display.init()

    self.ACTIVE = True #  background process(es) active

    if self.PhyPiConfDict['startActive']:
      self.DAQ_ACTIVE = True # Data Acquisition active
    else:
  # start in paused-mode
      self.DAQ_ACTIVE = False # Data Acquisition inactive
      print('  starting in Paused mode - type R to resume')

  # start keyboard control
    kbdthrd=threading.Thread(name='kbdInput', target = self.kbdInput,
                             args = (cmdQ,)  )
#                                    Queue       
    kbdthrd.daemon = True
    kbdthrd.start()  

    # set up space for data
    self.data = np.zeros(max(NChannels, self.NHWChannels))

    tflash = min(0.2, interval/2.) # pulse duration for readout LED
    if self.RunLED: self.RunLED.pulse(0) # switch on status LED
  # -- LOOP 
    try:
      cnt = 0
      T0 = time.time()
      brk = False

      wait = DAQwait(interval) # initialize wait timer
      
      while self.ACTIVE:
         
        # regularly check for command input for long intervals
        if interval > longInterval and self.DAQ_ACTIVE:
          cmd = 0 
          while not datQ.empty():  # check for command input
            if not cmdQ.empty():
              cmd = self.decodeCommand(cmdQ)  
              if cmd: break # got valid command
            time.sleep(longInterval/300.)
          if cmd >= 2: break  # end command received

        if self.DAQ_ACTIVE:
          cnt +=1
        # read data
          for i, DEV in enumerate(self.DEVs):
            DEV.acquireData(self.data[self.ChanIdx_ofDevice[i] : ] )

          if self.ReadoutLED: self.ReadoutLED.pulse(tflash) # pulse readout LED

        # eventually calibrate raw readings
          if self.CalibFuncts: self.apply_calibs()

        # eventualy apply fromula(e) 
          if self.Formulae: self.apply_formulae()

        # display data
          if DisplayModule is not None:  
            display.show(self.data[:NChannels])

        # store (latest) data in ring buffer as a list ...
          if self.RBuf is not None:
            self.RBuf.store( self.data[:NChannels].tolist())

        # ... and record all data to disc ...
          if self.DatRec: self.DatRec(self.data[:NChannels])

        # ... and write to fifo
          if self.fifo:
            print(','.join(['{0:.3f}'.format(cnt*interval)] +
                  ['{0:.4g}'.format(d) for d in self.data[:NChannels]]),
                  file = self.fifo)

          wait() #

        else:   # paused mode
          time.sleep( min(interval/10., 0.2) )

        # check for control input (from keyboard or display module)
        if not cmdQ.empty(): self.decodeCommand(cmdQ)
      
      # -- end while ACITVE 


    except KeyboardInterrupt:
      self.DAQ_ACTIVE = False     
      self.ACTIVE = False
      print('\n' + sys.argv[0] +': keyboard interrupt - closing down ...')

    except:
      # 'except Exception as e' leaves some errors unnoted
      print('\n!!! ' + sys.argv[0] + ': exception in data-taking loop' )
      print(sys.exc_info()[1])

    finally:
      self.ACTIVE = False
      if self.RunLED is not None: self.RunLED.pulse(-1) # RunLED off 
      if self.DatRec: self.DatRec.close()
      for DEV in self.DEVs:
        DEV.closeDevice() # close down hardware device
      if DisplayModule is not None: display.close()
      if self.RunLED is not None: self.RunLED.close() 
      if self.ReadoutLED is not None: self.ReadoutLED.close() 
      time.sleep(1.)
     
      if self.verbose:
        print('\n*==* ' + sys.argv[0] + ': normal end - type <ret>')
      sys.exit()

# execute only if called directly, but not when imported
if __name__ == "__main__": # - - - - - - - - - - - - - - - - - - - - - -

  daq = runPhyPiDAQ()
  daq.setup() 
  daq.run()
