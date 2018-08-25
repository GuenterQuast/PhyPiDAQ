#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''Data visualisation
     this script reads data samples from PicoScope and 
     displays data as effective voltage, history display and xy plot

     Usage: ./runPicoScope_demo.py [Interval <PhyPiConf_file>.yaml]
'''

from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import sys, time, yaml, numpy as np, threading, multiprocessing as mp
sys.path.append('..')


# display module
from phypidaq.mpTkDisplay import mpTkDisplay

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

def stop_processes(proclst):
  '''
    Close all running processes at end of run
  '''
  for p in proclst: # stop all sub-processes
    if p.is_alive():
      print('    terminating '+p.name)
      if p.is_alive(): p.terminate()
      time.sleep(1.)

def setup():
# set up data source, display module and options

  global interval, PhyPiConfDict, DEVs, ChanIdx_ofDevice, DatRec 

# check for / read command line arguments
  if len(sys.argv) >=3:
    interval = float(sys.argv[2])
  else: 
    interval = 0.5

  # read PhyPicDAQ configuration file
  if len(sys.argv) >= 2:
    PhyPiConfFile = sys.argv[1]
  else:
    PhyPiConfFile = 'PhyPiConf.daq'

  # read DAQ configuration file
  print('  Configuration from file ' + PhyPiConfFile)
  try:
    with open(PhyPiConfFile) as f:
      PhyPiConfDict = yaml.load(f)
  except:
    print('!!! failed to read configuration file ' + PhyPiConfFile)
    print('   using default settings')
  # define default config dictionary
    PhyPiConfDict={}
    PhyPiConfDict['DeviceFile'] = 'ADS1115Config.yaml'
    PhyPiConfDict['ChanLabels'] = ['(V)', '(V)']  
    PhyPiConfDict['ChanColors'] = ['darkblue', 'sienna'] 

# set default options:
  if 'Interval' not in PhyPiConfDict:
    PhyPiConfDict['Interval'] = interval
  if PhyPiConfDict['Interval'] < 0.05:
    print(" !!! read-out intervals < 0.05 s not reliable, setting to 0.05 s")
    PhyPiConfDict['Interval'] = 0.05

  if 'XYmode' not in PhyPiConfDict:
    PhyPiConfDict['XYmode'] = False

  if 'DataFile' not in PhyPiConfDict:
    PhyPiConfDict['DataFile'] = None

  if 'DisplayModule' not in PhyPiConfDict:
    PhyPiConfDict['DisplayModule'] = 'DataLogger'

# read Device configuration(s) and instantiate device handler(s)
  if 'DeviceFile' in PhyPiConfDict:
    DevFiles = PhyPiConfDict['DeviceFile']
  elif "DAQModule" in phypiConfD: 
    DevFiles = phypiConfD["DAQModule"] + '.yaml' 
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
    except:
      print('!!! failed to read configuration file ' + fnam)
      exit(1)

# configure and initialize all Devices
  DEVNames = []
  NChannels = 0
  ChanNams = []
  ChanLims = []
  ChanIdx_ofDevice = []

  DEVs = []
  for i in range(NDevices):
    if 'DAQModule' in DEVconfDicts[i]:
      DEVNames.append(DEVconfDicts[i]['DAQModule'])
    elif 'DAQModule' in PhyPiConfDict:
      DEVNames.append(PhyPiConfDict['DAQModule'][i])
    else:  # try to derive from name of Device Config File
      DEVNames.append(DevFiles[i].split('.')[0])

    print('  configuring device ' + DEVNames[i])
    # import device class ...
    exec('from phypidaq.' + DEVNames[i] +  ' import ' + DEVNames[i])
    # ...  and instantiate device handler
    exec('global DEVs;  DEVs.append(' + DEVNames[i] + '(DEVconfDicts[i]) )' )
    DEVs[i].init()
    ChanIdx_ofDevice.append(NChannels)
    nC = DEVs[i].NChannels  
    NChannels += nC
    ChanNams += DEVs[i].ChanNams[0 : nC]
    ChanLims += DEVs[i].ChanLims[0 : nC]

# Add information for graphical display(s) to PhyPiConfDict
  PhyPiConfDict['NChannels'] = NChannels
  if 'ChanNams' not in PhyPiConfDict:
    PhyPiConfDict['ChanNams' ] = ChanNams 
  if 'ChanLimits' not in PhyPiConfDict:  
    PhyPiConfDict['ChanLimits'] = ChanLims # take from devices if not set

  if PhyPiConfDict['DataFile'] != None:
    FName = PhyPiConfDict['DataFile']
    from phypidaq.DataRecorder import DataRecorder
    DatRec = DataRecorder(FName, PhyPiConfDict)
  else:
    DatRec = None

  print ('\nPhyPiDAQ Configuration:')
  print (yaml.dump(PhyPiConfDict) )


if __name__ == "__main__": # - - - - - - - - - - - - - - - - - - - - - -

  print('\n*==* script ' + sys.argv[0] + ' running \n')

  setup()
  NChannels = PhyPiConfDict['NChannels']
  DisplayModule = PhyPiConfDict['DisplayModule']

  thrds=[]
  procs=[]
  cmdQ =  mp.Queue(1) # Queue for command input

  DLmpQ = mp.Queue(1) # Queue for data transfer to sub-process
  procs.append(mp.Process(name='DataLogger', target = mpTkDisplay, 
             args=(DLmpQ, PhyPiConfDict, DisplayModule , cmdQ) ) )
#                   Queue    config        ModuleName    commandQ

# mulit-graph display:
#  DGmpQ =  mp.Queue(1) # Queue for data transfer to sub-process
#  procs.append(mp.Process(name='DataGraphs', target = mpTkDisplay, 
#    args=(DGmpQ, PhyPiConfDict, 'DataGraphs', cmdQ) ) )
#         Queue     config       ModuleName  CommandQ

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
        for i, DEV in enumerate(DEVs):
          DEV.acquireData(sig[ChanIdx_ofDevice[i]:])
        DLmpQ.put(sig)  # for DataLogger
#        DGmpQ.put(sig)  # for DataGraphs
        if DatRec: DatRec(sig) # for data recorder
   # check for keboard input
      if not cmdQ.empty():
        cmd = cmdQ.get()
        if cmd == 'E':
          #DGmpQ.put(None)       # send empty "end" event
          print('\n' + sys.argv[0] + ': End command recieved - closing down')
          ACTIVE = False
          break
        elif cmd == 'P':
          DAQ_ACTIVE = False     
        elif cmd == 'R':
          DAQ_ACTIVE = True
        elif cmd == 's':  
          #DGmpQ.put(None)       # send empty "end" event
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
    if DatRec: DatRec.close()
    DEV.closeDevice() # close down hardware device
    time.sleep(1.)
    stop_processes(procs)  # stop all sub-processes in list
    print('*==* ' + sys.argv[0] + ': normal end')
