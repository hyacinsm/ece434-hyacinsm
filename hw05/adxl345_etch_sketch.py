#!/usr/bin/env python3
# //////////////////////////////////////
#
#   Author: Sean Hyacinthe
#   Date: 1/22/24
#
# 	Runs an etch-sketch game on an LED matrix, using accelerometer to control direction
#   drawing. Hold finger on temp sensor to clear board. Press Ctrl -C to quit
#
#   Setup : run the ./adxel345_setup.sh to configure the needed pins
#   Wiring:	tmp101_gnd is has pin add0 wired to GND
#           tmp101_vcc is has pin add0 wired to 3.3 V
#           adxl345 connected SD0 to gnd and CS to Vdd
#           SDA is running on P9_22
#           SCL is running on P9_21


import gpiod
import sys
import smbus
import time
import operator
from functools import reduce

BOARD_ROWS = 8
BOARD_COLS = 8


sketch_board = [[" " for i in range(BOARD_COLS)] for j in range(BOARD_ROWS)]
cursor = [0, 0]


# smbus temp
sensor_addresses = [0x48, 0x4a]

# smbus matrix configuration
bus = smbus.SMBus(2)  # Use i2c bus 2
matrix = 0x70         # Use address 0x70

delay = 1  # Delay between images in s
bus.write_byte_data(matrix, 0x21, 0)   # Start oscillator (p10)
bus.write_byte_data(matrix, 0x81, 0)   # Disp on, blink off (p11)
bus.write_byte_data(matrix, 0xe7, 0)   # Full brightness (page 15)

green_channel = [0x0a for i in range(BOARD_COLS)]
red_channel = [0x00 for i in range(BOARD_COLS)]

ACCEL_DEFAULT_X = 8
ACCEL_DEFAULT_Y = 5

cur_accel = [ACCEL_DEFAULT_X, ACCEL_DEFAULT_Y]
ADXL345 = '/sys/class/i2c-adapter/i2c-2/2-0053/iio:device0'

X_ACCEL_PATH = "/in_accel_x_raw"
Y_ACCEL_PATH = "/in_accel_y_raw"

TOL = 50


x_file = open(ADXL345 + X_ACCEL_PATH, "r")
y_file = open(ADXL345 + Y_ACCEL_PATH, "r")


def read_adxl345():
    delta = [0, 0]

    x_file.seek(0)
    y_file.seek(0)

    new_data = [int(x_file.read().strip()), int(y_file.read().strip())]

    delta = [n - o for n, o in zip(new_data, cur_accel)]

    x_is_bigger = abs(delta[0]) > abs(delta[1])

    if (delta[0] > -TOL and x_is_bigger):
        return 's'
    elif (delta[0] < TOL and x_is_bigger):
        return 'w'
    elif (delta[1] < -TOL and not x_is_bigger):
        return 'a'
    elif (delta[1] > TOL and not x_is_bigger):
        return 'd'
    elif (delta[0] < ACCEL_DEFAULT_X + TOL) or (delta[0] > ACCEL_DEFAULT_X - TOL) or (delta[1] < ACCEL_DEFAULT_Y + TOL) or (delta[1] > ACCEL_DEFAULT_Y - TOL):
        return ""


# combines the channels alternatin between green value and red value, creating 16 element list
# [g0, r0, g1, r1, .. gN,rN]


def combine_channels():
    return list(reduce(operator.add, zip(green_channel, red_channel)))


def update_channels(r, c):
    green_channel[r] = green_channel[r] | (1 << c)
    red_channel[r] = red_channel[r] | (1 << c)


def clear_channels():
    for i in range(BOARD_COLS):
        green_channel[i] = 0x00
        red_channel[i] = 0x00


def print_event(event):
    if event.type == gpiod.LineEvent.FALLING_EDGE:
        evstr = 'FALLING EDGE'
    else:
        raise TypeError('Invalid event type')

    print('event: {} offset: {} timestamp: [{}.{}]'.format(evstr,
                                                           event.source.offset(),
                                                           event.sec, event.nsec))


def print_board(board):
    for r_id, row in enumerate(board):
        if r_id == 0:
            [print(f"   {i}", end=" ") if i == 0 else print(
                f"{i} ", end="") for i in range(BOARD_COLS)]
            print("")
        print(f"{r_id}.", end=" ")
        for c_id, col in enumerate(row):
            print(col, end=" ")
        print("")


def clear_board(board):
    clear_channels()
    bus.write_i2c_block_data(matrix, 0, combine_channels())
    for r_id, row in enumerate(board):
        for c_id, col in enumerate(row):
            board[r_id][c_id] = " "


def draw():
    update_channels(cursor[0], cursor[1])
    bus.write_i2c_block_data(matrix, 0, combine_channels())
    sketch_board[cursor[0]][cursor[1]] = "X"


def valid_move(r, c):
    if r >= 0 and r < BOARD_ROWS and c >= 0 and c < BOARD_COLS:
        return True
    else:
        print("Invalid move")
        return False


def update_pos(r=cursor[0], c=cursor[1]):
    print(r, c)
    if valid_move(r, c):
        cursor[0] = r
        cursor[1] = c

    else:
        sketch_board[cursor[0]][cursor[1]] = "O"


def parse_cmd(cmd):
    pcmd = str.lower(cmd.strip())
    if pcmd == "quit":
        exit()
    elif pcmd == "clear":
        clear_board(sketch_board)

    if pcmd == "w":
        update_pos(cursor[0]-1, cursor[1])
    elif pcmd == "a":
        update_pos(cursor[0], cursor[1]-1)
    elif pcmd == "s":
        update_pos(cursor[0]+1, cursor[1])
    elif pcmd == "d":
        update_pos(cursor[0], cursor[1]+1)
    elif pcmd == "c":
        clear_board(sketch_board)
    else:
        return
    draw()


def read_tmp():
    temp = [0, 0]
    for i, sensor in enumerate(sensor_addresses):
        temp[i] = bus.read_byte_data(sensor, 0)
    return temp


clear_board(sketch_board)
update_pos()

while True:
    temps = read_tmp()
    if (any(t > 25 for t in temps)):
        clear_board(sketch_board)
        time.sleep(3)
    else:
        cmd = read_adxl345()
        if cmd != "":
            parse_cmd(cmd)
    time.sleep(0.25)
