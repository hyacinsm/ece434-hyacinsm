# <center> ECE 434 hW06

#### <center> By: Sean Hyacinthe

## What Every Driver Developer Should Know about RT

1. She works at National Instruments.
2. PREEMPT_RT is "a set of patches for the Linux Kernel that enable real-time computing capabilites."
3. Mixed criticality is a term used to describe complex embedded systems that typically seperate responsiblies into real-time needs and non-time critical tasks.
4. Because the configuration using PREEMPT_RT share an OS, the drivers the potential to effect the RT tasks that need to be executed. 
5. The triangle is delta and represents the difference between when an interrupt occurrs and when the interrupt is serviced in real life.
6. A cyclic test is that measures the amount of time a threads actually sleeps for compared to the time it was expected to sleep for
7. In figure two the difference shown is reality-expected sleep durations for the cyclic test. The graph shows the PREEMPT and PREEMPT_RT OS cyclic test results. The main emphasis is on the wider distribution for the non-RTOS compared to the low variablity in an RT system.
8. Dispatch latency is the time from the hardware firing and getting to the scheduler. Scheduling latency is the amount from the scheduler acknowledging the interrupt to it getting ran on CPU.
9. The mainline model is an example of long running interrupts running on the cpu.
10. The lower-priority long-running interrupt that is being serviced
11. To start the external event sooner, PREEMPT_RT by using force IRQ threads to wake up threads that are ready to be executed in the interrupt handler.
