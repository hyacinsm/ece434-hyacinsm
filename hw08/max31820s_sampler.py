#!/usr/bin/env python3
#
#   Author: Sean Hyacinthe
#   Date: 2/04/24
#
#   Description: Reads temperature on 3 MAX31820 sensors using 1 wire protocol
#
#   Setup:  Use .dts file to conigure pin P9.14 as a 1 wire protocol pin
#
#
#   Wiring: P9.14 is configured as a 1 wire pin using device treee


import time

HWMON_0 = '/sys/class/hwmon/hwmon0'
HWMON_1 = '/sys/class/hwmon/hwmon1'
HWMON_2 = '/sys/class/hwmon/hwmon2'

TEMP_READING = '/temp1_input'

CELSIUS_MULTIPLIER = 1/1000

SAMPLE_RATE = 5

hw0_fd = open(HWMON_0 + TEMP_READING, "r")
hw1_fd = open(HWMON_1 + TEMP_READING, "r")
hw2_fd = open(HWMON_2 + TEMP_READING, "r")

t = 0


while True:
    try:
        hw0_fd.seek(0)
        hw1_fd.seek(0)
        hw2_fd.seek(0)

        hw0_val = round(float(hw0_fd.read().strip()) * CELSIUS_MULTIPLIER, 2)
        hw1_val = round(float(hw1_fd.read().strip()) * CELSIUS_MULTIPLIER, 2)
        hw2_val = round(float(hw2_fd.read().strip()) * CELSIUS_MULTIPLIER, 2)

        data = [t, hw0_val, hw1_val, hw2_val]

        print(data)
    except IOError as e:
        print(f"Error reading or seeking in file: {e}")

    t = t + SAMPLE_RATE
    time.sleep(SAMPLE_RATE)
