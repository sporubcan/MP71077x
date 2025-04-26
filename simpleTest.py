#!/usr/bin/env python3

import MP71077x
import time
from sys import argv

if len(argv) < 2:
    print("Usage: python simpleTest.py <address>")
    exit(0)
address = argv[1]
load = MP71077x.MP71077x(target_ip = address, verbosity=True)
load.openSocket()

load.setUpperVoltageLimit(30.00)
load.setUpperCurrentLimit(30.00)

try:
    load.setCIcurrent(40.000, True)
except Exception as e:
    print (e)
    pass
load.setUpperCurrentLimit(40.00)
load.setCIcurrent(40.000, True)

time.sleep(1)

try:
    load.setCVvoltage(40.000, True)
except Exception as e:
    print (e)
    pass
load.setUpperVoltageLimit(150.00)
load.setCVvoltage(150.000, True)

time.sleep(1)

load.setUpperPowerLimit(25.00)
try:
    load.setCPpower(35.000, True)
except Exception as e:
    print (e)
    pass
load.setUpperPowerLimit(300.00)
load.setCPpower(300.000, True)

time.sleep(1)

load.setUpperResistanceLimit(133.00)
try:
    load.setCRresistance(500.000, True)
except Exception as e:
    print (e)
    pass
load.setUpperResistanceLimit(7500.00)
load.setCRresistance(7500.000, True)

load.turnInputON(True)
time.sleep(2)
load.turnInputOFF(True)

print(load.getVoltageLimits())
print(load.getCurrentLimits())
print(load.getPowerLimits())
print(load.getResistanceLimits())

load.closeSocket()
