# <center> ECE 434 hW06

#### <center> By: Sean Hyacinthe

## What Every Driver Developer Should Know about RT

1. She works at National Instruments.

2. PREEMPT_RT is "a set of patches for the Linux Kernel that enable real-time computing capabilities."

3. Mixed criticality is a term used to describe complex embedded systems that typically separate responsibilities into real-time needs and non-time-critical tasks.

4. Because the configuration using PREEMPT_RT shares an OS, the drivers can affect the RT tasks that must be executed.

5. The triangle is a delta representing the difference between when an interrupt occurs and when the interrupt is serviced in real life.

6. A cyclic test is that measures the amount of time a thread actually sleeps compared to the time it was expected to sleep for

7. In Figure 2, the difference shown is reality vs expected sleep durations for the cyclic test. The graph shows the PREEMPT and PREEMPT_RT OS cyclic test results. The main emphasis is on the wider distribution for the non-RTOS compared to the low variability in an RT system.

8. Dispatch latency is the time from the hardware firing and getting to the scheduler. Scheduling latency is the amount from the scheduler acknowledging the interrupt to it getting run on the CPU.

9. The mainline model is an example of long-running interrupts running on the CPU.

10. The lower-priority long-running interrupt that is being serviced

11. To start the external event sooner, PREEMPT_RT uses force IRQ threads to wake up threads ready to be executed in the interrupt handler.





## PREEMPT_RT Simulation

1. The figure reference is the cyclictest.png in this directory. Based on the distribution spread for the RTOS, the upper bound of latency is 150 microseconds. In contrast, the standard Beagle OS has a much wider range of variability and doesn't seem bounded. The load I used to compare the two OS was an infinite for loop I ran in the terminal.


