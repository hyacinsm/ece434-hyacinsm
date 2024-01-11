#!/usr/bin/env python3
# /////////////////////////////////////////
#
#   Author: Sean Hyacinthe
#   Date: 1/09/24
#
#   Description: The script reads the value of two tmp101 sensors every 1 second
#
#   Setup:
#           ./setup.sh
#
#   Wiring:
#           tmp101_gnd is has pin add0 wired to GND
#           tmp101_vcc is has pin add0 wired to 3.3 V

import time

tmp_48_path = '/sys/class/i2c-adapter/i2c-2/2-0048/hwmon/hwmon0/temp1_input'
tmp_4a_path = '/sys/class/i2c-adapter/i2c-2/2-004a/hwmon/hwmon1/temp1_input'


file_48 = open(tmp_48_path, "r")
file_4a = open(tmp_4a_path, "r")


def c2f(temp_c):
    return round((temp_c * 9/5) + 32, 2)


while True:

    # set cursor position
    file_48.seek(0)
    file_4a.seek(0)

    # grab current data and convert it to Celsius
    data_48 = int(file_48.read().strip()) / 1000
    data_4a = int(file_4a.read().strip()) / 1000

    print(f"tmp @ 48 = {c2f(data_48)}")
    print(f"tmp @ 4a = {c2f(data_4a)}")
    print("")

    time.sleep(1)
