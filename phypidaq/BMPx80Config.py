# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import numpy as np, time, sys, smbus

# default addresses and ChipIDs of Bosch BMP 085/180 and BMP/E 280 sensors
BMP_I2CADDR  = 0x77
BMP_I2CADDR2 = 0x76
#BMP_I2CADDR = 0x76 # alternative device I2C address
BMP180_CHIPID = 0x55
BMP280_CHIPID = 0x58
BME280_CHIPID = 0x60
# ID register:
REG_ID = 0xD0

# code of driver classes included below

class BMPx80Config(object):
  '''digital thermometer DS18B20Config configuration and interface'''
  def __init__(self, confdict = None):
    self.BMP_I2CADDR = BMP_I2CADDR
    if confdict==None: confdict={}
    if 'I2CADDR' in confdict:
      self.BMP_I2CADDR = confdict['I2CADDR']
      print("BMPx80: I2C address set to %x "%(self.BMP_I2CADDR) )
    if 'NChannels' in confdict:
      self.NChannels = confdict["NChannels"]
    else:
      self.NChannels = 2
    self.ChanLims = [[-40., 85.],[300., 1100.], [0., 100.]]
    self.ChanNams = ['T','P', 'H']
    self.ChanUnits= ['°C','hPa', '%']

  def init(self):
    try:
      # set up I2C bus
      busnum = 1
      bus = smbus.SMBus(busnum) # Rev 2 Pi, Pi 2 & Pi 3 uses bus 1
                                # Rev 1 Pi uses bus 0
    except Exception as e:      
       print("BMPx80: Error initialising I2C bus - exit")
       print(str(e))
       sys.exit(1)

    try:
      try:
      # find out which sensor we have:
        (self.chipID,) = bus.read_i2c_block_data(self.BMP_I2CADDR, REG_ID, 1)
      except:
      # try secondary address (BMP280)
        print("BMPx80: trying secondary address %x "%(BMP_I2CADDR2) )
        (self.chipID,) = bus.read_i2c_block_data(BMP_I2CADDR2, REG_ID, 1)
        self.BMP_I2CADDR = BMP_I2CADDR2

      # set up sensor
      print("BMPx80: ChipID %x "%(self.chipID) )
      if self.chipID == BMP180_CHIPID:
        self.sensor = BMP085(address=self.BMP_I2CADDR, busnum=busnum, i2c_interface=smbus.SMBus)
      elif self.chipID == BMP280_CHIPID:
        self.sensor = BMP280(address=self.BMP_I2CADDR, busnum=busnum, i2c_interface=smbus.SMBus)
      elif self.chipID == BME280_CHIPID:
        self.sensor = BME280(address=self.BMP_I2CADDR, i2c = bus)
      else:
       print("BMPx80: unknown chip ID - exiting")
       sys.exit(1)
    except Exception as e:      
       print("BMPx80: Error setting up device - exit")
       print(str(e))
       sys.exit(1)
      
  def acquireData(self, buf):

    if self.chipID == BME280_CHIPID:
      buf[0], p, h = self.sensor.readAll() # temp., press., hum.
      if self.NChannels > 1:
        buf[1] = p
      if self.NChannels > 2:
        buf[2] = h
    else:
      buf[0] = self.sensor.read_temperature() # in degC
      if self.NChannels > 1:
        buf[1] = self.sensor.read_pressure()/100. # in hPa

  def closeDevice(self):
   # nothing to do here
    pass

## ----- driver section -----------

# driver code for BMP085/180, 
#   adapted from original code by Tony DiCola, (c) Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Operating Modes
BMP085_ULTRALOWPOWER     = 0
BMP085_STANDARD          = 1
BMP085_HIGHRES           = 2
BMP085_ULTRAHIGHRES      = 3

# BMP085 Registers
BMP085_CAL_AC1           = 0xAA  # R   Calibration data (16 bits)
BMP085_CAL_AC2           = 0xAC  # R   Calibration data (16 bits)
BMP085_CAL_AC3           = 0xAE  # R   Calibration data (16 bits)
BMP085_CAL_AC4           = 0xB0  # R   Calibration data (16 bits)
BMP085_CAL_AC5           = 0xB2  # R   Calibration data (16 bits)
BMP085_CAL_AC6           = 0xB4  # R   Calibration data (16 bits)
BMP085_CAL_B1            = 0xB6  # R   Calibration data (16 bits)
BMP085_CAL_B2            = 0xB8  # R   Calibration data (16 bits)
BMP085_CAL_MB            = 0xBA  # R   Calibration data (16 bits)
BMP085_CAL_MC            = 0xBC  # R   Calibration data (16 bits)
BMP085_CAL_MD            = 0xBE  # R   Calibration data (16 bits)
BMP085_CONTROL           = 0xF4
BMP085_TEMPDATA          = 0xF6
BMP085_PRESSUREDATA      = 0xF6

