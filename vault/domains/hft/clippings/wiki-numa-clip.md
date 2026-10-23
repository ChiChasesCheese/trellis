---
title: Non-uniform memory access - Wikipedia
source: https://en.wikipedia.org/wiki/Non-uniform_memory_access
published: '2002-02-25'
site: Wikimedia Foundation, Inc.
clipped: '2026-10-23'
---

# Non-uniform memory access - Wikipedia

# Non-uniform memory access

**Non-uniform memory access** (**NUMA**) is a [computer memory](https://en.wikipedia.org/wiki/Computer_storage) design used in [multiprocessing](https://en.wikipedia.org/wiki/Multiprocessing), where the memory access time depends on the memory location relative to the processor. Under NUMA, a processor can access its own [local memory](https://en.wikipedia.org/wiki/Local_memory) faster than non-local memory (memory local to another processor or memory shared between processors).<sup>[\[1\]](#cite_note-1)</sup> NUMA is beneficial for workloads with high memory [locality of reference](https://en.wikipedia.org/wiki/Locality_of_reference) and low [lock contention](https://en.wikipedia.org/wiki/Lock_contention), because a processor may operate on a subset of memory mostly or entirely within its own cache node, reducing traffic on the memory bus.[\[2\]](#cite_note-nyu-numa-2)

NUMA architectures logically follow in scaling from [symmetric multiprocessing](https://en.wikipedia.org/wiki/Symmetric_multiprocessing) (SMP) architectures. They were developed commercially during the 1990s by [Unisys](https://en.wikipedia.org/wiki/Unisys), [Convex Computer](https://en.wikipedia.org/wiki/Convex_Computer) (later [Hewlett-Packard](https://en.wikipedia.org/wiki/Hewlett-Packard)), [Honeywell](https://en.wikipedia.org/wiki/Honeywell) Information Systems Italy (HISI) (later [Groupe Bull](https://en.wikipedia.org/wiki/Groupe_Bull)), [Silicon Graphics](https://en.wikipedia.org/wiki/Silicon_Graphics) (later [Silicon Graphics International](https://en.wikipedia.org/wiki/Silicon_Graphics_International)), [Sequent Computer Systems](https://en.wikipedia.org/wiki/Sequent_Computer_Systems) (later [IBM](https://en.wikipedia.org/wiki/IBM)), [Data General](https://en.wikipedia.org/wiki/Data_General) (later [EMC](https://en.wikipedia.org/wiki/EMC_Corporation), now [Dell Technologies](https://en.wikipedia.org/wiki/Dell_Technologies)), [Digital](https://en.wikipedia.org/wiki/Digital_Equipment_Corporation) (later [Compaq](https://en.wikipedia.org/wiki/Compaq), then [HP](https://en.wikipedia.org/wiki/Hewlett-Packard), now [HPE](https://en.wikipedia.org/wiki/Hewlett_Packard_Enterprise)) and [ICL](https://en.wikipedia.org/wiki/International_Computers_Limited). Techniques developed by these companies later featured in a variety of [Unix-like](https://en.wikipedia.org/wiki/Unix-like) [operating systems](https://en.wikipedia.org/wiki/Operating_system), and to an extent in [Windows NT](https://en.wikipedia.org/wiki/Windows_NT).

The first commercial implementation of a NUMA-based Unix system was<sup>[*[where?](<https://en.wikipedia.org/wiki/Wikipedia:Naming_conventions_(geographic_names)>)*]</sup><sup>[*[when?](https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Dates_and_numbers#Chronological_items)*]</sup> the Symmetrical Multi Processing XPS-100 family of servers, designed by Dan Gielan of VAST Corporation for [Honeywell Information Systems](https://en.wikipedia.org/wiki/Honeywell_Information_Systems) Italy.

## Overview

[
[edit](/w/index.php?title=Non-uniform_memory_access&action=edit§ion=1)]

Modern CPUs operate considerably faster than the main memory they use. In the early days of computing and data processing, the CPU generally ran slower than its own memory. The performance lines of processors and memory crossed in the 1960s with the advent of the first [supercomputers](https://en.wikipedia.org/wiki/Supercomputer). Since then, CPUs increasingly have found themselves "starved for data" and forced to stall to wait for data to arrive from memory (e.g. for [Von-Neumann architecture](https://en.wikipedia.org/wiki/Von_Neumann_architecture)-based computers, see [Von Neumann bottleneck](https://en.wikipedia.org/wiki/Von_Neumann_architecture#Von_Neumann_bottleneck)). Many supercomputer designs of the 1980s and 1990s focused on providing high-speed memory access as opposed to faster processors, allowing the computers to work on large data sets at speeds other systems could not approach.

Limiting the number of memory accesses provided the key to extracting high performance from a modern computer. For commodity processors, this meant installing an ever-increasing amount of high-speed [cache memory](https://en.wikipedia.org/wiki/Cache_memory) and using increasingly sophisticated algorithms to avoid [cache misses](https://en.wikipedia.org/wiki/Cache_miss). But the dramatic increase in size of both the operating systems and the applications that run on them has generally overwhelmed these cache-processing improvements. Multi-processor systems without NUMA make the problem considerably worse. Now a system can starve several processors at the same time, notably because only one processor can access the computer's memory at a time.[\[3\]](#cite_note-3)

NUMA attempts to address this problem by providing separate memory for each processor, avoiding the performance hit when several processors attempt to address the same memory. For problems involving spread data (common for [servers](<https://en.wikipedia.org/wiki/Server_(computing)>) and similar applications), NUMA can improve the performance over a single shared memory by a factor of roughly the number of processors (or separate memory banks).<sup>[\[4\]](#cite_note-acm-zmajo-4)</sup> Another approach to addressing this problem is the [multi-channel memory architecture](https://en.wikipedia.org/wiki/Multi-channel_memory_architecture), in which a linear increase in the number of memory channels increases the memory access concurrency linearly.[\[5\]](#cite_note-5)

Of course, not all data ends up confined to a single task, which means that more than one processor may require the same data. To handle these cases, NUMA systems include additional hardware or software to move data between memory banks. This operation slows the processors attached to those banks, so the overall speed increase due to NUMA heavily depends on the nature of the running tasks.[\[4\]](#cite_note-acm-zmajo-4)

## Implementations

[
[edit](/w/index.php?title=Non-uniform_memory_access&action=edit§ion=2)]

[AMD](https://en.wikipedia.org/wiki/Advanced_Micro_Devices) implemented NUMA with its [Opteron](https://en.wikipedia.org/wiki/Opteron) processor (2003), using [HyperTransport](https://en.wikipedia.org/wiki/HyperTransport). [Intel](https://en.wikipedia.org/wiki/Intel) announced NUMA compatibility for its x86 and [Itanium](https://en.wikipedia.org/wiki/Itanium) servers in late 2007 with its [Nehalem](<https://en.wikipedia.org/wiki/Nehalem_(microarchitecture)>) and [Tukwila](<https://en.wikipedia.org/wiki/Tukwila_(processor)>) CPUs.<sup>[\[6\]](#cite_note-6)</sup> Both Intel CPU families share a common [chipset](https://en.wikipedia.org/wiki/Chipset); the interconnection is called Intel [QuickPath Interconnect](https://en.wikipedia.org/wiki/Intel_QuickPath_Interconnect) (QPI), which provides extremely high bandwidth to enable high on-board scalability and was replaced by a new version called Intel [UltraPath Interconnect](https://en.wikipedia.org/wiki/Intel_UltraPath_Interconnect) with the release of [Skylake](https://en.wikipedia.org/wiki/Skylake_microarchitecture) (2017).[\[7\]](#cite_note-7)

## Cache coherent NUMA (ccNUMA)

[
[edit](/w/index.php?title=Non-uniform_memory_access&action=edit§ion=3)]

Nearly all CPU architectures use a small amount of very fast non-shared memory known as [cache](https://en.wikipedia.org/wiki/CPU_cache) to exploit [locality of reference](https://en.wikipedia.org/wiki/Locality_of_reference) in memory accesses. With NUMA, maintaining [cache coherence](https://en.wikipedia.org/wiki/Cache_coherence) across shared memory has a significant overhead. Although simpler to design and build, non-cache-coherent NUMA systems become prohibitively complex to program in the standard [von Neumann architecture](https://en.wikipedia.org/wiki/Von_Neumann_architecture) programming model.[\[8\]](#cite_note-8)

Typically, ccNUMA uses inter-processor communication between cache controllers to keep a consistent memory image when more than one cache stores the same memory location. For this reason, ccNUMA may perform poorly when multiple processors attempt to access the same memory area in rapid succession.  Support for NUMA in [operating systems](https://en.wikipedia.org/wiki/Operating_system) attempts to reduce the frequency of this kind of access by allocating processors and memory in NUMA-friendly ways and by avoiding scheduling and locking algorithms that make NUMA-unfriendly accesses necessary.[\[9\]](#cite_note-9)

Alternatively, cache coherency protocols such as the [MESIF protocol](https://en.wikipedia.org/wiki/MESIF_protocol) attempt to reduce the communication required to maintain cache coherency. [Scalable Coherent Interface](https://en.wikipedia.org/wiki/Scalable_Coherent_Interface) (SCI) is an [IEEE](https://en.wikipedia.org/wiki/IEEE) standard defining a directory-based cache coherency protocol to avoid scalability limitations found in earlier multiprocessor systems. For example, SCI is used as the basis for the NumaConnect technology.[\[10\]](#cite_note-10)[\[11\]](#cite_note-11)

## NUMA vs. cluster computing

[
[edit](/w/index.php?title=Non-uniform_memory_access&action=edit§ion=4)]

One can view NUMA as a tightly coupled form of [cluster computing](https://en.wikipedia.org/wiki/Cluster_computing). The addition of [virtual memory](https://en.wikipedia.org/wiki/Virtual_memory) paging to a cluster architecture can allow the implementation of NUMA entirely in software. However, the inter-node latency of software-based NUMA remains several orders of magnitude greater (slower) than that of hardware-based NUMA.[\[2\]](#cite_note-nyu-numa-2)

## Software support

[
[edit](/w/index.php?title=Non-uniform_memory_access&action=edit§ion=5)]

Since NUMA largely influences memory access performance, certain software optimizations are needed to allow scheduling threads and processes close to their in-memory data.

- [Microsoft](https://en.wikipedia.org/wiki/Microsoft)[Windows 7](https://en.wikipedia.org/wiki/Windows_7) and[Windows Server 2008 R2](https://en.wikipedia.org/wiki/Windows_Server_2008_R2) added support for NUMA architecture over 64 logical cores.<sup>[\[12\]](#cite_note-12)</sup>
- [Java 7](https://en.wikipedia.org/wiki/Java_7) added support for NUMA-aware memory allocator and[garbage collector](<https://en.wikipedia.org/wiki/Garbage_collection_(computer_science)>) .<sup>[\[13\]](#cite_note-13)</sup>
- [Linux kernel](https://en.wikipedia.org/wiki/Linux_kernel) :
  - Version 2.5 provided a basic NUMA support,<sup>[\[14\]](#cite_note-14)</sup> which was further improved in subsequent kernel releases.
  - Version 3.8 of the Linux kernel brought a new NUMA foundation that allowed development of more efficient NUMA policies in later kernel releases.<sup>[\[15\]](#cite_note-15)</sup><sup>[\[16\]](#cite_note-16)</sup>
  - Version 3.13 of the Linux kernel brought numerous policies that aim at putting a process near its memory, together with the handling of cases such as having [memory pages](https://en.wikipedia.org/wiki/Memory_page) shared between processes, or the use of transparent[huge pages](https://en.wikipedia.org/wiki/Huge_page) ; new[sysctl](https://en.wikipedia.org/wiki/Sysctl) settings allow NUMA balancing to be enabled or disabled, as well as the configuration of various NUMA memory balancing parameters.<sup>[\[17\]](#cite_note-17)</sup><sup>[\[18\]](#cite_note-18)</sup><sup>[\[19\]](#cite_note-19)</sup>
- Version 2.5 provided a basic NUMA support,
- [OpenSolaris](https://en.wikipedia.org/wiki/OpenSolaris) models NUMA architecture with lgroups.
- [FreeBSD](https://en.wikipedia.org/wiki/FreeBSD) added support for NUMA architecture in version 9.0.<sup>[\[20\]](#cite_note-20)</sup>
- [Silicon Graphics](https://en.wikipedia.org/wiki/Silicon_Graphics)[IRIX](https://en.wikipedia.org/wiki/IRIX) (discontinued as of 2013) support for ccNUMA architecture over 1240 CPU with Origin server series.

## Hardware support

[
[edit](/w/index.php?title=Non-uniform_memory_access&action=edit§ion=6)]

As of 2011,<sup>[\[update\]](https://en.wikipedia.org/w/index.php?title=Non-uniform_memory_access&action=edit)</sup> ccNUMA systems are multiprocessor systems based on the [AMD Opteron](https://en.wikipedia.org/wiki/AMD_Opteron) processor, which can be implemented without external logic, and the Intel [Itanium processor](https://en.wikipedia.org/wiki/Itanium_Processor_Family), which requires the chipset to support NUMA. Examples of ccNUMA-enabled chipsets are the SGI Shub (Super hub), the Intel E8870, the [HP](https://en.wikipedia.org/wiki/Hewlett-Packard) sx2000 (used in the Integrity and Superdome servers), and those found in NEC Itanium-based systems. Earlier ccNUMA systems such as those from [Silicon Graphics](https://en.wikipedia.org/wiki/Silicon_Graphics) were based on [MIPS](https://en.wikipedia.org/wiki/MIPS_architecture) processors and the [DEC](https://en.wikipedia.org/wiki/Digital_Equipment_Corporation) [Alpha 21364](https://en.wikipedia.org/wiki/Alpha_21364) (EV7) processor.

## See also

[
[edit](/w/index.php?title=Non-uniform_memory_access&action=edit§ion=7)]

- [Cache-only memory architecture](https://en.wikipedia.org/wiki/Cache-only_memory_architecture) (COMA)
- [CAS latency](https://en.wikipedia.org/wiki/CAS_latency) – Time delay between data read command and availability of data in a computer's RAM
- [HiperDispatch](https://en.wikipedia.org/wiki/HiperDispatch)
- [Nodal architecture](https://en.wikipedia.org/wiki/Nodal_architecture) – Computer series from British company ICL
- [Partitioned global address space](https://en.wikipedia.org/wiki/Partitioned_global_address_space) – Parallel programming model paradigm in computer science
- [Scratchpad memory](https://en.wikipedia.org/wiki/Scratchpad_memory) (SPM)
- [Uniform memory access](https://en.wikipedia.org/wiki/Uniform_memory_access) (UMA)

## References

[
[edit](/w/index.php?title=Non-uniform_memory_access&action=edit§ion=8)]

1. [↑](#cite_ref-1) This article is based on material taken from[Non-uniform+memory+access](https://foldoc.org/Non-uniform+memory+access) at the*[Free On-line Dictionary of Computing](https://en.wikipedia.org/wiki/Free_On-line_Dictionary_of_Computing)* prior to 1 November 2008 and incorporated under the "relicensing" terms of the[GFDL](https://en.wikipedia.org/wiki/GNU_Free_Documentation_License) , version 1.3 or later.
2. [1](#cite_ref-nyu-numa_2-0)[2](#cite_ref-nyu-numa_2-1) Manchanda, Nakul; Anand, Karan (2010-05-04).["Non-Uniform Memory Access (NUMA)"](https://web.archive.org/web/20131228092942/http://www.cs.nyu.edu/~lerner/spring10/projects/NUMA.pdf) (PDF). New York University. Archived from[the original](http://cs.nyu.edu/~lerner/spring10/projects/NUMA.pdf) (PDF) on 2013-12-28. Retrieved 2014-01-27.
3. [↑](#cite_ref-3) Sergey Blagodurov; Sergey Zhuravlev; Mohammad Dashti; Alexandra Fedorov (2011-05-02).["A Case for NUMA-aware Contention Management on Multicore Systems"](https://www.usenix.org/legacy/event/atc11/tech/final_files/Blagodurov.pdf) (PDF).[Simon Fraser University](https://en.wikipedia.org/wiki/Simon_Fraser_University) . Retrieved 2014-01-27.
4. [1](#cite_ref-acm-zmajo_4-0)[2](#cite_ref-acm-zmajo_4-1) Zoltan Majo; Thomas R. Gross (2011).["Memory System Performance in a NUMA Multicore Multiprocessor"](https://web.archive.org/web/20130612210800/http://people.inf.ethz.ch/zmajo/publications/11-systor.pdf) (PDF). ACM. Archived from[the original](http://people.inf.ethz.ch/zmajo/publications/11-systor.pdf) (PDF) on 2013-06-12. Retrieved 2014-01-27.
5. [↑](#cite_ref-5)["Intel Dual-Channel DDR Memory Architecture White Paper"](https://web.archive.org/web/20110929024052/http://www.kingston.com/newtech/MKF_520DDRwhitepaper.pdf) (PDF) (Rev. 1.0 ed.). Infineon Technologies North America and Kingston Technology. September 2003. Archived from[the original](http://www.kingston.com/newtech/MKF_520DDRwhitepaper.pdf) (PDF, 1021[KB](https://en.wikipedia.org/wiki/Kilobyte) ) on 2011-09-29. Retrieved 2007-09-06.
6. [↑](#cite_ref-6)["Intel QuickPath Architecture \[White paper\]"](http://www.intel.com/pressroom/archive/reference/whitepaper_QuickPath.pdf) (PDF).*Intel Corp* . 2008. Retrieved 2026-04-28.
7. [↑](#cite_ref-7)["Gelsinger Speaks To Intel And High-Tech Industry's Rapid Technology Cadence"](https://www.intel.com/pressroom/archive/releases/2007/20070918corp_b.htm) (Press release). Intel Corporation. September 18, 2007. Retrieved March 29, 2025.
8. [↑](#cite_ref-8)["ccNUMA: Cache Coherent Non-Uniform Memory Access"](https://www.slideshare.net/networksguy/ccnuma-cache-coherent-nonuniform-memory-access) . 2014.[Archived](https://web.archive.org/web/20140505112950/https://www.slideshare.net/networksguy/ccnuma-cache-coherent-nonuniform-memory-access) May 5, 2014, at the[Wayback Machine](https://en.wikipedia.org/wiki/Wayback_Machine)
9. [↑](#cite_ref-9) Per Stenstromt; Truman Joe; Anoop Gupta (2002).["Comparative Performance Evaluation of Cache-Coherent NUMA and COMA Architectures"](http://www.cs.berkeley.edu/~kubitron/cs258/handouts/papers/p80-stenstrom.pdf) (PDF). ACM. Retrieved 2014-01-27.
10. [↑](#cite_ref-10) Gustavson, David B. (September 1991).["The Scalable Coherent Interface and Related Standards Projects"](http://www.slac.stanford.edu/cgi-wrap/getdoc/slac-pub-5656.pdf) (PDF).*SLAC Publication 5656* .[Stanford Linear Accelerator Center](https://en.wikipedia.org/wiki/Stanford_Linear_Accelerator_Center) .[Archived](https://ghostarchive.org/archive/20221009/http://www.slac.stanford.edu/cgi-wrap/getdoc/slac-pub-5656.pdf) (PDF) from the original on 2022-10-09. Retrieved January 27, 2014.
11. [↑](#cite_ref-11)["The NumaChip enables cache coherent low cost shared memory"](https://web.archive.org/web/20140122115025/http://www.numascale.com/numa_technology.html) .*Numascale.com* . Archived from[the original](http://www.numascale.com/numa_technology.html) on 2014-01-22. Retrieved 2014-01-27.
12. [↑](#cite_ref-12) Karl-Bridge-Microsoft.["NUMA Support - Win32 apps"](http://msdn.microsoft.com/en-us/library/windows/desktop/aa363804%28v=vs.85%29.aspx) .*learn.microsoft.com* . Retrieved 2026-04-28.
13. [↑](#cite_ref-13)[Java HotSpot Virtual Machine Performance Enhancements](http://docs.oracle.com/javase/7/docs/technotes/guides/vm/performance-enhancements-7.html#numa)
14. [↑](#cite_ref-14)["Linux Scalability Effort: NUMA Group Homepage"](https://lse.sourceforge.net/numa/) .*SourceForge.net* . 2002-11-20. Retrieved 2014-02-06.
15. [↑](#cite_ref-15)["Linux kernel 3.8, Section 1.8. Automatic NUMA balancing"](http://kernelnewbies.org/Linux_3.8#head-c16d4288b51f0b50fbf615657e81b0db643fa7a0) .*kernelnewbies.org* . 2013-02-08. Retrieved 2014-02-06.
16. [↑](#cite_ref-16) Jonathan Corbet (2012-11-14).["NUMA in a hurry"](https://lwn.net/Articles/524977/) .*[LWN.net](https://en.wikipedia.org/wiki/LWN.net)* . Retrieved 2014-02-06.
17. [↑](#cite_ref-17)["Linux kernel 3.13, Section 1.6. Improved performance in NUMA systems"](http://kernelnewbies.org/Linux_3.13#head-d29c7db2e73bc464eb67ed8de953d0bfc9841636) .*kernelnewbies.org* . 2014-01-19. Retrieved 2014-02-06.
18. [↑](#cite_ref-18)["Linux kernel documentation: Documentation/sysctl/kernel.txt"](https://www.kernel.org/doc/Documentation/sysctl/kernel.txt) .*[kernel.org](https://en.wikipedia.org/wiki/Kernel.org)* . Retrieved 2014-02-06.
19. [↑](#cite_ref-19) Jonathan Corbet (2013-10-01).["NUMA scheduling progress"](https://lwn.net/Articles/568870/) .*[LWN.net](https://en.wikipedia.org/wiki/LWN.net)* . Retrieved 2014-02-06.
20. [↑](#cite_ref-20)["numa(4)"](<https://www.freebsd.org/cgi/man.cgi?numa(4)>) .*www.freebsd.org* . Retrieved 2020-12-03.

## External links

[
[edit](/w/index.php?title=Non-uniform_memory_access&action=edit§ion=9)]
