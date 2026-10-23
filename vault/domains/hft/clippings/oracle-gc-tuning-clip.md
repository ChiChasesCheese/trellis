---
title: HotSpot Virtual Machine Garbage Collection Tuning Guide
source: https://docs.oracle.com/en/java/javase/21/gctuning/introduction-garbage-collection-tuning.html
published: '2026-07-14'
site: Oracle Help Center
clipped: '2026-10-23'
---

# HotSpot Virtual Machine Garbage Collection Tuning Guide

## 1 Introduction to Garbage Collection Tuning

A wide variety of applications, from small applets on desktops to web services on large servers, use the Java Platform, Standard Edition (Java SE). In support of this diverse range of deployments, the Java HotSpot VM provides multiple garbage collectors, each designed to satisfy different requirements. Java SE selects the most appropriate garbage collector based on the class of the computer on which the application is run. However, this selection may not be optimal for every application. Users, developers, and administrators with strict performance goals or other requirements may need to explicitly select the garbage collector and tune certain parameters to achieve the desired level of performance. This document provides information to help with these tasks.

First, general features of a garbage collector and basic tuning options are described in the context of the serial, stop-the-world collector. Then specific features of the other collectors are presented along with factors to consider when selecting a collector.

### What Is a Garbage Collector?

The garbage collector (GC) automatically manages the application's dynamic memory allocation requests.

A garbage collector performs automatic dynamic memory management through the following operations:

- 
                        Allocates from and gives back memory to the operating system.
- 
                        Hands out that memory to the application as it requests it.
- 
                        Determines which parts of that memory is still in use by the application.
- 
                        Reclaims the unused memory for reuse by the application.

The Java HotSpot garbage collectors employ various techniques to improve the efficiency of these operations:

- 
                        Use generational scavenging in conjunction with aging to concentrate their efforts on areas in the heap that most likely contain a lot of reclaimable memory areas.
- 
                        Use multiple threads to aggressively make operations parallel, or perform some long-running operations in the background concurrent to the application.
- 
                        Try to recover larger contiguous free memory by compacting live objects.

### Why Does the Choice of Garbage Collector Matter?

The purpose of a garbage collector is to free the application developer from manual dynamic memory management. The developer is freed of the requirement to match allocations with deallocations and closely take care of the lifetimes of allocated dynamic memory. This completely eliminates some classes of errors related to memory management at the cost of some additional runtime overhead. The Java HotSpot VM provides a selection of garbage collection algorithms to choose from.

When does the choice of a garbage collector matter? For some applications, the answer is never. That is, the application can perform well in the presence of garbage collection with pauses of modest frequency and duration. However, this isn't the case for a large class of applications, particularly those with large amounts of data (multiple gigabytes), many threads, and high transaction rates.

Amdahl's law (parallel speedup in a given problem is limited by the sequential portion of the problem) implies that most workloads can't be perfectly parallelized; some portion is always sequential and doesn't benefit from parallelism. In the Java platform, there are currently four supported garbage collection alternatives and all but one of them, the serial GC, parallelize the work to improve performance. It's very important to keep the overhead of doing garbage collection as low as possible. This can be seen in the following example.

The graph in [Figure 1-1](introduction-garbage-collection-tuning.html#GUID-A48F272E-A6C1-45A0-9A8B-6D5790EB454C__PERCENTAGE_TIME_GC) models an ideal system that's perfectly scalable with the exception of garbage collection. The red line is an application spending only 1% of the time in garbage collection on a uniprocessor system. This translates to more than a 20% loss in throughput on systems with 32 processors. The magenta line shows that for an application at 10% of the time in garbage collection (not considered an outrageous amount of time in garbage collection in uniprocessor applications), more than 75% of throughput is lost when scaling up to 32 processors.
                  

Figure 1-1 Comparing Percentage of Time Spent in Garbage Collection

[Description of "Figure 1-1 Comparing Percentage of Time Spent in Garbage Collection"](img_text/jsgct-dt-005-gph-pc-vs-tp2.html)

This figure shows that negligible throughput issues when developing on small systems may become principal bottlenecks when scaling up to large systems. However, small improvements in reducing such a bottleneck can produce large gains in performance. For a sufficiently large system, it becomes worthwhile to select the right garbage collector and to tune it if necessary.

The serial collector is usually adequate for most small applications, in particular those requiring heaps of up to approximately 100 megabytes on modern processors. The other collectors have additional overhead or complexity, which is the price for specialized behavior. If the application does not need the specialized behavior of an alternate collector, use the serial collector. One situation where the serial collector isn't expected to be the best choice is a large, heavily threaded application that runs on a machine with a large amount of memory and two or more processors. When applications are run on such server-class machines, the Garbage-First (G1) collector is selected by default; see [Ergonomics](ergonomics1.html#GUID-DB4CAE94-2041-4A16-90EC-6AE3D91EC1F1).
                  

### Supported Operating Systems in Documentation

This document and its recommendations apply to all JDK 21 supported system configurations, limited by actual availability of some
                garbage collectors in a particular configuration. See [Oracle JDK Certified System Configurations](< https://www.oracle.com/pls/topic/lookup?ctx=javase18&id=latest_certified_system_configurations>).
