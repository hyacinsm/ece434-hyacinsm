#!/usr/bin/env python3
# /////////////////////////////////////////
#
#   Author: Sean Hyacinthe
#   Date: 1/09/24
#
#   Description: Reads the x and y raw data of the adxl345
#
#   Setup:
#           ./adxel345_etup.sh
#
#   Wiring:
#           tmp101_gnd is has pin add0 wired to GND
#           tmp101_vcc is has pin add0 wired to 3.3 V
#           SDA is running on P9_22
#           SCL is running on P9_21

import time

ADXL345 = '/sys/class/i2c-adapter/i2c-2/2-0053/iio:device0'

X_ACCEL_PATH = "/in_accel_x_raw"
Y_ACCEL_PATH = "/in_accel_y_raw"

x_file = open(ADXL345 + X_ACCEL_PATH, "r")
y_file = open(ADXL345 + Y_ACCEL_PATH, "r")


while True:

    # set cursor position
    x_file.seek(0)
    y_file.seek(0)

    x_val = int(x_file.read().strip())
    y_val = int(y_file.read().strip())

    print(f"X Accel = {x_val}")
    print(f"Y Accel = {y_val}")
    print("")

    time.sleep(1)
