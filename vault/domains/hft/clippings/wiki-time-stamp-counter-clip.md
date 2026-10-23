---
title: Time Stamp Counter - Wikipedia
source: https://en.wikipedia.org/wiki/Time_Stamp_Counter
published: '2006-03-28'
site: Wikimedia Foundation, Inc.
clipped: '2026-10-23'
---

# Time Stamp Counter - Wikipedia

# Time Stamp Counter

The **Time Stamp Counter** (**TSC**) is a [64-bit](https://en.wikipedia.org/wiki/64-bit_computing) [register](https://en.wikipedia.org/wiki/Processor_register) present on all [x86](https://en.wikipedia.org/wiki/X86) processors since the [Pentium](https://en.wikipedia.org/wiki/Intel_P5). It counts the number of [CPU](https://en.wikipedia.org/wiki/Central_processing_unit) [cycles](https://en.wikipedia.org/wiki/Clock_rate) since its reset. The instruction `RDTSC` returns the TSC in EDX:EAX. In [x86-64](https://en.wikipedia.org/wiki/X86-64) mode, `RDTSC` also clears the upper 32 bits of [RAX](https://en.wikipedia.org/wiki/RAX_register) and [RDX](https://en.wikipedia.org/wiki/RDX_register). Its [opcode](https://en.wikipedia.org/wiki/Opcode) is `0F 31`.[\[1\]](#cite_note-1)[Pentium](https://en.wikipedia.org/wiki/Pentium) competitors such as the [Cyrix](https://en.wikipedia.org/wiki/Cyrix) [6x86](https://en.wikipedia.org/wiki/6x86) did not always have a TSC and may consider `RDTSC` an illegal instruction. Cyrix included a Time Stamp Counter in their [MII](https://en.wikipedia.org/wiki/Cyrix_6x86#6x86MX_/_MII).

## Use

[
[edit](/w/index.php?title=Time_Stamp_Counter&action=edit§ion=1)]

The Time Stamp Counter was once a high-resolution, low-overhead way for a program to get CPU timing information. With the advent of [multi-core](https://en.wikipedia.org/wiki/Multi-core)/[hyper-threaded](https://en.wikipedia.org/wiki/Hyper-threaded) CPUs, systems with [multiple CPUs](https://en.wikipedia.org/wiki/Symmetric_multiprocessing), and [hibernating](<https://en.wikipedia.org/wiki/Hibernation_(computing)>) [operating systems](https://en.wikipedia.org/wiki/Operating_system), the TSC cannot be relied upon to provide accurate results — unless great care is taken to correct the possible flaws: rate of tick and whether all cores (processors) have identical values in their time-keeping registers. There is no promise that the timestamp counters of multiple CPUs on a single [motherboard](https://en.wikipedia.org/wiki/Motherboard) will be synchronized. Therefore, a program can get reliable results only by limiting itself to run on one specific CPU. Even then, the CPU speed may change because of power-saving measures taken by the OS or [BIOS](https://en.wikipedia.org/wiki/BIOS), or the system may be hibernated and later resumed, resetting the TSC. In those latter cases, to stay relevant, the program must re-calibrate the counter periodically.

Relying on the TSC also reduces portability, as other processors may not have a similar feature. Recent Intel processors include a constant rate TSC (identified by the kern.timecounter.invariant_tsc sysctl on FreeBSD or by the "`constant_tsc`" flag in Linux's `/proc/cpuinfo`). With these processors, the TSC ticks at the processor's nominal frequency, regardless of the actual CPU clock frequency due to turbo or power saving states.  Hence TSC ticks are counting the passage of time, not the number of CPU clock cycles elapsed.

On [Windows](https://en.wikipedia.org/wiki/Windows) platforms, Microsoft strongly discourages using the TSC for high-resolution timing for exactly these reasons, providing instead the [Windows APIs](https://en.wikipedia.org/wiki/Windows_API) `QueryPerformanceCounter` and `QueryPerformanceFrequency` (which itself uses RDTSCP if the system has an invariant TSC, i.e. the frequency of the TSC doesn't vary according to the current core's frequency).<sup>[\[2\]](#cite_note-2)</sup> On [Linux](https://en.wikipedia.org/wiki/Linux) systems, a program can get similar function by reading the value of `CLOCK_MONOTONIC_RAW` clock using the `clock_gettime` function.[\[3\]](#cite_note-3)

Starting with the [Pentium Pro](https://en.wikipedia.org/wiki/Pentium_Pro), Intel processors have practiced [out-of-order execution](https://en.wikipedia.org/wiki/Out-of-order_execution), where instructions are not necessarily performed in the order they appear in the program.  This can cause the processor to execute `RDTSC` earlier than a simple program expects, producing a misleading cycle count.<sup>[\[4\]](#cite_note-4)</sup>  The programmer can solve this problem by inserting a serializing instruction, such as [CPUID](https://en.wikipedia.org/wiki/CPUID), to force every preceding instruction to complete before allowing the program to continue. The `RDTSCP` instruction is a variant of `RDTSC` that features partial serialization of the instruction stream, but should not be considered as serializing.

## Implementation in various processors

[
[edit](/w/index.php?title=Time_Stamp_Counter&action=edit§ion=2)]

Intel processor families increment the time-stamp counter differently:[\[5\]](#cite_note-5)

- For [Pentium M](https://en.wikipedia.org/wiki/Pentium_M) processors (family [06H], models [09H, 0DH]); for Pentium 4 processors,[Intel Xeon](https://en.wikipedia.org/wiki/Intel_Xeon) processors (family [0FH], models [00H, 01H, or 02H]); and for P6 family processors: the time-stamp counter increments with every internal processor clock cycle. The internal processor clock cycle is determined by the current core-clock to busclock ratio. Intel SpeedStep technology transitions may also impact the processor clock.
- For [Pentium 4](https://en.wikipedia.org/wiki/Pentium_4) processors, Intel Xeon processors (family [0FH], models [03H and higher]); for[Intel Core Solo](https://en.wikipedia.org/wiki/Intel_Core_Solo) and[Intel Core Duo](https://en.wikipedia.org/wiki/Intel_Core_Duo) processors (family [06H], model [0EH]); for the Intel Xeon processor 5100 series and[Intel Core 2 Duo](https://en.wikipedia.org/wiki/Intel_Core_2_Duo) processors (family [06H], model [0FH]); for Intel Core 2 and Intel Xeon processors (family [06H], display_model [17H]); for[Intel Atom](https://en.wikipedia.org/wiki/Intel_Atom) processors (family [06H], display_model [1CH]): the time-stamp counter increments at a constant rate. That rate may be set by the maximum core-clock to bus-clock ratio of the processor or may be set by the maximum resolved frequency at which the processor is booted. The maximum resolved frequency may differ from the maximum qualified frequency of the processor.

The specific processor configuration determines the behavior. Constant TSC behavior ensures that the duration of each clock tick is uniform and makes it possible to use the TSC as a wall-clock timer even if the processor core changes frequency. This is the architectural behavior for all later Intel processors.

[AMD processors](https://en.wikipedia.org/wiki/AMD_processors) up to the [K8](https://en.wikipedia.org/wiki/AMD_K8) core always incremented the time-stamp counter every clock cycle.<sup>[\[6\]](#cite_note-6)</sup> Thus, power management features were able to change the number of increments per second, and the values could get out of sync between different cores or processors in the same system. For Windows, AMD provides a utility<sup>[\[7\]](#cite_note-7)</sup> to periodically synchronize the counters on multiple core CPUs.
Since the [family 10h](https://en.wikipedia.org/wiki/AMD_K10) (Barcelona/Phenom), AMD chips feature a constant TSC, which can be driven either by the [HyperTransport](https://en.wikipedia.org/wiki/HyperTransport) speed or the highest P state. A [CPUID](https://en.wikipedia.org/wiki/CPUID) bit (`Fn8000_0007:EDX_8`) advertises this; Intel-CPUs also report their invariant TSC on that bit.

## Operating system use

[
[edit](/w/index.php?title=Time_Stamp_Counter&action=edit§ion=3)]

An operating system may provide methods that both use and don't use the `RDTSC` instruction for time keeping, under administrator control. For example, on some versions of the [Linux kernel](https://en.wikipedia.org/wiki/Linux_kernel), [seccomp sandboxing mode](https://en.wikipedia.org/wiki/Seccomp) disables `RDTSC`.<sup>[\[8\]](#cite_note-8)</sup>  It can also be disabled using the `PR_SET_TSC` argument to the `prctl()` system call.[\[9\]](#cite_note-9)

## Use in exploiting cache side-channel attacks

[
[edit](/w/index.php?title=Time_Stamp_Counter&action=edit§ion=4)]

The time stamp counter can be used to time instructions accurately which can be exploited in the [Meltdown](<https://en.wikipedia.org/wiki/Meltdown_(security_vulnerability)>) and [Spectre](<https://en.wikipedia.org/wiki/Spectre_(security_vulnerability)>) security vulnerabilities.[\[10\]](#cite_note-10)<sup>[\[11\]](#cite_note-11)</sup> However, if this is not available other counters or timers can be used, as is the case with the [ARM](https://en.wikipedia.org/wiki/ARM_architecture) processors vulnerable to this type of attack.

## Other architectures

[
[edit](/w/index.php?title=Time_Stamp_Counter&action=edit§ion=5)]

Other processors also have registers which count CPU clock cycles, but with different names. For instance, on the [AVR32](https://en.wikipedia.org/wiki/AVR32), it is called the Performance Clock Counter (PCCNT) register. [SPARC V9](https://en.wikipedia.org/wiki/SPARC_V9) provides the `TICK` register. [PowerPC](https://en.wikipedia.org/wiki/PowerPC) provides the 64-bit `TBR` register.

ARMv7 provides a Cycle Counter Register CCNT as part of its "Performance Monitoring Unit", and instructions to read and write the counter, but the counter is by default disabled (to save power) and the instructions are privileged.<sup>[\[12\]](#cite_note-12)</sup>  User-mode access can be enabled.[\[13\]](#cite_note-13)[ARMv7](https://en.wikipedia.org/wiki/ARMv7)<sup>[\[14\]](#cite_note-14)</sup> and [ARMv8-A](https://en.wikipedia.org/wiki/ARMv8)<sup>[\[15\]](#cite_note-15)</sup> architectures provide a generic counter which counts at a constant frequency, but this frequency is typically at most 50 MHz.[\[16\]](#cite_note-16)

## See also

[
[edit](/w/index.php?title=Time_Stamp_Counter&action=edit§ion=6)]

- [High Precision Event Timer](https://en.wikipedia.org/wiki/High_Precision_Event_Timer) (HPET)

## References

[
[edit](/w/index.php?title=Time_Stamp_Counter&action=edit§ion=7)]

1. [↑](#cite_ref-1)[*Intel 64 and IA-32 Architectures Software Developer's Manual Volume 2B: Instruction Set Reference, M-Z*](http://www.intel.com/content/dam/www/public/us/en/documents/manuals/64-ia-32-architectures-software-developer-vol-2b-manual.pdf) (PDF). p. 545.
2. [↑](#cite_ref-2)[*Game Timing and Multicore Processors*](http://msdn.microsoft.com/en-us/library/ee417693%28VS.85%29.aspx) . pp. 251–252.
3. [↑](#cite_ref-3)["clock_getres, clock_gettime, clock_settime - clock and timer functions"](http://pubs.opengroup.org/onlinepubs/9699919799/functions/clock_getres.html) .
4. [↑](#cite_ref-4)["Using the RDTSC Instruction for Performance Monitoring"](http://www.ccsl.carleton.ca/~jamuir/rdtscpm1.pdf) (PDF).
5. [↑](#cite_ref-5) "Volume 3A, Chapter 16".[*Intel 64 and IA-32 Architectures Software Developer's Manual*](http://www.intel.com/products/processor/manuals/) .
6. [↑](#cite_ref-6) "Volume 3".[*AMD64 Architecture Programmer's Manual*](https://www.amd.com/us-en/Processors/DevelopWithAMD/0,,30_2252_11467_11513,00.html) .
7. [↑](#cite_ref-7)["AMD Dual-Core Optimizer"](https://www.amd.com/us-en/Processors/TechnicalResources/0,,30_182_871_13118,00.html?redir=COGA01) .
8. [↑](#cite_ref-8)["cr0 blog: Time-stamp counter disabling oddities in the Linux kernel"](http://blog.cr0.org/2009/05/time-stamp-counter-disabling-oddities.html) . May 2009.
9. [↑](#cite_ref-9) –[Linux](https://en.wikipedia.org/wiki/Linux) Programmer's[Manual](https://en.wikipedia.org/wiki/Man_page) – System Calls from Manned.org
10. [↑](#cite_ref-10)["meltdown.c"](https://gist.github.com/mentha/14e6b957183daf4f6dd1657bad0b4a6e) .
11. [↑](#cite_ref-11)["spectre.c"](https://gist.github.com/ErikAugust/724d4a969fb2c6ae1bbd7b2a9e3d4bb6) .
12. [↑](#cite_ref-12)["Cycle Counter Register (CCNT)"](https://developer.arm.com/documentation/ddi0211/h/system-control-coprocessor/system-control-processor-register-descriptions/c15--cycle-counter-register--ccnt-) .[ARM Ltd.](https://en.wikipedia.org/wiki/ARM_Ltd.) Retrieved March 5, 2021.
13. [↑](#cite_ref-13) Protsenko, Sam (14 July 2010).["How to measure program execution time in ARM Cortex-A8 processor?"](https://stackoverflow.com/questions/3247373/how-to-measure-program-execution-time-in-arm-cortex-a8-processor/3250835#3250835) .*[Stack Overflow](https://en.wikipedia.org/wiki/Stack_Overflow)* .
14. [↑](#cite_ref-14)["ARMv7 reference manual"](http://infocenter.arm.com/help/topic/com.arm.doc.ddi0406c/index.html) .
15. [↑](#cite_ref-15)["ARMv8 reference manual"](http://infocenter.arm.com/help/topic/com.arm.doc.ddi0487a.h/index.html) .
16. [↑](#cite_ref-16)[*AArch64 Programmer's Guides: Generic Timer*](https://developer.arm.com/-/media/Arm%20Developer%20Community/PDF/Learn%20the%20Architecture/Generic%20Timer.pdf?revision=c710e7a7-9f52-4901-8c9d-91b19f44f9c7#page=6) (PDF) (Manual).[ARM Ltd.](https://en.wikipedia.org/wiki/ARM_Ltd.) 13 August 2019. p. 6. ARM062-1010708621-30.The system count value is between 56 bits and 64 bits in width, with a frequency typically in the range of 1MHz to 50MHz.

## External links

[
[edit](/w/index.php?title=Time_Stamp_Counter&action=edit§ion=8)]

- [cycle.h](http://www.fftw.org/cycle.h) -[C](https://en.wikipedia.org/wiki/C_programming_language) code to read the high-resolution timer on many CPUs and compilers.
- [AMD engineer on TSC drift in AMD processors](https://lkml.org/lkml/2005/11/4/173)
