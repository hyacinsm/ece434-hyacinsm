#!/usr/bin/env python3
# //////////////////////////////////////
#
#   Author: Sean Hyacinthe
#   Date: 12/11/23
#
# 	Runs an etch-sketch game using buttong connected as described in the
#   wiring diagram. Led's are physically wired to button to indicate a
#   sucessful press. Buttons are active high.
#
#   * if mulitple buttons are pressed at once the board is cleared
#
# 	Wiring:	Yellow:     Pos 1 btn(P8_16) - Up
#           Green :     Pos 2 btn(P9_14) - Down
#           Red   :     Pos 3 btn(P9_16) - Left
#           Blue   :     Pos 4 btn(P9_23) - Right
#           LED's anode are connected to same node as each button gnd terminal


import gpiod
import sys


# gpio d stuff

CONSUMER = 'getset'
CHIP = '1'
getoffsets = [14, 18, 19, 17]
idx = [0, 1, 2, 3]
offset_cmd = ["w", "s", "a", "d"]
offset_2_cmd = dict(zip(idx, offset_cmd))


def print_event(event):
    if event.type == gpiod.LineEvent.FALLING_EDGE:
        evstr = 'FALLING EDGE'
    else:
        raise TypeError('Invalid event type')

    print('event: {} offset: {} timestamp: [{}.{}]'.format(evstr,
                                                           event.source.offset(),
                                                           event.sec, event.nsec))


chip = gpiod.Chip(CHIP)

getlines = chip.get_lines(getoffsets)
getlines.request(consumer=CONSUMER, type=gpiod.LINE_REQ_EV_BOTH_EDGES)


# board constants
BOARD_ROWS = 8
BOARD_COLS = 10

sketch_board = [[" " for i in range(BOARD_COLS)] for j in range(BOARD_ROWS)]
cursor = [0, 0]


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
    for r_id, row in enumerate(board):
        for c_id, col in enumerate(row):
            board[r_id][c_id] = " "


def draw():
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

    draw()


def gpio_input():
    ev_lines = getlines.event_wait(sec=1)
    if ev_lines:
        for line in ev_lines:
            event = line.event_read()
    vals = getlines.get_values()

    # checks if multiple buttons are pressed
    if vals.count(1) > 1:
        return "c"

    return offset_2_cmd.get(vals.index(1)) if 1 in vals else ""


update_pos()
print_board(sketch_board)
print("Pos 1 - up\nPos 2 - down\nPos 3 - left\nPos 4 - right\n*Press multiple buttons to clear board")

while True:
    cmd = gpio_input()
    if cmd != "":
        parse_cmd(cmd)
        print_board(sketch_board)
