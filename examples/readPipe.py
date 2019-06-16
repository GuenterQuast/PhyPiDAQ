#!/usr/bin/python3
# -*- coding: utf-8 -*-
''' script readPipe 
    usage: readPipe
'''

import sys, os, errno

FiFo = "PhyPiDAQ.fifo"

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
      
      
