# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

'''
  interface for FTLAB GDK 101 gamma radiation detector

    attention: I²C interface needs level shifter 5.0 <-> 3.3 V 
'''

import numpy as np, time, sys
from smbus2 import SMBus

# default addresses
I2CADDR  = 0x18

# code of driver classes included below

class GDK101Config(object):
  '''interface for GDK101 gamma detector
    1st channel: 1 min av
    2nd channel: 10 min sliding average
  '''
  
  def __init__(self, confdict = None):
    self.I2CADDR = I2CADDR
    if confdict==None: confdict={}
    if 'I2CADDR' in confdict:
      self.I2CADDR = confdict['I2CADDR']
      print("GDK101: I2C address set to %x "%(self.I2CADDR) )
    if 'NChannels' in confdict:
      self.NChannels = confdict["NChannels"]
    else:
      self.NChannels = 1
    self.ChanLims = [[0, 200.],[0., 200.]]
    self.ChanNams = ['D', 'D']
    self.ChanUnits= ['µSv','µSv']

  def init(self):
    '''init sensor'''
    try:
      busnum = 1
      self.sensor = GDK101(busnum, self.I2CADDR) 
      print("GDK101: sensor found, firmware version ", self.sensor.version())
    except Exception as e:      
       print("GDK101: Error setting up device - exit")
       print(str(e))
       sys.exit(1)
      
  def acquireData(self, buf):
    '''read data from sensor'''
    buf[0] = self.sensor.read1()
    if self.NChannels > 1:
      buf[1] = self.sensor.read10()

  def closeDevice(self):
    self.sensor.close()

## ----- driver section -----------
# GDK101 has a very simple I²C interface
#   list of valid commands
CMD_reset = 0xA0 # reset 
CMD_status = 0xB0 # reset 
CMD_firmware = 0xB4  # read firmware
CMD_measuringTime = 0xB1  # read measurement time
CMD_readDose10 = 0xB2  # 10 min average, 1 min update
CMD_readDose1 = 0xB3  # 1 min average

class GDK101(object):
  '''driver code for GDK101 gamma ray sensor'''

  def __init__(self, busnum, addr):
    self.bus = SMBus(busnum)
    self.addr = addr
    rc = self.reset()
    if rc != 1: # reset failed
      raise Exception('GKD101: failed to reset sensor')
      
  def _readGKD101(self, cmd):
    '''implement simple I²C interface of GDK101
       - send command
       - block-read two bytes
    '''
    self.bus.write_byte_data(self.addr, 0 , cmd)
    return self.bus.read_i2c_block_data(self.addr, 0, 2)

  def reset(self):
    d = self._readGKD101(CMD_reset)
    return d[0]
  
  def read1(self):
    ''' read 1 min average'''
    d = self._readGKD101(CMD_readDose1)
    return d[0]+d[1]/100.
  
  def read10(self):
    ''' read 10 min sliding average'''
    d = self._readGKD101(CMD_readDose10)
    return d[0]+d[1]/100.
 
  def version(self):
    '''return firmware version'''
    fw = self._readGKD101(CMD_firmware)
    return str(fw[0]+fw[1]/10.)

  def close(self):
    '''close bus'''
    self.bus.close()
    