# Commands
BMP085_READTEMPCMD       = 0x2E
BMP085_READPRESSURECMD   = 0x34


class BMP085(object):
    def __init__(self, mode=BMP085_STANDARD, address=BMP_I2CADDR, i2c=None, busnum=1, i2c_interface=None):
        # Check that mode is valid.
        if mode not in [BMP085_ULTRALOWPOWER, BMP085_STANDARD, BMP085_HIGHRES, BMP085_ULTRAHIGHRES]:
            raise ValueError('Unexpected mode value {0}.  Set mode to one of ' + 
              'BMP085_ULTRALOWPOWER, BMP085_STANDARD, BMP085_HIGHRES, or BMP085_ULTRAHIGHRES'.format(mode))
        self._mode = mode
        # Create I2C device.
        if i2c is None:
            import Adafruit_GPIO.I2C as I2C
            i2c = I2C

        self._device = i2c.get_i2c_device(address, busnum=busnum, i2c_interface=i2c_interface)
        # Load calibration values.
        self._load_calibration()

    def _load_calibration(self):
        self.cal_AC1 = self._device.readS16BE(BMP085_CAL_AC1)   # INT16
        self.cal_AC2 = self._device.readS16BE(BMP085_CAL_AC2)   # INT16
        self.cal_AC3 = self._device.readS16BE(BMP085_CAL_AC3)   # INT16
        self.cal_AC4 = self._device.readU16BE(BMP085_CAL_AC4)   # UINT16
        self.cal_AC5 = self._device.readU16BE(BMP085_CAL_AC5)   # UINT16
        self.cal_AC6 = self._device.readU16BE(BMP085_CAL_AC6)   # UINT16
        self.cal_B1 = self._device.readS16BE(BMP085_CAL_B1)     # INT16
        self.cal_B2 = self._device.readS16BE(BMP085_CAL_B2)     # INT16
        self.cal_MB = self._device.readS16BE(BMP085_CAL_MB)     # INT16
        self.cal_MC = self._device.readS16BE(BMP085_CAL_MC)     # INT16
        self.cal_MD = self._device.readS16BE(BMP085_CAL_MD)     # INT16

    def _load_datasheet_calibration(self):
        # Set calibration from values in the datasheet example.  Useful for debugging the
        # temp and pressure calculation accuracy.
        self.cal_AC1 = 408
        self.cal_AC2 = -72
        self.cal_AC3 = -14383
        self.cal_AC4 = 32741
        self.cal_AC5 = 32757
        self.cal_AC6 = 23153
        self.cal_B1 = 6190
        self.cal_B2 = 4
        self.cal_MB = -32767
        self.cal_MC = -8711
        self.cal_MD = 2868

    def read_raw_temp(self):
        """Reads the raw (uncompensated) temperature from the sensor."""
        self._device.write8(BMP085_CONTROL, BMP085_READTEMPCMD)
        time.sleep(0.005)  # Wait 5ms
        raw = self._device.readU16BE(BMP085_TEMPDATA)
        return raw

    def read_raw_pressure(self):
        """Reads the raw (uncompensated) pressure level from the sensor."""
        self._device.write8(BMP085_CONTROL, BMP085_READPRESSURECMD + (self._mode << 6))
        if self._mode == BMP085_ULTRALOWPOWER:
            time.sleep(0.005)
        elif self._mode == BMP085_HIGHRES:
            time.sleep(0.014)
        elif self._mode == BMP085_ULTRAHIGHRES:
            time.sleep(0.026)
        else:
            time.sleep(0.008)
        msb = self._device.readU8(BMP085_PRESSUREDATA)
        lsb = self._device.readU8(BMP085_PRESSUREDATA+1)
        xlsb = self._device.readU8(BMP085_PRESSUREDATA+2)
        raw = ((msb << 16) + (lsb << 8) + xlsb) >> (8 - self._mode)
        return raw

    def read_temperature(self):
        """Gets the compensated temperature in degrees celsius."""
        UT = self.read_raw_temp()
        # Datasheet value for debugging:
        #UT = 27898
        # Calculations below are taken straight from section 3.5 of the datasheet.
        X1 = ((UT - self.cal_AC6) * self.cal_AC5) >> 15
        X2 = (self.cal_MC << 11) // (X1 + self.cal_MD)
        B5 = X1 + X2
        temp = ((B5 + 8) >> 4) / 10.0
        return temp

    def read_pressure(self):
        """Gets the compensated pressure in Pascals."""
        UT = self.read_raw_temp()
        UP = self.read_raw_pressure()
        # Datasheet values for debugging:
        #UT = 27898
        #UP = 23843
        # Calculations below are taken straight from section 3.5 of the datasheet.
        # Calculate true temperature coefficient B5.
        X1 = ((UT - self.cal_AC6) * self.cal_AC5) >> 15
        X2 = (self.cal_MC << 11) // (X1 + self.cal_MD)
        B5 = X1 + X2
        # Pressure Calculations
        B6 = B5 - 4000
        X1 = (self.cal_B2 * (B6 * B6) >> 12) >> 11
        X2 = (self.cal_AC2 * B6) >> 11
        X3 = X1 + X2
        B3 = (((self.cal_AC1 * 4 + X3) << self._mode) + 2) // 4
        X1 = (self.cal_AC3 * B6) >> 13
        X2 = (self.cal_B1 * ((B6 * B6) >> 12)) >> 16
        X3 = ((X1 + X2) + 2) >> 2
        B4 = (self.cal_AC4 * (X3 + 32768)) >> 15
        B7 = (UP - B3) * (50000 >> self._mode)
        if B7 < 0x80000000:
            p = (B7 * 2) // B4
        else:
            p = (B7 // B4) * 2
        X1 = (p >> 8) * (p >> 8)
        X1 = (X1 * 3038) >> 16
        X2 = (-7357 * p) >> 16
        p = p + ((X1 + X2 + 3791) >> 4)
        return p

    def read_altitude(self, sealevel_pa=101325.0):
        """Calculates the altitude in meters."""
        # Calculation taken straight from section 3.6 of the datasheet.
        pressure = float(self.read_pressure())
        altitude = 44330.0 * (1.0 - pow(pressure / sealevel_pa, (1.0/5.255)))
        return altitude

    def read_sealevel_pressure(self, altitude_m=0.0):
        """Calculates the pressure at sealevel when given a known altitude in
        meters. Returns a value in Pascals."""
        pressure = float(self.read_pressure())
        p0 = pressure / pow(1.0 - altitude_m/44330.0, 5.255)
        return p0

# driver code for BMP280  (Guenter Quast, 2018)
#  adapted vom code by Bastien Wirtz <bastien.wirtz@gmail.com>
#
# Based on the Adafruit BMP280 Driver C++ driver and the BMP085 python lib.
#  - https://github.com/adafruit/Adafruit_BMP280_Library
#  - https://github.com/adafruit/Adafruit_Python_BMP
#
# Datasheet: https://www.adafruit.com/datasheets/BST-BMP280-DS001-11.pdf

# BMP280 Registers
BMP280_DIG_T1 = 0x88  # R   Unsigned Calibration data (16 bits)
BMP280_DIG_T2 = 0x8A  # R   Signed Calibration data (16 bits)
BMP280_DIG_T3 = 0x8C  # R   Signed Calibration data (16 bits)
BMP280_DIG_P1 = 0x8E  # R   Unsigned Calibration data (16 bits)
BMP280_DIG_P2 = 0x90  # R   Signed Calibration data (16 bits)
BMP280_DIG_P3 = 0x92  # R   Signed Calibration data (16 bits)
BMP280_DIG_P4 = 0x94  # R   Signed Calibration data (16 bits)
BMP280_DIG_P5 = 0x96  # R   Signed Calibration data (16 bits)
BMP280_DIG_P6 = 0x98  # R   Signed Calibration data (16 bits)
BMP280_DIG_P7 = 0x9A  # R   Signed Calibration data (16 bits)
BMP280_DIG_P8 = 0x9C  # R   Signed Calibration data (16 bits)
BMP280_DIG_P9 = 0x9E  # R   Signed Calibration data (16 bits)

BMP280_CONTROL = 0xF4
BMP280_RESET = 0xE0
BMP280_CONFIG = 0xF5
BMP280_PRESSUREDATA = 0xF7
BMP280_TEMPDATA = 0xFA


class BMP280(object):
    def __init__(self, address=BMP_I2CADDR, i2c=None, busnum=1, i2c_interface= None):

        # Adadfruit I2C interface
        if i2c is None:
            import Adafruit_GPIO.I2C as I2C
            i2c = I2C

        self._device = i2c.get_i2c_device(address, 
                         busnum = busnum, i2c_interface = i2c_interface)

        if self._device.readU8(REG_ID) != BMP280_CHIPID:
            raise Exception('Unsupported chip')

        # Load calibration values.
        self._load_calibration()
        self._device.write8(BMP280_CONTROL, 0x3F)

    def _load_calibration(self):
        self.cal_t1 = int(self._device.readU16(BMP280_DIG_T1))  # UINT16
        self.cal_t2 = int(self._device.readS16(BMP280_DIG_T2))  # INT16
        self.cal_t3 = int(self._device.readS16(BMP280_DIG_T3))  # INT16
        self.cal_p1 = int(self._device.readU16(BMP280_DIG_P1))  # UINT16
        self.cal_p2 = int(self._device.readS16(BMP280_DIG_P2))  # INT16
        self.cal_p3 = int(self._device.readS16(BMP280_DIG_P3))  # INT16
        self.cal_p4 = int(self._device.readS16(BMP280_DIG_P4))  # INT16
        self.cal_p5 = int(self._device.readS16(BMP280_DIG_P5))  # INT16
        self.cal_p6 = int(self._device.readS16(BMP280_DIG_P6))  # INT16
        self.cal_p7 = int(self._device.readS16(BMP280_DIG_P7))  # INT16
        self.cal_p8 = int(self._device.readS16(BMP280_DIG_P8))  # INT16
        self.cal_p9 = int(self._device.readS16(BMP280_DIG_P9))  # INT16

    def _load_datasheet_calibration(self):
        # Set calibration from values in the datasheet example.  Useful for debugging the
        # temp and pressure calculation accuracy.
        self.cal_t1 = 27504
        self.cal_t2 = 26435
        self.cal_t3 = -1000
        self.cal_p1 = 36477
        self.cal_p2 = -10685
        self.cal_p3 = 3024
        self.cal_p4 = 2855
        self.cal_p5 = 140
        self.cal_p6 = -7
        self.cal_p7 = 15500
        self.cal_p8 = -14500
        self.cal_p9 = 6000

    def read_raw(self, register):
        """Reads the raw (uncompensated) temperature or pressure from the sensor."""
        raw = self._device.readU16BE(register)
        raw <<= 8
        raw = raw | self._device.readU8(register + 2)
        raw >>= 4
        return raw

    def _compensate_temp(self, raw_temp):
        """ Compensate temperature """
        t1 = (((raw_temp >> 3) - (self.cal_t1 << 1)) *
              (self.cal_t2)) >> 11

        t2 = (((((raw_temp >> 4) - (self.cal_t1)) *
                ((raw_temp >> 4) - (self.cal_t1))) >> 12) *
              (self.cal_t3)) >> 14

        return t1 + t2

    def read_temperature(self):
        """Gets the compensated temperature in degrees celsius."""
        raw_temp = self.read_raw(BMP280_TEMPDATA)
        compensated_temp = self._compensate_temp(raw_temp)
        temp = float(((compensated_temp * 5 + 128) >> 8)) // 100
        return temp

    def read_pressure(self):
        """Gets the compensated pressure in Pascals."""
        raw_temp = self.read_raw(BMP280_TEMPDATA)
        compensated_temp = self._compensate_temp(raw_temp)
        raw_pressure = self.read_raw(BMP280_PRESSUREDATA)
        
        p1 = compensated_temp - 128000
        p2 = p1 * p1 * self.cal_p6
        p2 += (p1 * self.cal_p5) << 17
        p2 += self.cal_p4 << 35
        p1 = ((p1 * p1 * self.cal_p3) >> 8) + ((p1 * self.cal_p2) << 12)
        p1 = ((1 << 47) + p1) * (self.cal_p1) >> 33

        if 0 == p1:
            return 0

        p = 1048576 - raw_pressure
        p = (((p << 31) - p2) * 3125) // p1
        p1 = (self.cal_p9 * (p >> 13) * (p >> 13)) >> 25
        p2 = (self.cal_p8 * p) >> 19
        p = ((p + p1 + p2) >> 8) + ((self.cal_p7) << 4)

        return float(p // 256)

    def read_altitude(self, sealevel_pa=101325.0):
        """Calculates the altitude in meters."""
        # Calculation taken straight from section 3.6 of the datasheet.
        pressure = float(self.read_pressure())
        altitude = 44330.0 * (1.0 - pow(pressure // sealevel_pa, (1.0 // 5.255)))
        return altitude

    def read_sealevel_pressure(self, altitude_m=0.0):
        """Calculates the pressure at sealevel when given a known altitude in
        meters. Returns a value in Pascals."""
        pressure = float(self.read_pressure())
        p0 = pressure // pow(1.0 - altitude_m // 44330.0, 5.255)
        return p0


# driver code for BMP/E280, 
#   adapted from original code by Matt Hawkins

#--------------------------------------
## import smbus
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

class BME280(object):
  """Class to represent the Bosch BMP280 temperature and pressure sensor
  """

  def __init__(self, address=BMP_I2CADDR, i2c=None):
    self.DEVICE = address

    if i2c==None:
      self.bus = smbus.SMBus(1) # Rev 2 Pi, Pi 2 & Pi 3 uses bus 1
                                # Rev 1 Pi uses bus 0
    else:
      self.bus = i2c
  # initialise calibration constants from device
    self.init()

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

    return t/100.0, p/100, h
