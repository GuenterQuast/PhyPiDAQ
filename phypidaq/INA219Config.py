# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import numpy as np, time, sys

# default addresses and ChipIDs of Bosch BMP 085/180 and BMP/E 280 sensors
# Hardware defaults
busnum = 1 
INA_I2CADDR  = 0x40 # I2C address
SHUNT = 0.1         # Shunt resitor in Ohms

cname = "INA219Config"

# code of driver classes is included below

class INA219Config(object):
  '''current and voltage sensor INA219'''
  def __init__(self, confdict = None):
    self.I2CADDR = INA_I2CADDR

    if confdict==None: confdict={}
    if 'I2CADDR' in confdict:
      self.I2CADDR = confdict['I2CADDR']
      print(cname +": I2C address set to %x "%(self.I2CADDR) )
    if 'NChannels' in confdict:
      self.NChannels = confdict["NChannels"]
    else:
      self.NChannels = 2

    if 'maxAmp' in confdict:
      self.maxAmp = confdict['maxAmp']
    else:
      self.maxAmp = 3.19999
    print(cname +": Current range set to %.3fA "%(self.maxAmp ) )

    if 'maxVolt' in confdict:
      self.maxVolt = confdict['maxVolt']
    else:
      self.maxVolt = 32.

    self.ChanLims = [[0., self.maxAmp], 
                     [0., self.maxVolt],
                     [0., self.maxAmp*self.maxVolt]  ]
    self.ChanNams = ['I','U', 'P']
    self.ChanUnits= ['A','V', 'W']

  def init(self):

    if self.maxAmp > 3.2 :
      print('!!! ' + cname +": Current range must be < 3.2A")
      sys.exit(1)

    self.sensor = INA219(SHUNT, self.maxAmp,
                   busnum=busnum, address=INA_I2CADDR )

    if self.maxVolt <= 16. :
      VRange=self.sensor.RANGE_16V
    elif self.maxVolt <=32. : 
      VRange = self.sensor.RANGE_32V
    else:
      print('!!! ' + cname +": Voltage must be < 32.V")
      sys.exit(1)      

    self.sensor.configure(VRange, self.sensor.GAIN_AUTO)
      
  def acquireData(self, buf):
    buf[0] = self.sensor.current()/1000. # in Amps
    if self.NChannels > 1:
      buf[1] = self.sensor.voltage()
    if self.NChannels > 2:
      buf[2] = self.sensor.power()

  def closeDevice(self):
   # nothing to do here
    pass


## ----- driver section ---------
# driver code for INA219 adapted from original version by Chris Borill,
#       https://github.com/chrisb2/pi_ina219# 

from math import trunc
import Adafruit_GPIO.I2C as I2C

