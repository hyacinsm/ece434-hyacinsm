#!/usr/bin/env python3
# /////////////////////////////////////////
#
#   Author: Sean Hyacinthe & Mark A Yoder
#   Date: 12/18/24
#
#   Description: Testing to make sure encoder code works separately
#
#   Wiring:
#               ./config-pin P8_12 eqep => A
#               ./config-pin P8_11 eqep => B
#               ./config-pin P8_33 eqep => B
#               ./config-pin P8_35 eqep => A

import time

eQEP_VERT = '2'
eQEP_HORI = '1'

COUNTERPATH_VERT = '/dev/bone/counter/'+eQEP_VERT+'/count0'
COUNTERPATH_HORI = '/dev/bone/counter/'+eQEP_HORI+'/count0'

encoders = [COUNTERPATH_HORI, COUNTERPATH_VERT]


ms = 100  # Time between samples in ms
maxCount = '10000'

# Set the eEQP maximum count
for path in encoders:
    f = open(path+'/ceiling', 'w')
    f.write(maxCount)
    f.close()

# Clear the eEQP count
for path in encoders:
    f = open(path+'/count', 'w')
    f.write("5000")
    f.close()

# Enable
for path in encoders:
    f = open(path+'/enable', 'w')
    f.write('1')
    f.close()


olddata = [-1, -1]
while True:
    for i, path in enumerate(encoders):
        f = open(path+'/count', 'r')

        f.seek(0)
        data = f.read()[:-1]
        # Print only if data changes
        if data != olddata[i]:
            olddata[i] = data
            print(f"Encoder {i+1} data = " + data)
        time.sleep(ms/1000)
        f.close()
