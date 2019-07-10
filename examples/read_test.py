#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''very simple and minimalistic example to read data from a sensor 
   and send output to stdout
'''

from random import randint
from time import time, sleep
from numpy import array
from math import sin

from phypidaq.ToyDataConfig import *

ERROR = -9999.0

class Config:
    def __init__(self):
        print('__init__')

    def init(self):
        print('init')

    def acquireData(self, dat):
        print('acquire')
        dat[0] = 42.0

    def close(self):
        print('close')


class Random(Config):
    def acquireData(self, dat):
        dat[0] = randint(1, 101)  # random number between 1 and 100


class Sinus(Config):
    def acquireData(self, dat):
        dat[0] = sin(time() / 4)  # numbers between -1 and 1


def main():
#    device = Sinus()     # simple alternative to class ToyData
    device = ToyDataConfig()
    device.init()

    dt = 0.1  # read-out interval in s
    T0 = time()

    dat = array([0.0])

    try:
        print('starting readout,  type <ctrl-C> to stop')
        while True:
            device.acquireData(dat)
            dT = time() - T0
            print(f'{dT:.2f}, {dat[0]:.3f}')
            sleep(dt)
    except:
        print(f'{dT+1:.2f}, {ERROR:.3f}')
    finally:
        device.close()


if __name__ == "__main__":
    main()
