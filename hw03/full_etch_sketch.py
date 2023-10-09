#!/usr/bin/env python3
# //////////////////////////////////////
#
#   Author: Sean Hyacinthe
#   Date: 12/18/23
#
# 	Runs an etch-sketch game on an LED matrix with to rotary encoders for
#   drawing. Hold finger on temp sensor to clear board. Press Ctrl -C to quit
#
#   Setup : run the ./setup.sh to configure the needed pins
#   Wiring:	tmp101_gnd is has pin add0 wired to GND
#           tmp101_vcc is has pin add0 wired to 3.3 V
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

# encoders
eQEP_VERT = '2'
eQEP_HORI = '1'

COUNTERPATH_VERT = '/dev/bone/counter/'+eQEP_VERT+'/count0'
COUNTERPATH_HORI = '/dev/bone/counter/'+eQEP_HORI+'/count0'

encoders = [COUNTERPATH_HORI, COUNTERPATH_VERT]

ms = 100  # Time between samples in ms
MAX_COUNT = '10000'
old_data = [-1, -1]


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


def read_encoders():
    # represents change in the horizontal, vertical
    delta = [0, 0]
    for i, path in enumerate(encoders):
        f = open(path+'/count', 'r')

        f.seek(0)
        data = f.read()[:-1]
        # Print only if data changes
        if data != old_data[i]:
            delta[i] = int(old_data[i]) - int(data)
            old_data[i] = data
            print(f"Encoder {i+1} data = " + data)
        time.sleep(ms/1000)
        f.close()

    if (delta[1] > 0):
        return 'w'
    elif (delta[1] < 0):
        return 's'
    elif (delta[0] > 0):
        return 'd'
    elif (delta[0] < 0):
        return 'a'
    else:
        return ""

# Set the eEQP maximum count


def set_encoders_max():
    for path in encoders:
        f = open(path+'/ceiling', 'w')
        f.write(MAX_COUNT)
        f.close()

# Clear the eEQP count


def set_encoders_min():
    for path in encoders:
        f = open(path+'/count', 'w')
        f.write(str(5000))
        f.close()

# Enable


def enable_encoders():
    for path in encoders:
        f = open(path+'/enable', 'w')
        f.write('1')
        f.close()

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


set_encoders_max()
set_encoders_min()
enable_encoders()
clear_board(sketch_board)
update_pos()
print_board(sketch_board)

while True:
    temps = read_tmp()
    if (any(t > 25 for t in temps)):
        clear_board(sketch_board)
        time.sleep(3)
    else:
        cmd = read_encoders()
        if cmd != "":
            parse_cmd(cmd)
            print_board(sketch_board)
    time.sleep(0.25)
