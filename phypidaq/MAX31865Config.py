# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import time
import board
import digitalio
import adafruit_max31865


class MAX31865Config(object):
    """RTD-to-Digital Converter - configuration and interface"""

    def __init__(self, conf_dict=None):
        if conf_dict is None:
            conf_dict = {}

        # Number of channels
        if 'NChannels' in conf_dict:
            self.NChannels = conf_dict["NChannels"]
            if self.NChannels <= 0:
                self.NChannels = 1
            elif self.NChannels > 2:
                self.NChannels = 2
        else:
            self.NChannels = 1

        # -- number of wires PT100
        if "NWires" in conf_dict:
            self.NWires = conf_dict["NWires"]
        else:
            self.NWires = 3

        # -- number of Channels
        self.NChannels = 1

        # -- reference resistor
        if 'Rref' in conf_dict:
            self.Rref = conf_dict['Rref']
        else:
            self.Rref = 430.0

        # -- resistance of PT100 at 0°C
        if 'R0' in conf_dict:
            self.R0 = conf_dict['R0']
        else:
            self.R0 = 100.

    def init(self):
        spi = board.SPI()
        cs = digitalio.DigitalInOut(board.D5)
        self.sensor = adafruit_max31865.MAX31865(spi, cs, wires=self.NWires, rtd_nominal=self.R0,
                                                 ref_resistor=self.Rref)

        # Provide configuration parameters
        self.ChanLims = [[-10., 110.]]
        self.ChanNams = [str(1)]

    def acquireData(self, buf):
        # Read the temperature
        buf[0] = self.sensor.temperature
        # Read the resistance, if two channels are configured
        if self.NChannels == 2:
            buf[1] = self.sensor.resistance

    def closeDevice(self):
        # Nothing to do here
        pass

    if __name__ == "__main__":
        import MAX31865Config
        sig = [0]
        max = MAX31865Config.MAX31865Config()
        max.init()
        for i in range(10):
            max.acquireData(sig)
            time.sleep(1)