class INA219:

    RANGE_16V = 0  # Range 0-16 volts
    RANGE_32V = 1  # Range 0-32 volts

    GAIN_1_40MV = 0  # Maximum shunt voltage 40mV
    GAIN_2_80MV = 1  # Maximum shunt voltage 80mV
    GAIN_4_160MV = 2  # Maximum shunt voltage 160mV
    GAIN_8_320MV = 3  # Maximum shunt voltage 320mV
    GAIN_AUTO = -1  # Determine gain automatically

    ADC_9BIT = 0  # 9-bit conversion time  84us.
    ADC_10BIT = 1  # 10-bit conversion time 148us.
    ADC_11BIT = 2  # 11-bit conversion time 2766us.
    ADC_12BIT = 3  # 12-bit conversion time 532us.
    ADC_2SAMP = 9  # 2 samples at 12-bit, conversion time 1.06ms.
    ADC_4SAMP = 10  # 4 samples at 12-bit, conversion time 2.13ms.
    ADC_8SAMP = 11  # 8 samples at 12-bit, conversion time 4.26ms.
    ADC_16SAMP = 12  # 16 samples at 12-bit,conversion time 8.51ms
    ADC_32SAMP = 13  # 32 samples at 12-bit, conversion time 17.02ms.
    ADC_64SAMP = 14  # 64 samples at 12-bit, conversion time 34.05ms.
    ADC_128SAMP = 15  # 128 samples at 12-bit, conversion time 68.10ms.

    __ADDRESS = 0x40

    __REG_CONFIG = 0x00
    __REG_SHUNTVOLTAGE = 0x01
    __REG_BUSVOLTAGE = 0x02
    __REG_POWER = 0x03
    __REG_CURRENT = 0x04
    __REG_CALIBRATION = 0x05

    __RST = 15
    __BRNG = 13
    __PG1 = 12
    __PG0 = 11
    __BADC4 = 10
    __BADC3 = 9
    __BADC2 = 8
    __BADC1 = 7
    __SADC4 = 6
    __SADC3 = 5
    __SADC2 = 4
    __SADC1 = 3
    __MODE3 = 2
    __MODE2 = 1
    __MODE1 = 0

    __OVF = 1
    __CNVR = 2

    __BUS_RANGE = [16, 32]
    __GAIN_VOLTS = [0.04, 0.08, 0.16, 0.32]

    __CONT_SH_BUS = 7

    __AMP_ERR_MSG = ('Expected current %.3fA is greater '
                     'than max possible current %.3fA')
    __RNG_ERR_MSG = ('Expected amps %.2fA, out of range, use a lower '
                     'value shunt resistor')
    __VOLT_ERR_MSG = ('Invalid voltage range, must be one of: '
                      'RANGE_16V, RANGE_32V')

    __LOG_FORMAT = '%(asctime)s - %(levelname)s - INA219 %(message)s'
    __LOG_MSG_1 = ('shunt ohms: %.3f, bus max volts: %d, '
                   'shunt volts max: %.2f%s, '
                   'bus ADC: %d, shunt ADC: %d')
    __LOG_MSG_2 = ('calibrate called with: bus max volts: %dV, '
                   'max shunt volts: %.2fV%s')
    __LOG_MSG_3 = ('Current overflow detected - '
                   'attempting to increase gain')

    __SHUNT_MILLIVOLTS_LSB = 0.01  # 10uV
    __BUS_MILLIVOLTS_LSB = 4  # 4mV
    __CALIBRATION_FACTOR = 0.04096
    __MAX_CALIBRATION_VALUE = 0xFFFE  # Max value supported (65534 decimal)
    # In the spec (p17) the current LSB factor for the minimum LSB is
    # documented as 32767, but a larger value (100.1% of 32767) is used
    # to guarantee that current overflow can always be detected.
    __CURRENT_LSB_FACTOR = 32800

    def __init__(self, shunt_ohms, max_expected_amps=None,
                 busnum=None, address=__ADDRESS):
        """ Construct the class passing in the resistance of the shunt
        resistor and the maximum expected current flowing through it in
        your system.

        Arguments:
        shunt_ohms -- value of shunt resistor in Ohms (mandatory).
        max_expected_amps -- the maximum expected current in Amps (optional).
        address -- the I2C address of the INA219, defaults
            to *0x40* (optional).
        """
        self._i2c = I2C.get_i2c_device(address=address, busnum=busnum)
        self._shunt_ohms = shunt_ohms
        self._max_expected_amps = max_expected_amps
        self._min_device_current_lsb = self._calculate_min_current_lsb()
        self._gain = None
        self._auto_gain_enabled = False

    def configure(self, voltage_range=RANGE_32V, gain=GAIN_AUTO,
                  bus_adc=ADC_12BIT, shunt_adc=ADC_12BIT):
        """ Configures and calibrates how the INA219 will take measurements.

        Arguments:
        voltage_range -- The full scale voltage range, this is either 16V
            or 32V represented by one of the following constants;
            RANGE_16V, RANGE_32V (default).
        gain -- The gain which controls the maximum range of the shunt
            voltage represented by one of the following constants;
            GAIN_1_40MV, GAIN_2_80MV, GAIN_4_160MV,
            GAIN_8_320MV, GAIN_AUTO (default).
        bus_adc -- The bus ADC resolution (9, 10, 11, or 12-bit) or
            set the number of samples used when averaging results
            represent by one of the following constants; ADC_9BIT,
            ADC_10BIT, ADC_11BIT, ADC_12BIT (default),
            ADC_2SAMP, ADC_4SAMP, ADC_8SAMP, ADC_16SAMP,
            ADC_32SAMP, ADC_64SAMP, ADC_128SAMP
        shunt_adc -- The shunt ADC resolution (9, 10, 11, or 12-bit) or
            set the number of samples used when averaging results
            represent by one of the following constants; ADC_9BIT,
            ADC_10BIT, ADC_11BIT, ADC_12BIT (default),
            ADC_2SAMP, ADC_4SAMP, ADC_8SAMP, ADC_16SAMP,
            ADC_32SAMP, ADC_64SAMP, ADC_128SAMP
        """
        self.__validate_voltage_range(voltage_range)
        self._voltage_range = voltage_range

        if self._max_expected_amps is not None:
            if gain == self.GAIN_AUTO:
                self._auto_gain_enabled = True
                self._gain = self._determine_gain(self._max_expected_amps)
            else:
                self._gain = gain
        else:
            if gain != self.GAIN_AUTO:
                self._gain = gain
            else:
                self._auto_gain_enabled = True
                self._gain = self.GAIN_1_40MV

        self._calibrate(
            self.__BUS_RANGE[voltage_range], self.__GAIN_VOLTS[self._gain],
            self._max_expected_amps)
        self._configure(voltage_range, self._gain, bus_adc, shunt_adc)

    def voltage(self):
        """ Returns the bus voltage in volts. """
        value = self._voltage_register()
        return float(value) * self.__BUS_MILLIVOLTS_LSB / 1000

    def supply_voltage(self):
        """ Returns the bus supply voltage in volts. This is the sum of
        the bus voltage and shunt voltage. A DeviceRangeError
        exception is thrown if current overflow occurs."""
        return self.voltage() + (float(self.shunt_voltage()) / 1000)

    def current(self):
        """ Returns the bus current in milliamps. A DeviceRangeError
        exception is thrown if current overflow occurs."""
        self._handle_current_overflow()
        return self._current_register() * self._current_lsb * 1000

    def power(self):
        """ Returns the bus power consumption in milliwatts.
        A DeviceRangeError exception is thrown if current overflow occurs."""
        self._handle_current_overflow()
        return self._power_register() * self._power_lsb * 1000

    def shunt_voltage(self):
        """ Returns the shunt voltage in millivolts.
        A DeviceRangeError exception is thrown if current overflow occurs."""
        self._handle_current_overflow()
        return self._shunt_voltage_register() * self.__SHUNT_MILLIVOLTS_LSB

    def sleep(self):
        """ Put the INA219 into power down mode. """
        configuration = self._read_configuration()
        self._configuration_register(configuration & 0xFFF8)

    def wake(self):
        """ Wake the INA219 from power down mode """
        configuration = self._read_configuration()
        self._configuration_register(configuration | 0x0007)
        # 40us delay to recover from powerdown (p14 of spec)
        time.sleep(0.00004)

    def current_overflow(self):
        """ Returns true if the sensor has detect current overflow. In
        this case the current and power values are invalid."""
        return self._has_current_overflow()

    def reset(self):
        """ Reset the INA219 to its default configuration. """
        self._configuration_register(1 << self.__RST)

    def _handle_current_overflow(self):
        if self._auto_gain_enabled:
            while self._has_current_overflow():
                self._increase_gain()
        else:
            if self._has_current_overflow():
                raise DeviceRangeError(self.__GAIN_VOLTS[self._gain])

    def _determine_gain(self, max_expected_amps):
        shunt_v = max_expected_amps * self._shunt_ohms
        if shunt_v > self.__GAIN_VOLTS[3]:
            raise ValueError(self.__RNG_ERR_MSG % max_expected_amps)
        gain = min(v for v in self.__GAIN_VOLTS if v > shunt_v)
        return self.__GAIN_VOLTS.index(gain)

    def _increase_gain(self):
        gain = self._read_gain()
        if gain < len(self.__GAIN_VOLTS) - 1:
            gain = gain + 1
            self._calibrate(self.__BUS_RANGE[self._voltage_range],
                            self.__GAIN_VOLTS[gain])
            self._configure_gain(gain)
            # 1ms delay required for new configuration to take effect,
            # otherwise invalid current/power readings can occur.
            time.sleep(0.001)
        else:
            print('Device limit reach, gain cannot be increased')
            raise DeviceRangeError(self.__GAIN_VOLTS[gain], True)

    def _configure(self, voltage_range, gain, bus_adc, shunt_adc):
        configuration = (
            voltage_range << self.__BRNG | gain << self.__PG0 |
            bus_adc << self.__BADC1 | shunt_adc << self.__SADC1 |
            self.__CONT_SH_BUS)
        self._configuration_register(configuration)

    def _calibrate(self, bus_volts_max, shunt_volts_max,
                   max_expected_amps=None):

        max_possible_amps = shunt_volts_max / self._shunt_ohms

        self._current_lsb = \
            self._determine_current_lsb(max_expected_amps, max_possible_amps)

        self._power_lsb = self._current_lsb * 20

        max_current = self._current_lsb * 32767

        max_shunt_voltage = max_current * self._shunt_ohms

        calibration = trunc(self.__CALIBRATION_FACTOR /
                            (self._current_lsb * self._shunt_ohms))
        self._calibration_register(calibration)

    def _determine_current_lsb(self, max_expected_amps, max_possible_amps):
        if max_expected_amps is not None:
            if max_expected_amps > round(max_possible_amps, 3):
                raise ValueError(self.__AMP_ERR_MSG %
                                 (max_expected_amps, max_possible_amps))
            if max_expected_amps < max_possible_amps:
                current_lsb = max_expected_amps / self.__CURRENT_LSB_FACTOR
            else:
                current_lsb = max_possible_amps / self.__CURRENT_LSB_FACTOR
        else:
            current_lsb = max_possible_amps / self.__CURRENT_LSB_FACTOR

        if current_lsb < self._min_device_current_lsb:
            current_lsb = self._min_device_current_lsb
        return current_lsb

    def _configuration_register(self, register_value):
        self.__write_register(self.__REG_CONFIG, register_value)

    def _read_configuration(self):
        return self.__read_register(self.__REG_CONFIG)

    def _calculate_min_current_lsb(self):
        return self.__CALIBRATION_FACTOR / \
            (self._shunt_ohms * self.__MAX_CALIBRATION_VALUE)

    def _read_gain(self):
        configuration = self._read_configuration()
        gain = (configuration & 0x1800) >> self.__PG0
        return gain

    def _configure_gain(self, gain):
        configuration = self._read_configuration()
        configuration = configuration & 0xE7FF
        self._configuration_register(configuration | (gain << self.__PG0))
        self._gain = gain

    def _calibration_register(self, register_value):
        self.__write_register(self.__REG_CALIBRATION, register_value)

    def _has_current_overflow(self):
        ovf = self._read_voltage_register() & self.__OVF
        return (ovf == 1)

    def _voltage_register(self):
        register_value = self._read_voltage_register()
        return register_value >> 3

    def _read_voltage_register(self):
        return self.__read_register(self.__REG_BUSVOLTAGE)

    def _current_register(self):
        return self.__read_register(self.__REG_CURRENT, True)

    def _shunt_voltage_register(self):
        return self.__read_register(self.__REG_SHUNTVOLTAGE, True)

    def _power_register(self):
        return self.__read_register(self.__REG_POWER)

    def __validate_voltage_range(self, voltage_range):
        if voltage_range > len(self.__BUS_RANGE) - 1:
            raise ValueError(self.__VOLT_ERR_MSG)

    def __write_register(self, register, register_value):
        register_bytes = self.__to_bytes(register_value)
        self._i2c.writeList(register, register_bytes)

    def __read_register(self, register, negative_value_supported=False):
        if negative_value_supported:
            register_value = self._i2c.readS16BE(register)
        else:
            register_value = self._i2c.readU16BE(register)
        return register_value

    def __to_bytes(self, register_value):
        return [(register_value >> 8) & 0xFF, register_value & 0xFF]

    def __binary_as_string(self, register_value):
        return bin(register_value)[2:].zfill(16)

    def __max_expected_amps_to_string(self, max_expected_amps):
        if max_expected_amps is None:
            return ''
        else:
            return ', max expected amps: %.3fA' % max_expected_amps


class DeviceRangeError(Exception):

    __DEV_RNG_ERR = ('Current out of range (overflow), '
                     'for gain %.2fV')

    def __init__(self, gain_volts, device_max=False):
        msg = self.__DEV_RNG_ERR % gain_volts
        if device_max:
            msg = msg + ', device limit reached'
        super(DeviceRangeError, self).__init__(msg)
        self.gain_volts = gain_volts
        self.device_limit_reached = device_max

