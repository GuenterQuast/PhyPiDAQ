# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import numpy as np, time, sys

# code for Bosch BMP280 temperature and pressure sensor below

#DEVICE = 0x77 # Default device I2C address
DEVICE = 0x76 # alternative device I2C address


class BMP280Config(object):
  '''digital thermometer DS18B20Config configuration and interface'''

  def __init__(self, confdict = None):
    if confdict==None: confdict={}
          
# -- number of Channels
    self.NChannels = 2
    self.ChanLims = [[-40., 85.],[300., 1100.], [0., 100.]]
    self.ChanNams = ['T','P', 'H']
    self.ChanUnits= ['°C','hPa', '%']


  def init(self):

    try:
      self.sensor = BMP280(DEVICE)
    except Exception as e:      
       print("BMP280: Error setting up device - exit")
       print(str(e))
       sys.exit(1)
    try:
      self.sensor.init()
    except Exception as e:      
       print("BMP280: Error initialising device - exit")
       print(str(e))
       sys.exit(1)
      
  def acquireData(self, buf):
    buf[0], p, h = self.sensor.readAll()
    if self.NChannels > 1:
      buf[1] = p # in hPa
    if self.NChannels > 2:
      buf[2] = h # humidity

  def closeDevice(self):
   # nothing to do here
    pass


# driver code for BMP280, 
#   adapted from original code by Matt Hawkins

#--------------------------------------
import smbus
from ctypes import c_short
from ctypes import c_byte
from ctypes import c_ubyte

# some helper functions
def getShort(data, index):
  # return two bytes from data as a signed 16-bit value
  return c_short((data[index+1] << 8) + data[index]).value

def getUShort(data, index):
  # return two bytes from data as an unsigned 16-bit value
  return (data[index+1] << 8) + data[index]

def getChar(data,index):
  # return one byte from data as a signed char
  result = data[index]
  if result > 127:
    result -= 256
  return result

def getUChar(data,index):
  # return one byte from data as an unsigned char
  result =  data[index] & 0xFF
  return result


# Control Registers of BMP280
REG_ID     = 0xD0
# Register Addresses
REG_DATA = 0xF7
REG_CONTROL = 0xF4
REG_CONFIG  = 0xF5

REG_CONTROL_HUM = 0xF2
REG_HUM_MSB = 0xFD
REG_HUM_LSB = 0xFE

# Oversample setting - page 27
OVERSAMPLE_TEMP = 2
OVERSAMPLE_PRES = 2
MODE = 1

# Oversample setting for humidity register - page 26
OVERSAMPLE_HUM = 2


class BMP280(object):
  """Class to represent the Bosch BMP280 temperature and pressure sensor
  """

  def __init__(self, addr=0x77):
    self.DEVICE = addr

    self.bus = smbus.SMBus(1) # Rev 2 Pi, Pi 2 & Pi 3 uses bus 1
                     # Rev 1 Pi uses bus 0
    (chip_id, chip_version) = self.bus.read_i2c_block_data(addr, REG_ID, 2)
    print("BMP280: Chip ID ", chip_id)
    print("BMP208: Version ", chip_version)

  def init(self):

    self.bus.write_byte_data(self.DEVICE, REG_CONTROL_HUM, OVERSAMPLE_HUM)

    control = OVERSAMPLE_TEMP<<5 | OVERSAMPLE_PRES<<2 | MODE
    self.bus.write_byte_data(self.DEVICE, REG_CONTROL, control)

    # Read blocks of calibration data from EEPROM
    # See Page 22 data sheet
    cal1 = self.bus.read_i2c_block_data(self.DEVICE, 0x88, 24)
    cal2 = self.bus.read_i2c_block_data(self.DEVICE, 0xA1, 1)
    cal3 = self.bus.read_i2c_block_data(self.DEVICE, 0xE1, 7)

    # Convert byte data to word values
    self.dig_T1 = getUShort(cal1, 0)
    self.dig_T2 = getShort(cal1, 2)
    self.dig_T3 = getShort(cal1, 4)

    self.dig_P1 = getUShort(cal1, 6)
    self.dig_P2 = getShort(cal1, 8)
    self.dig_P3 = getShort(cal1, 10)
    self.dig_P4 = getShort(cal1, 12)
    self.dig_P5 = getShort(cal1, 14)
    self.dig_P6 = getShort(cal1, 16)
    self.dig_P7 = getShort(cal1, 18)
    self.dig_P8 = getShort(cal1, 20)
    self.dig_P9 = getShort(cal1, 22)

    self.dig_H1 = getUChar(cal2, 0)
    self.dig_H2 = getShort(cal3, 0)
    self.dig_H3 = getUChar(cal3, 2)
    self.dig_H4 = getChar(cal3, 3)
    self.dig_H4 = (self.dig_H4 << 24) >> 20
    self.dig_H4 = self.dig_H4 | (getChar(cal3, 4) & 0x0F)
    self.dig_H5 = getChar(cal3, 5)
    self.dig_H5 = (self.dig_H5 << 24) >> 20
    self.dig_H5 = self.dig_H5 | (getUChar(cal3, 4) >> 4 & 0x0F)
    self.dig_H6 = getChar(cal3, 6)

    # Wait in ms (Datasheet Appendix B: Measurement time and current calculation)
    wait_time = 1.25 + (2.3 * OVERSAMPLE_TEMP) + ((2.3 * OVERSAMPLE_PRES) + 0.575) + ((2.3 * OVERSAMPLE_HUM)+0.575)
    time.sleep(wait_time/1000)  # Wait the required time  

  def readAll(self):

    # Read temperature/pressure/humidity
    data = self.bus.read_i2c_block_data(self.DEVICE, REG_DATA, 8)
    pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
    temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
    hum_raw = (data[6] << 8) | data[7]

    #Refine temperature
    var1 = ((((temp_raw>>3)-(self.dig_T1<<1)))*(self.dig_T2)) >> 11
    var2 = (((((temp_raw>>4) - (self.dig_T1)) * ((temp_raw>>4) - (self.dig_T1))) >> 12) * (self.dig_T3)) >> 14
    t_fine = var1+var2
    t = float(((t_fine * 5) + 128) >> 8);

    # Refine pressure and adjust for temperature
    var1 = t_fine / 2.0 - 64000.0
    var2 = var1 * var1 * self.dig_P6 / 32768.0
    var2 = var2 + var1 * self.dig_P5 * 2.0
    var2 = var2 / 4.0 + self.dig_P4 * 65536.0
    var1 = (self.dig_P3 * var1 * var1 / 524288.0 + self.dig_P2 * var1) / 524288.0
    var1 = (1.0 + var1 / 32768.0) * self.dig_P1
    if var1 == 0:
      p=0
    else:
      p = 1048576.0 - pres_raw
      p = ((p - var2 / 4096.0) * 6250.0) / var1
      var1 = self.dig_P9 * p * p / 2147483648.0
      var2 = p * self.dig_P8 / 32768.0
      p = p + (var1 + var2 + self.dig_P7) / 16.0

    # Refine humidity
    h = t_fine - 76800.0
    h = (hum_raw - (self.dig_H4 * 64.0 + self.dig_H5 / 16384.0 * h)) 
    h = h * (self.dig_H2 / 65536.0 * (1.0 + self.dig_H6 / 67108864.0 * h * (1.0 + self.dig_H3 / 67108864.0 * h)))
    h = h * (1.0 - self.dig_H1 * h / 524288.0)
    if h > 100:
      h = 100
    elif h < 0:
      h = 0.

    return t/100.0, p/100.0, h
