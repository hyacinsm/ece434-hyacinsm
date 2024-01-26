# <center> ECE434 HW05

#### <center> By: Sean Hyacinthe

## Installing the Kernel Source

A. My pin 16 does not work, so I used pin P9_14 for the demo. Both P9_14 & P9_16 are pwm pins so the setup should be the say with the exception of the pin # for the push button. My could is written as if P9_16 works

## Summary of Files

adxl345_etch_sketch.py -> the etch n sketch variation controlled by an accelometer
adxl345_i2cc.py -> test script for reading data of the sensor
adxl345_setup -> the script to run pin configuration and set up i2c driver for sensor
gpio_test_double.c -> controling two sets of leds and push buttons with kernel driver
gpio_test_single.c -> control a single led and push button using kernel module
led.c -> program to blink led at two different rates
Makefile -> based on the make example exercise

# hw05 grading

| Points      | Description |
| ----------- | ----------- |
|  0/0 | Project 
|  2/2 | Makefile
|  5/6 | Kernel Source | Version missing
|  6/6 | Kernel Modules: hello, ebbchar, gpio_test, led
|  4/4 | Etch-a-Sketch
|  2/2 | Blink at different rates
| 19/20 | **Total**

*My comments are in italics. --may*

