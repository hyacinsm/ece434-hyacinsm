#!/usr/bin/env python3
# /////////////////////////////////////////
#
#   Author: Sean Hyacinthe
#   Date: 12/18/24
#
#   Description: The script reads the value of two tmp101 sensors every 1 second
#
#   Wiring:
#               ./config_pin P9_21 i2c
#               ./config_pin P9_22 i2c
#               ./config_pin P8_12 eqep //=> A
#               ./config_pin P8_11 eqep //=> B
#               ./config_pin P8_33 eqep //=> B
#               ./config_pin P8_35 eqep //=> A
#
#           tmp101_gnd is has pin add0 wired to GND
#           tmp101_vcc is has pin add0 wired to 3.3 V
#


import smbus
import time


bus = smbus.SMBus(2)
sensor_addresses = [0x48, 0x4a]

while True:
    for sensor in sensor_addresses:
        temp = bus.read_byte_data(sensor, 0)
        print(f"Temp @ {sensor:0x} = ", temp)
    print("")
    time.sleep(1)
