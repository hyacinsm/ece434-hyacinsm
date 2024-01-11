# <center> ECE434 HW04

#### <center> By: Sean Hyacinthe

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

## GPIO Using mmap(...)

2. The results of using mmap were slightly faster than using the /sys/gpio interface.

<center>

| Sleep    | Period (s) |
| :------- | :--------: |
| 0.00025  |  0.000700  |
| 0.000023 |  0.000245  |
| 0.00002  |  0.000235  |
| 0.00001  |  0.000217  |

</center>
