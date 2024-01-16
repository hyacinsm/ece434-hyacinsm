# <center> ECE434 HW04

#### <center> By: Sean Hyacinthe

## Summary of Files
etch_setup.sh - the setup script to run the flask etch n sketch program

flask_etch_sketch.py - the actual logic of the etch n sketch and interace between webserver and BBB

kernel_tmp.sh - the setup script for running two tmp101 sensors on i2c

kernel_tmp.py - the script collecting data from sensors

mmap_input.sh - the setup script for configuring the need gpio pins for reading button input

mmap_input.c - the script reading button values and controlling USR LEDs

mmap_toggle.py - is the script used for gathering data on the toggle speed of mmap vs sys/gpio interface

\templates\ - holds the html files from formating the flask server page

\static\ - contains the CSS files for the buttons on the template page

\photos\ - contains all the photos asked for in hw04


## Memory Map of the BBB

<center>

| Memory Map  |
| :---------: |
| 0x44E0_7000 |
|    gpio0    |
| 0x44E0_7FFF |
| 0x4804_C000 |
|    gpio1    |
| 0x4804_CFFF |
| 0x481A_C000 |
|    gpio2    |
| 0x481A_CFFF |
| 0x481A_E000 |
|    gpio3    |
| 0x481A_EFFF |
| 0x4C00_0000 |
|    EMIF0    |
| 0x4CFF_FFFF |
| 0x8000_0000 |
| EMIFO SDRAM |
| 0xBFFF_FFF  |

</center>

## GPIO Using mmap Function

2. The results of using mmap were slightly faster than using the /sys/gpio interface.

<center>

| Sleep    | Period (s) |
| :------- | :--------: |
| 0.00025  |  0.000700  |
| 0.000023 |  0.000245  |
| 0.00002  |  0.000235  |
| 0.00001  |  0.000217  |

</center>
