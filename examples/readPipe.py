#!/usr/bin/python3
# -*- coding: utf-8 -*-
''' script readPipe.py
    usage: readPipe [name of pipe]

    Read data from a named linux pipe 
    filled by run_phypi.py with option 
    DAQfifo: <name of pipe>
'''

import sys, os, errno

if len(sys.argv)>=2:
  FiFo = sys.argv[1]
else:
  FiFo = "PhyPiDAQ.fifo"
print('*==* ', sys.argv[0], ' Lese Daten aus Pipe',  FiFo)
  
# crate a fifo, ignore error if it already exists
try:
  os.mkfifo(FiFo)
except OSError as e:
  if e.errno != errno.EEXIST:
    raise

# with os.open(FiFo, os.O_RDONLY | os.O_NONBLOCK) as f:
with open(FiFo) as f:
  #inp = f.read()  f.readline()
  for inp in f:
   if inp == '\n':
     print("empty input - closing")
     break    
   print('Read: %s '%inp, end='')
      
print('        empty line received, ending')
      
