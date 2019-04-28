# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import
import numpy as np, time, sys


# code of driver classes included below

# AS7265x defaults
AS_I2CADDR = 0x49
BUS = 1
AS_MAXVAL = 15000 # ~14 bit

class AS7265xConfig(object):
  ''' AS7265x configuration and interface'''

  def __init__(self, confdict = None):
    if confdict == None: confdict={}
          
# -- number of Channels
    self.NChannels = 18

    if 'Gain' in confdict:
      self.gain = confdict['Gain']      
    else:
      self.gain = 11
        # Possible gain values:
        #   0, 1, 2, 3 where b00=1x; b01=3.7x; b10=16x; b11=64x

    if 'IntegrationTime' in confdict:
      self.IntT = confdict['IntegrationTime']      
    else:
      self.IntT = 10
    
    if 'LEDCurrent' in confdict:
      self.LEDI = confdict['LEDCurrent']      
    else:
      self.LEDI = 0  
        
    if 'ShutterLEDs' in confdict:
      self.LEDShutter = confdict['ShutterLEDs']      
    else:
      self.LEDShutter = 0
      
    if 'CalibrateData' in confdict:
      self.CalibrateData = confdict['CalibrateData']      
    else:
      self.CalibrateData = 0
      
    if 'TrimTo1' in confdict:
      self.TrimTo1 = confdict['TrimTo1']      
    else:
      self.TrimTo1 = 0

    if 'I2CADDR' in confdict:
      self.I2CAddr = confdict['I2CADDR']
      print("AS7265x: I2C address set to %x "%(self.I2CAddr) )
    else: 
      self.I2CAddr = AS_I2CADDR  # use default

    if 'busnum' in confdict:
      self.busnum = confdict['busnum']
      print("AS7265x: bus number set to %x "%(self.busnum) )
    else: 
      self.busnum = BUS # use default
    
    self.maxVal = AS_MAXVAL # ~14 bit

 # provide configuration parameters
    self.ChanNams = ['410', '435', '460', '485', '510', '535', '560', '585', '610', '645', '680', '705', '730', '760', '810', '860', '900', '940'] #nm
    self.ChanLims = [[0., 1.]] * self.NChannels
      
 ##############################################################################
  def init(self):
    self.AS7265x = AS7265x(self.busnum, self.I2CAddr) 

    try:
      if self.AS7265x.boardPresent() != 0:
        self.AS7265x.initDev()
        self.AS7265x.setGain(self.gain)
        self.AS7265x.setIntegrationTime(self.IntT)
        self.AS7265x.setLEDDriveCurrent(self.LEDI)
        self.AS7265x.setBlueLED(0) # Turn blue LED off to indicate that Device is initialized
        
        print(str(self.LEDShutter))
        if self.LEDShutter & 0x01: 
           self.AS7265x.shutterLED("AS72651",1)
        if self.LEDShutter & 0x02: 
           self.AS7265x.shutterLED("AS72652",1)
        if self.LEDShutter & 0x04: 
           self.AS7265x.shutterLED("AS72653",1)
      else:
        print("AS7265xConfig: AS7265x not found - exit")
        sys.exit(1)
              
    except Exception as e:
      print("AS7265xConfig: Error initialising device - exit")
      print(str(e))
      sys.exit(1)

  def acquireData(self, buf):
    
    if self.CalibrateData ==1:
      buf[0], buf[1], buf[2], buf[3], buf[4], buf[5], buf[6], buf[7], buf[8], buf[9], buf[10], buf[11], buf[12], buf[13], buf[14], buf[15], buf[16], buf[17] = self.AS7265x.readCAL()
    else:
      buf[0], buf[1], buf[2], buf[3], buf[4], buf[5], buf[6], buf[7], buf[8], buf[9], buf[10], buf[11], buf[12], buf[13], buf[14], buf[15], buf[16], buf[17] = self.AS7265x.readRAW()
    
    if self.TrimTo1 ==1:
      arrmax=np.amax(buf)    
      for i in range(self.NChannels):
        buf[i] /= arrmax
    else:
      for i in range(self.NChannels):
        buf[i] /= self.maxVal
      
  def closeDevice(self):
    self.AS7265x.setBlueLED(1) # LED on indicates standyby, uninitialized(LED is ON, when powered)
    self.AS7265x.shutterLED("AS72651",0)
    self.AS7265x.shutterLED("AS72652",0)
    self.AS7265x.shutterLED("AS72653",0)

