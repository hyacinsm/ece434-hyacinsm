import sys
from flask import Flask, render_template, request
app = Flask(__name__)


@app.route("/")
def index():
    # Read GPIO Status
    vals = getlines.get_values()
    templateData = {
        'button': getlines.get_values()[0],
        'ledRed': setlines.get_values()[0]
    }
    return render_template('index5.html', **templateData)


@app.route("/<deviceName>/<action>")
def action(deviceName, action):
    if action == "on":
        setlines.set_values([1])
    if action == "off":
        setlines.set_values([0])
    if action == "toggle":
        setlines.set_values([not setlines.get_values()[0]])

    templateData = {
        'button': getlines.get_values()[0],
        'ledRed': setlines.get_values()[0]
    }
    return render_template('index5.html', **templateData)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081, debug=True)
