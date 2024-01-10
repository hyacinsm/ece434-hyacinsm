#!/usr/bin/env python3
# From: https://towardsdatascience.com/python-webserver-with-flask-and-raspberry-pi-398423cc6f5d

import gpiod
CHIP = '0'		# P9_11
offsets=[30]

from flask import Flask, render_template
app = Flask(__name__)

chip = gpiod.Chip(CHIP)
lines = chip.get_lines(offsets)

# Set button as an input
lines.request(consumer="app2.py", type=gpiod.LINE_REQ_DIR_IN)

@app.route("/")
def index():
	# Read Button Status
	vals = lines.get_values()
	templateData = {
        'title' : 'GPIO input Status!',
        'button'  : vals,
        }
	return render_template('index2.html', **templateData)
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8081, debug=True)