##############################################################################
##############################################################################

# driver code
#   adapted from 
# https://github.com/LiamsGitHub/AS7265x-spectrometer/blob/master/spectrometer.py


# Python 2.7 module for the SparkFun Triad Spectroscopy board
# Feb 2019. Version 1


from smbus import SMBus                                         # Module for I2C
import time

class AS7265x(object):
  def __init__(self, busnum, i2caddr):
    self.I2C_ADDR =      i2caddr       #0x49
    self.STATUS_REG =    0x00
    self.WRITE_REG =     0x01
    self.READ_REG =      0x02
    self.TX_VALID =      0x02
    self.RX_VALID =      0x01
    self.POLLING_DELAY = 0.002   # 50mS delay to prevent swamping the slave's I2C port
    self.i2c = SMBus(busnum)                          


  # ---- Low level functions -----

  # Low level function to read a Master register over I2C
  # Input variables: addr (Int)
  # Legal input values: n/a
  # Returns: data (int)
  def readReg(self, addr):

      status = self.i2c.read_byte_data(self.I2C_ADDR,self.STATUS_REG)            # Do a dummy read to ensure FIFO queue is empty
      if ((status & self.RX_VALID) != 0):                              # There is data to be read
          incoming = self.i2c.read_byte_data(self.I2C_ADDR,self.READ_REG)        # Read it to clear the queue and dump it

      while (1):

          status = self.i2c.read_byte_data(self.I2C_ADDR,self.STATUS_REG)        # Poll Slave Status register

          if ((status & self.TX_VALID) == 0):                          # Wait for OK to transmit
              break

          time.sleep(self.POLLING_DELAY)                               # Polling delay to avoid drowning Slave

      self.i2c.write_byte_data(self.I2C_ADDR, self.WRITE_REG, addr)              # send to Write register the Virtual Register address

      while (1):
          status = self.i2c.read_byte_data(self.I2C_ADDR,self.STATUS_REG)        # Poll Slave Status register

          if ((status & self.RX_VALID) != 0):                          # Wait for data to be present
              break
          time.sleep(0.05)                                        # Polling delay to avoid drowning Slave

      data = self.i2c.read_byte_data(self.I2C_ADDR,self.READ_REG)                # Finally pick up the data

      return data

  # Low level function to write to a Master register over I2C
  # Input variables: addr (Int), data (Int)
  # Legal input values: n/a
  # Returns: none
  def writeReg(self, addr,data):

      while (1):

          status = self.i2c.read_byte_data(self.I2C_ADDR,self.STATUS_REG)        # Poll Slave Status register

          if ((status & self.TX_VALID) == 0):                          # Wait for OK to transmit
              break

          time.sleep(self.POLLING_DELAY)

      self.i2c.write_byte_data(self.I2C_ADDR, self.WRITE_REG, addr | 0x80)       # Send Virtual Register address to Write register 

      while (1):
          status = self.i2c.read_byte_data(self.I2C_ADDR,self.STATUS_REG)        # Poll Slave Status register

          if ((status & self.TX_VALID) == 0):                          # Ready for the write
              break
              
          time.sleep(self.POLLING_DELAY)

      self.i2c.write_byte_data(self.I2C_ADDR,self.WRITE_REG,data)                # Do the write
      return

  # Calibrated data comes back as IEEE754 encoded number (sign/mantissa/fraction). Need to convert to a float. Spec page 27.
  # Input variables: [Int] list of 4 Ints
  # Legal input values: n/a
  # Returns: Float
  def IEEE754toFloat(self, valArray):

      c0 = valArray[0]
      c1 = valArray[1]
      c2 = valArray[2]
      c3 = valArray[3]
      
      fullChannel = (c0 <<24) | (c1 << 16) | (c2 << 8) | (c3)

      sign = ((1 << 31) & (fullChannel)) >> 31
      sign = (-1) ** sign

      exponent = (fullChannel >> 23) & (0xff)
      frac = fullChannel & 0x7fffff                               # filter out all but bottom 22 bits (fraction)

      accum = 1

      for bit in range(22,-1,-1):
          if (frac & (1<<bit)):
              bitfrac = 1/float(2 ** (23 - bit))
              accum = accum + bitfrac

      floatVal = sign * accum * (2 ** (exponent - 127))

      return floatVal

  # Set the DEVSEL register 0X4F to point to the sensor that we want
  # Input variables: (String) device name
  # Legal input values: n/a
  # Returns: Bool True if OK
  # Note: There is a BUG in the AS firmware: you CAN'T to read/modify/write. Doesn't work. Just overwrite whole register.
  def setDEVSEL(self, device):

      DEVSELbits = {"AS72651":0b00, "AS72652": 0b01, "AS72653": 0b10}

      try:
          mode = DEVSELbits[device]
      except:
          print ("DEVSEL bad device name")
          return (False)

      self.writeReg(0x4f, mode)

      return (True)
      
  # Frequencies of sensors when read out serially are not in ascending order due to overlapping sensor bandwidths. Re-order data.
  # Input variables: [Int] or [Float]. List of 18 data points
  # Legal input values: n/a
  # Returns: [Int] or [Float]. List of 18 data points
  def reorderData(self, unsortedData):

      mappings = [(1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7), (8,8), (13,9), (14,11), (9,10), (10,12), (15,13), (16,14), (17,15), (18,16), (11,17), (12,18) ]
      sortedData = [0] * 18
      
      for pairs in mappings:
          sortedData[pairs[1]-1] = unsortedData[pairs[0]-1]   # -1 is to correct for 1st list member being in position 0

      return (sortedData)


  # ---- Spec functions -----

  # Initialize board with default settings (factory reset)
  # Input variables: none
  # Legal input values: none
  # Returns: none
  def initDev(self):

      self.writeReg(0x04,1)
      time.sleep(2)       # Experience was the on-board firmware needs a 2s delay after factory reset to get ready. If you poll it immediately you get [Errno 121] Remote I/O error

      return (True)


  # Return device present
  # Input variables: none
  # Legal input values: none
  # Returns: Boolean. True, False
  def boardPresent(self):
      try:
          device_type = self.readReg(0x00)
          return (True)
      except:
          return (False)

  # Return system hardware version
  # Input variables: void
  # Legal input values:
  # Returns: tuple of ints (device type, hardware version)
  def hwVersion(self):
      device_type = self.readReg(0x00)
      hw_version = self.readReg(0x01)
      
      #print (device_type, hw_version)

      return ( (device_type, hw_version) )

  # Return current temperatures of all 3 devices in a list
  # Input variables: void
  # Legal input values:
  # Returns: [int, int, int]
  def temperatures(self):
      devices = ["AS72651", "AS72652", "AS72653"]
      temps = []
      for device in devices:
          self.setDEVSEL(device)
          temp = self.readReg(0x06)
          temps.append(temp)
      return (temps)


  # Set master blue LED state (device 1 on IND line)
  # Input variables: state (Bool)
  # Legal input values: True, False
  # Returns: Bool. True if OK.
  def setBlueLED(self, state):

      self.setDEVSEL("AS72651")    # Blue LED attached to this device so need to select it first

      currentState = self.readReg(0x07)

      if (state):
          newState = (currentState | 0b1 )
      else:
          newState = (currentState & 0b11111110 )

      self.writeReg(0x07,newState)
      return (True)
      

  # Switch on/off shutter individual LEDs attached to sensor DRV lines
  # Input variables: device (String), state (Bool)
  # Legal input values: device {"AS72651","AS72652","AS72653"}, state{True, False}
  def shutterLED(self, device,state):

      DEVSELbits = {"AS72651":0b00, "AS72652": 0b01, "AS72653": 0b10}

      try:
          mode = DEVSELbits[device]
          #print ("Mode = " + str(mode))
      except:
          print ("Bad device name")
          return (False)
          
      self.setDEVSEL(device)
      currentState = self.readReg(0x07)
      
      if (state == True):
          newState = (currentState | 0b1000)
      else:
          newState = (currentState & 0b11110111)
          
      self.writeReg(0x07,newState)
      
      return (True)


  # Set LED drive current for all shutter LEDs together
  # Input variables: current (Int)
  # Legal input values: 0, 1, 2, 3 where b00=12.5mA; b01=25mA; b10=50mA; b11=100mA
  # Returns: Bool. True if OK.
  def setLEDDriveCurrent(self, current):

      devices = ["AS72651", "AS72652", "AS72653"]
      
      if current not in [0, 1]: #[0, 1, 2, 3]:
          print ("Illegal current setting")
          return (False)

      for device in devices:
          self.setDEVSEL(device)
          configReg = self.readReg(0x07)
          configReg = ( configReg & 0b11001111 )
          configReg = configReg | (current << 4)
          self.writeReg(0x07, configReg)

      return (True)


  # Set integration time for all sensors together
  # Input variables: time (Int)
  # Legal input values: 0 to 255
  # Returns: Bool. True if OK.
  def setIntegrationTime(self, time):

      devices = ["AS72651", "AS72652", "AS72653"]
      
      if time not in range(0,255):
          print ("Illegal integration time setting")
          return (False)

      for device in devices:
          self.setDEVSEL(device)
          self.writeReg(0x05, time)
          
      for device in devices:
          self.setDEVSEL(device)
          #print(self.readReg(0x05))

      return (True)


  # Set sensor gains for all devices together
  # Input variables: gain (Int) 
  # Legal input values:  0, 1, 2, 3 where b00=1x; b01=3.7x; b10=16x; b11=64x
  # Returns: Bool. True if OK.
  def setGain(self, gain):

      devices = ["AS72651", "AS72652", "AS72653"]
      
      if gain not in [0, 1, 2, 3]:
          print ("Illegal gain setting")
          return (False)

      for device in devices:
          self.setDEVSEL(device)
          configReg = self.readReg(0x04)
          configReg = ( configReg & 0b11001111 )
          configReg = configReg | (gain << 4)
          self.writeReg(0x04, configReg)
          
      for device in devices:
          self.setDEVSEL(device)
          #print(self.readReg(0x04))

      return (True)


  # Read all 18 RAW values together
  # Input variables: none
  # Legal input values:  none
  # Returns: [Int] list of 18 Int values
  def readRAW(self):

      RAWRegisters = [(0x08, 0x09), (0x0a, 0x0b), (0x0c, 0x0d), (0x0e, 0x0f), (0x10, 0x11), (0x12, 0x13)]
      RAWValues = []
      devices = ["AS72651", "AS72652", "AS72653"]
      
      for device in devices:
          self.setDEVSEL(device)

          for regPair in RAWRegisters:
              highVal = self.readReg(regPair[0])
              lowVal = self.readReg(regPair[1])
              RAWValues.append( (highVal << 8) | (lowVal) )

  # now reorder the data to be in monotonic frequency order
      output = self.reorderData(RAWValues)
      #print(output)

      return (output)


  # Read all 18 calibrated values together
  # Input variables: none
  # Legal input values:  none
  # Returns: [Int] list of 18 Int values
  def readCAL(self):

      CALRegisters = [(0x14,0x15,0x16,0x17),(0x18,0x19,0x1a,0x1b),(0x1c,0x1d,0x1e,0x1f),(0x20,0x21,0x22,0x23),(0x24,0x25,0x26,0x27),(0x28,0x29,0x2a,0x2b)]
      CALValues = []
      devices = ["AS72651", "AS72652", "AS72653"]
      
      for device in devices:
          self.setDEVSEL(device)

          for regQuad in CALRegisters:
              cal0 = self.readReg(regQuad[0])
              cal1 = self.readReg(regQuad[1])
              cal2 = self.readReg(regQuad[2])
              cal3 = self.readReg(regQuad[3])
              floatval = self.IEEE754toFloat([cal0,cal1,cal2,cal3])
              CALValues.append(floatval)

  # now reorder the data to be in monotonic frequency order
      output = self.reorderData(CALValues)
      #print(output)

      return (output)
