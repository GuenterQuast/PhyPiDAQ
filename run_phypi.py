#!/usr/bin/python3
# -*- coding: utf-8 -*-
''' script run_phypi.py to execute PhyPiDAQ

    usage: run_phypi.py <config>.daq
'''

import sys
import argparse as ap
from phypidaq.runPhyPiDAQ import *

if __name__ == "__main__": # - - - - - - - - - - - - - - - - - - - -
    parser = ap.ArgumentParser(description="runs PhyPiDAQ from a predefined configuration")
    parser.add_argument("configuration", help="Path to the configuration used",
            default="PhyPiDemo.daq")
    parser.add_argument("-v", "--verbose", action='count', default=0)
    args = parser.parse_args()
    if args['configuration'] == "PhyPiDemo.daq":
        print("No configuration given, using demo configuration: PhyPiDemo.daq")
    daq=runPhyPiDAQ(verbose=args['verbose'])
    daq.setup()
    print("DAQ set-up:\n", yaml.dump(daq.PhyPiConfDict))
    daq.run()
