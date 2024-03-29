# ECE 434 Embedded Linux HW01 #
#### <center> Date: 12/11/23 &emsp; By: Sean Hyacinthe

#### Homework Overview

Parts 1-3 compared performance across c and python scripts for various GPIO methods on the BBB. The results are compiled into two table under sections 2.3 & 3.1

The "button_etch_sketch" is an extension of the hw01 etch a sketch program. Instead of using terminal input, buttons were added. My actual circuit wiring is described in the python file. To use the program, just run the file. Controls are explained in the python file.

### <center> <u> Measuring GPIO on Oscilloscope </u>

#### 1. Shell Script
1.1 Using the ./blinkLED.sh script the maximum, minimum voltage:

&emsp; &emsp; &emsp; &emsp; Max Voltage:  4.1 V
&emsp; &emsp; &emsp; &emsp; Min Voltage:  -300 mV

1.2 The measured frequency for the blink was:

&emsp; &emsp; &emsp; &emsp; Frequency:  980 mHz
&emsp; &emsp; &emsp; Period:  1.02 s

1.3 Using htop the cpu usage statistcs is 4.6%

1.4 Tables of results from varying sleep duration in ./blinkLED.sh

<center> 

| Sleep       | Period (s)   |CPU Usage %|
| :---        |    :----:    |      ---: |
| 0.0015      | < 0.030      | 88.1      |
| 0.0035      | 0.030        | 76.5      |
| 0.0075      | 0.035        | 60.8      |
| 0.015       | 0.045        | 43.5      |
| 0.03        | 0.075        | 25.9      |
| 0.06        | 0.135        | 15.3      |
| 0.12        | 0.260        | 9.9       |
| 0.25        | 0.520        | 6.6       |
| 0.5         | 1.02         | 4.6       |

</center> 

1.5 The period was fairly consistent until the sleep duration was less than 30 ms or 0.03 s.

1.6 Opening another application while running the blink script slightly decreased my period

1.7 After removing all the comments and the error handing for the export  my period increased and became less stable

1.8 The lowest measurable period I could get using the shell script was 30 ms.

#### 2. Python Script
2.1 The measured frequency for the blink was:

&emsp; &emsp; &emsp; &emsp; Frequency:  1 Hz
&emsp; &emsp; &emsp; Period:  1.00 s

2.2 For the given python script the CPU usage was 5.2 %

2.3 The results for the python file

<center>

| Sleep -Py    | Period (s) -Py  |CPU Usage % - Py| Sleep  -C     | Period (s) -C   |CPU Usage % -C|
| :---         |     :----:      |      ---:      | :---          |    :----:       |         ---: |
| 0.0009       | 0.0002          | 51.3           | 0.00001       | 0.000220        | 44.5         |
| 0.00018      | 0.0027          | 28.3           | 0.00075       | 0.0022          | 28.3         |
| 0.0015       | 0.0047          | 13.6           | 0.0015        | 0.0037          | 22.6         |
| 0.0035       | 0.008           | 11.1           | 0.0035        | 0.008           | 37.1         |
| 0.0075       | 0.016           | 8.1            | 0.0075        | 0.015           | 22.1         |
| 0.015        | 0.034           | 8.6            | 0.015         | 0.030           | 12.4         |
| 0.03         | 0.063           | 7.7            | 0.03          | 0.060           | 12.9         |

</center>

#### 3. C Script
2.1 The measured frequency for the blink was:

&emsp; &emsp; &emsp; &emsp; Frequency:  1 Hz
&emsp; &emsp; &emsp; Period:  1.00 s

2.2 For the given c script the CPU usage was 5.2 %

2.3 The results for the python file

### 3. GPIOD Performance in Python and C
3.1 Metrics for Python script:

<center>

| Sleep -Py   | T(s)- Py    |CPU % - Py | Sleep -C   | T(s) - C    |CPU % -C   |
| :---        |    :----:   |      ---: | :---       |    :----:   |      ---: |
| 0.00002344  | 0.000260    | 52.2      | 0.000023   | 0.000230    | 36.2      |
| 0.00004688  | 0.000300    | 37.4      | 0.000047   | 0.000300    | 37.4      |
| 0.00009375  | 0.000400    | 30.1      | 0.000094   | 0.000380    | 17.6      |
| 0.0001875   | 0.000580    | 22.4      | 0.000187   | 0.000560    | 16.3      | 
| 0.000375    | 0.00126     | 17.5      | 0.000375   | 0.00140     | 20.4      |
| 0.00075     | 0.0022      | 20.8      | 0.00075    | 0.0022      | 15.5      |

# hw02 grading

| Points      | Description | Comment
| ----------- | ----------- | -------
|  2/2 | Buttons and LEDs 
|  8/8 | Etch-a-Sketch works
|  2/2 | Measuring a gpio pin on an Oscilloscope 
|  2/2 | Questions answered
|  4/4 | Table complete
|  2/2 | gpiod
| 20/20   | **Total**

Tables look good.