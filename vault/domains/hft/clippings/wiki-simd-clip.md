---
title: Single instruction, multiple data - Wikipedia
source: https://en.wikipedia.org/wiki/Single_instruction,_multiple_data
author: Authority control databases National United States Israel
published: '2002-06-07'
site: Wikimedia Foundation, Inc.
clipped: '2026-10-23'
---

# Single instruction, multiple data - Wikipedia

# Single instruction, multiple data

| [Flynn's taxonomy](https://en.wikipedia.org/wiki/Flynn's_taxonomy) | 
|---|
| Single data stream | 
| Multiple data streams | 
| SIMD subcategories <sup>[\[1\]](#cite_note-flynn-1972-1)</sup> | 
| See also | 

**Single instruction, multiple data** (**SIMD**) is a type of [parallel computing](https://en.wikipedia.org/wiki/Parallel_computing) (processing) in [Flynn's taxonomy](https://en.wikipedia.org/wiki/Flynn's_taxonomy). SIMD describes computers with [multiple processing elements](https://en.wikipedia.org/wiki/Multiple_processing_elements) that perform the same operation on multiple data points simultaneously. SIMD can be internal (part of the hardware design) and it can be directly accessible through an [instruction set architecture](https://en.wikipedia.org/wiki/Instruction_set_architecture) (ISA), but it should not be confused with an ISA.

Such machines exploit [data level parallelism](https://en.wikipedia.org/wiki/Data_parallelism), but not [concurrency](https://en.wikipedia.org/wiki/Concurrent_computing): there are simultaneous (parallel) computations, but each unit performs exactly the same instruction at any given moment (just with different data). A simple example is to add many pairs of numbers together, all of the SIMD units are performing an addition, but each one has different pairs of values to add. SIMD is especially applicable to common tasks such as adjusting the contrast in a [digital image](https://en.wikipedia.org/wiki/Digital_image) or adjusting the volume of [digital audio](https://en.wikipedia.org/wiki/Digital_audio). Most modern [central processing unit](https://en.wikipedia.org/wiki/Central_processing_unit) (CPU) designs include SIMD instructions to improve the performance of [multimedia](https://en.wikipedia.org/wiki/Multimedia) use. In recent CPUs, SIMD units are tightly coupled with cache hierarchies and prefetch mechanisms, which minimize latency during large block operations. For instance, AVX-512-enabled processors can prefetch entire cache lines and apply fused multiply-add operations (FMA) in a single SIMD cycle.

## Confusion between SIMT and SIMD

[
[edit](/w/index.php?title=Single_instruction,_multiple_data&action=edit§ion=1)]

SIMD has three different subcategories in [Flynn's 1972 Taxonomy](<https://en.wikipedia.org/wiki/Flynn's_taxonomy#Single_instruction_stream,_multiple_data_streams_(SIMD)>), one of which is [single instruction, multiple threads](https://en.wikipedia.org/wiki/Single_instruction,_multiple_threads) (SIMT). SIMT should not be confused with [software threads](<https://en.wikipedia.org/wiki/Thread_(computing)>) or [hardware threads](<https://en.wikipedia.org/wiki/Multithreading_(computer_architecture)>), both of which are task time-sharing (time-slicing). SIMT is true simultaneous parallel hardware-level execution, such as in the [ILLIAC IV](https://en.wikipedia.org/wiki/ILLIAC_IV).

SIMD should not be confused with [Vector processing](https://en.wikipedia.org/wiki/Vector_processing), characterized by the [Cray 1](https://en.wikipedia.org/wiki/Cray_1) and  clarified in [Duncan's taxonomy](https://en.wikipedia.org/wiki/Duncan's_taxonomy). The [difference between SIMD and vector processors](https://en.wikipedia.org/wiki/Vector_processor#Difference_between_SIMD_and_vector_processors) is primarily the presence of a Cray-style `SET VECTOR LENGTH` instruction.

## History

[
[edit](/w/index.php?title=Single_instruction,_multiple_data&action=edit§ion=2)]

The first known operational use to date of [SIMD within a register](https://en.wikipedia.org/wiki/SIMD_within_a_register) was the [TX-2](https://en.wikipedia.org/wiki/TX-2), in 1958. It was capable of 36-bit operations and two 18-bit or four 9-bit sub-word operations.

The first commercial use of SIMD instructions was in the [ILLIAC IV](https://en.wikipedia.org/wiki/ILLIAC_IV), which was completed in 1972.

[Vector supercomputers](https://en.wikipedia.org/wiki/Vector_processor) of the early 1970s such as the [CDC Star-100](https://en.wikipedia.org/wiki/CDC_STAR-100) and the [Texas Instruments ASC](https://en.wikipedia.org/wiki/TI_Advanced_Scientific_Computer) could operate on a "vector" of data with a single instruction. Vector processing was especially popularized by [Cray](https://en.wikipedia.org/wiki/Cray) in the 1970s and 1980s. Vector processing architectures are now considered separate from SIMD computers: [Duncan's Taxonomy](https://en.wikipedia.org/wiki/Duncan's_Taxonomy) includes them whereas [Flynn's Taxonomy](https://en.wikipedia.org/wiki/Flynn's_Taxonomy) does not, due to Flynn's work (1966, 1972) pre-dating the [Cray-1](https://en.wikipedia.org/wiki/Cray-1) (1977). The complexity of Vector processors however inspired a simpler arrangement known as [SIMD within a register](https://en.wikipedia.org/wiki/SIMD_within_a_register).

The first era of modern SIMD computers was characterized by [massively parallel processing](https://en.wikipedia.org/wiki/Massively_parallel_processing)-style [supercomputers](https://en.wikipedia.org/wiki/Supercomputer) such as the [Thinking Machines](https://en.wikipedia.org/wiki/Thinking_Machines_Corporation) [Connection Machine](https://en.wikipedia.org/wiki/Connection_Machine) CM-1 and CM-2. These computers had many limited-functionality processors that would work in parallel. For example, each of 65,536 single-bit processors in a Thinking Machines CM-2 would execute the same instruction at the same time, allowing, for instance, to logically combine 65,536 pairs of bits at a time, using a hypercube-connected network or processor-dedicated RAM to find its operands. Supercomputing moved away from the SIMD approach when inexpensive scalar [multiple instruction, multiple data](https://en.wikipedia.org/wiki/Multiple_instruction,_multiple_data) (MIMD) approaches based on commodity processors such as the [Intel i860 XP](https://en.wikipedia.org/wiki/Intel_i860) became more powerful, and interest in SIMD waned.[\[3\]](#cite_note-3)

The current era of SIMD processors grew out of the desktop-computer market rather than the supercomputer market. As desktop processors became powerful enough to support real-time gaming and audio/video processing during the 1990s, demand grew for this type of computing power, and microprocessor vendors turned to SIMD to meet the demand.<sup>[\[4\]](#cite_note-conte-4)</sup> This resurgence also coincided with the rise of [DirectX](https://en.wikipedia.org/wiki/DirectX) and OpenGL shader models, which heavily leveraged SIMD under the hood. The graphics APIs encouraged programmers to adopt data-parallel programming styles, indirectly accelerating SIMD adoption in desktop software. Hewlett-Packard introduced [Multimedia Acceleration eXtensions](https://en.wikipedia.org/wiki/Multimedia_Acceleration_eXtensions) (MAX) instructions into [PA-RISC](https://en.wikipedia.org/wiki/PA-RISC) 1.1 desktops in 1994 to accelerate MPEG decoding.<sup>[\[5\]](#cite_note-5)</sup> Sun Microsystems introduced SIMD integer instructions in its "[VIS](https://en.wikipedia.org/wiki/Visual_Instruction_Set)" instruction set extensions in 1995, in its [UltraSPARC I](https://en.wikipedia.org/wiki/UltraSPARC) microprocessor. MIPS followed suit with their similar [MDMX](https://en.wikipedia.org/wiki/MDMX) system.

The first widely deployed desktop SIMD was with Intel's [MMX](<https://en.wikipedia.org/wiki/MMX_(instruction_set)>) extensions to the [x86](https://en.wikipedia.org/wiki/X86) architecture in 1996. This sparked the introduction of the much more powerful [AltiVec](https://en.wikipedia.org/wiki/AltiVec) system in the [Motorola](https://en.wikipedia.org/wiki/Motorola) [PowerPC](https://en.wikipedia.org/wiki/PowerPC) and IBM's [POWER](https://en.wikipedia.org/wiki/IBM_Power_microprocessors) systems. Intel responded in 1999 by introducing the all-new [SSE](https://en.wikipedia.org/wiki/Streaming_SIMD_Extensions) system. Since then, there have been several extensions to the SIMD instruction sets for both architectures. Advanced vector extensions AVX, [AVX2](https://en.wikipedia.org/wiki/AVX2) and [AVX-512](https://en.wikipedia.org/wiki/AVX-512) are developed by Intel. AMD supports AVX, [AVX2](https://en.wikipedia.org/wiki/AVX2), and [AVX-512](https://en.wikipedia.org/wiki/AVX-512) in their current products.[\[6\]](#cite_note-6)

## Disadvantages

[
[edit](/w/index.php?title=Single_instruction,_multiple_data&action=edit§ion=3)]

With SIMD, an order of magnitude increase in code size is not uncommon, when compared to equivalent scalar or equivalent vector code, and an order of magnitude *or greater* effectiveness (work done per instruction) is achievable with Vector ISAs.[\[7\]](#cite_note-7)

ARM's [Scalable Vector Extension](https://en.wikipedia.org/wiki/Scalable_Vector_Extension) takes another approach, known in [Flynn's Taxonomy](<https://en.wikipedia.org/wiki/Flynn's_taxonomy#Single_instruction_stream,_multiple_data_streams_(SIMD)>) more commonly known today as ["Predicated" (masked)](<https://en.wikipedia.org/wiki/Predication_(computer_architecture)#SIMD,_SIMT_and_vector_predication>) SIMD. This approach is not as compact as [vector processing](https://en.wikipedia.org/wiki/Vector_processing) but is still far better than non-predicated SIMD. Detailed comparative examples are given at [Vector processor § Vector instruction example](https://en.wikipedia.org/wiki/Vector_processor#Vector_instruction_example).

## Chronology

[
[edit](/w/index.php?title=Single_instruction,_multiple_data&action=edit§ion=4)]

| SIMD supercomputer examples excluding  vector processors |  | 
|---|---|
| Year | Example | 
|---|---|
| 1974 | [ILLIAC IV](https://en.wikipedia.org/wiki/ILLIAC_IV) - an Array Processor comprising scalar 64-bit PEs | 
| 1974 | [ICL Distributed Array Processor](https://en.wikipedia.org/wiki/ICL_Distributed_Array_Processor) (DAP) | 
| 1976 | [Burroughs Scientific Processor](https://en.wikipedia.org/wiki/Burroughs_Scientific_Processor) | 
| 1981 | [Geometric-Arithmetic Parallel Processor](https://en.wikipedia.org/wiki/Geometric-Arithmetic_Parallel_Processor) from[Martin Marietta](https://en.wikipedia.org/wiki/Martin_Marietta) (continued at[Lockheed Martin](https://en.wikipedia.org/wiki/Lockheed_Martin) , then at[Teranex](http://www.teranex.com) and[Silicon Optix](https://en.wikipedia.org/wiki/Silicon_Optix) ) | 
| 1983–1991 | [Massively Parallel Processor](https://en.wikipedia.org/wiki/Goodyear_MPP) (MPP), from[NASA](https://en.wikipedia.org/wiki/NASA) /[Goddard Space Flight Center](https://en.wikipedia.org/wiki/Goddard_Space_Flight_Center) | 
| 1985 | [Connection Machine](https://en.wikipedia.org/wiki/Connection_Machine) , models 1 and 2 (CM-1 and CM-2), from[Thinking Machines Corporation](https://en.wikipedia.org/wiki/Thinking_Machines_Corporation) | 
| 1987–1996 | [MasPar](https://en.wikipedia.org/wiki/MasPar) MP-1 and MP-2 | 
| 1991 | Zephyr DC from Wavetracer | 
| 2001 | Xplor from Pyxsys, Inc. | 

[vector processors](https://en.wikipedia.org/wiki/Vector_processor)

## Hardware

[
[edit](/w/index.php?title=Single_instruction,_multiple_data&action=edit§ion=5)]

### CPUs

[
[edit](/w/index.php?title=Single_instruction,_multiple_data&action=edit§ion=6)]

Small-scale (64 or 128 bits) SIMD became popular on general-purpose CPUs in the early 1990s and continued through 1997 and later with Motion Video Instructions (MVI) for [Alpha](https://en.wikipedia.org/wiki/DEC_Alpha). SIMD instructions can be found, to one degree or another, on most CPUs, including [Hewlett-Packard](https://en.wikipedia.org/wiki/Hewlett-Packard)'s (HP) [PA-RISC](https://en.wikipedia.org/wiki/PA-RISC) [Multimedia Acceleration eXtensions](https://en.wikipedia.org/wiki/Multimedia_Acceleration_eXtensions) (MAX), [IBM](https://en.wikipedia.org/wiki/IBM)'s [AltiVec](https://en.wikipedia.org/wiki/AltiVec) and Signal Processing Engine (SPE) for [PowerPC](https://en.wikipedia.org/wiki/PowerPC), [Intel](https://en.wikipedia.org/wiki/Intel)'s [MMX and iwMMXt](<https://en.wikipedia.org/wiki/MMX_(instruction_set)>), [Streaming SIMD Extensions](https://en.wikipedia.org/wiki/Streaming_SIMD_Extensions) (SSE), [SSE2](https://en.wikipedia.org/wiki/SSE2), [SSE3](https://en.wikipedia.org/wiki/SSE3) [SSSE3](https://en.wikipedia.org/wiki/SSSE3) and [SSE4](https://en.wikipedia.org/wiki/SSE4).x, [AMD](https://en.wikipedia.org/wiki/Advanced_Micro_Devices)'s [3DNow!](https://en.wikipedia.org/wiki/3DNow!), [ARC's](<https://en.wikipedia.org/wiki/ARC_(processor)>) ARC Video subsystem, [SPARC](https://en.wikipedia.org/wiki/SPARC)'s [VIS](https://en.wikipedia.org/wiki/Visual_Instruction_Set) and VIS2, [Sun](https://en.wikipedia.org/wiki/Sun_Microsystems)'s [MAJC](https://en.wikipedia.org/wiki/MAJC), [ARM's](https://en.wikipedia.org/wiki/ARM_Holdings) [Neon](<https://en.wikipedia.org/wiki/ARM_architecture#Advanced_SIMD_(Neon)>) technology, [MIPS](https://en.wikipedia.org/wiki/MIPS_architecture)' [MDMX](https://en.wikipedia.org/wiki/MDMX) (MaDMaX) and [MIPS-3D](https://en.wikipedia.org/wiki/MIPS-3D).

Intel's [AVX-512](https://en.wikipedia.org/wiki/AVX-512) SIMD instructions process 512 bits of data at once.

### Coprocessors

[
[edit](/w/index.php?title=Single_instruction,_multiple_data&action=edit§ion=7)]

The IBM, Sony, Toshiba co-developed [Cell processor's](<https://en.wikipedia.org/wiki/Cell_(processor)>) [Synergistic Processing Element's](<https://en.wikipedia.org/wiki/Cell_(processor)#Synergistic_Processing_Element_(SPE)>) (SPE's) instruction set is heavily SIMD based.

Some, but not all, GPUs are SIMD-based. AMD GPUs since the [TeraScale (microarchitecture)](<https://en.wikipedia.org/wiki/TeraScale_(microarchitecture)>) are SIMD-based, a feature that has remained in the 2020s microartectures RDNA and CDNA,<sup>[\[8\]](#cite_note-8)</sup> with a layer of [single instruction, multiple threads](https://en.wikipedia.org/wiki/Single_instruction,_multiple_threads) (SIMT) above.<sup>[\[9\]](#cite_note-9)</sup> On the other hand, Nvidia's CUDA architectures use scalar cores with SIMT.[\[10\]](#cite_note-10)

[Philips](https://en.wikipedia.org/wiki/Philips), now [NXP](https://en.wikipedia.org/wiki/NXP_Semiconductors), developed several SIMD processors named [Xetal](https://en.wikipedia.org/wiki/Xetal). The Xetal has 320 16-bit processor elements especially designed for vision tasks.

Apple's M1 and M2 chips also incorporate SIMD units deeply integrated with their GPU and Neural Engine, using Apple-designed SIMD pipelines optimized for image filtering, convolution, and matrix multiplication. This unified memory architecture helps SIMD instructions operate on shared memory pools more efficiently. (The CPU part implements ordinary NEON).

## Software

[
[edit](/w/index.php?title=Single_instruction,_multiple_data&action=edit§ion=8)]

SIMD instructions are widely used to process 3D graphics, although modern [graphics cards](https://en.wikipedia.org/wiki/Video_card) with embedded SIMD have largely taken over this task from the CPU. Some systems also include permute functions that re-pack elements inside vectors, making them especially useful for data processing and compression. They are also used in cryptography.[\[11\]](#cite_note-11)[\[12\]](#cite_note-12)<sup>[\[13\]](#cite_note-13)</sup> The trend of general-purpose computing on GPUs ([GPGPU](https://en.wikipedia.org/wiki/GPGPU)) may lead to wider use of SIMD in the future. Recent compilers such as [LLVM](https://en.wikipedia.org/wiki/LLVM), [GNU Compiler Collection](https://en.wikipedia.org/wiki/GNU_Compiler_Collection) (GCC), and Intel's ICC offer aggressive auto-vectoring options. Developers can often enable these with flags like `-O3` or `-ftree-vectorize`, which guide the compiler to restructure loops for SIMD compatibility.

Adoption of SIMD systems in [personal computer](https://en.wikipedia.org/wiki/Personal_computer) software was at first slow, due to a number of problems. One was that many of the early SIMD instruction sets tended to slow overall performance of the system due to the re-use of existing floating point registers. Other systems, like [MMX](<https://en.wikipedia.org/wiki/MMX_(instruction_set)>) and [3DNow!](https://en.wikipedia.org/wiki/3DNow!), offered support for data types that were not interesting to a wide audience and had expensive context switching instructions to switch between using the [FPU](https://en.wikipedia.org/wiki/Floating-point_unit) and MMX [registers](https://en.wikipedia.org/wiki/Processor_register). Compilers also often lacked support, requiring programmers to resort to [assembly language](https://en.wikipedia.org/wiki/Assembly_language) coding.

SIMD on [x86](https://en.wikipedia.org/wiki/X86) had a slow start. The introduction of [3DNow!](https://en.wikipedia.org/wiki/3DNow!) by [AMD](https://en.wikipedia.org/wiki/Advanced_Micro_Devices) and [SSE](https://en.wikipedia.org/wiki/Streaming_SIMD_Extensions) by [Intel](https://en.wikipedia.org/wiki/Intel) confused matters somewhat, but today the system seems to have settled down (after AMD adopted SSE) and newer compilers should result in more SIMD-enabled software. Intel and AMD now both provide optimized math [libraries](<https://en.wikipedia.org/wiki/Library_(computing)>) that use SIMD instructions, and open source alternatives like libSIMD, SIMDx86 and SLEEF have started to appear (see also [libm](https://en.wikipedia.org/wiki/Libm)).[\[14\]](#cite_note-14)

[Apple Computer](https://en.wikipedia.org/wiki/Apple_Inc.) had somewhat more success, even though they entered the SIMD market later than the rest. [AltiVec](https://en.wikipedia.org/wiki/AltiVec) offered a rich system and can be programmed using increasingly sophisticated compilers from [Motorola](https://en.wikipedia.org/wiki/Motorola), [IBM](https://en.wikipedia.org/wiki/IBM) and [GNU](https://en.wikipedia.org/wiki/GNU), therefore assembly language programming is rarely needed. Additionally, many of the systems that would benefit from SIMD were supplied by Apple itself, for example [iTunes](https://en.wikipedia.org/wiki/ITunes) and [QuickTime](https://en.wikipedia.org/wiki/QuickTime). However, in 2006, Apple computers moved to Intel x86 processors. Apple's [APIs](https://en.wikipedia.org/wiki/Application_programming_interface) and [development tools](https://en.wikipedia.org/wiki/Integrated_development_environment) ([XCode](https://en.wikipedia.org/wiki/Xcode)) were modified to support [SSE2](https://en.wikipedia.org/wiki/SSE2) and [SSE3](https://en.wikipedia.org/wiki/SSE3) as well as AltiVec. Apple was the dominant purchaser of PowerPC chips from IBM and [Freescale Semiconductor](https://en.wikipedia.org/wiki/Freescale_Semiconductor). Even though Apple has stopped using PowerPC processors in their products, further development of AltiVec is continued in several PowerPC and [Power ISA](https://en.wikipedia.org/wiki/Power_ISA) designs from Freescale and IBM.

*SIMD within a register*, or [SWAR](https://en.wikipedia.org/wiki/SWAR), is a range of techniques and tricks used for performing SIMD in general-purpose registers on hardware that does not provide any direct support for SIMD instructions. This can be used to exploit parallelism in certain algorithms even on hardware that does not support SIMD directly.

### Programmer interface

[
[edit](/w/index.php?title=Single_instruction,_multiple_data&action=edit§ion=9)]

It is common for publishers of the SIMD instruction sets to make their own [C](<https://en.wikipedia.org/wiki/C_(programming_language)>) and [C++](https://en.wikipedia.org/wiki/C++) language extensions with [intrinsic functions](https://en.wikipedia.org/wiki/Intrinsic_function) or special datatypes (with [operator overloading](https://en.wikipedia.org/wiki/Operator_overloading)) guaranteeing the generation of vector code. Intel, AltiVec, and ARM NEON provide extensions widely adopted by the compilers targeting their CPUs. (More complex operations are the task of vector math libraries.)

#### Generic datatypes

[
[edit](/w/index.php?title=Single_instruction,_multiple_data&action=edit§ion=10)]

The [GNU C Compiler](https://en.wikipedia.org/wiki/GNU_C_Compiler) takes the extensions a step further by abstracting them into a universal interface that can be used on any platform by providing a way of defining SIMD datatypes.<sup>[\[15\]](#cite_note-15)</sup> The [LLVM](https://en.wikipedia.org/wiki/LLVM) Clang compiler also implements the feature, with an analogous interface defined in the IR.[\[16\]](#cite_note-16)[Rust](<https://en.wikipedia.org/wiki/Rust_(programming_language)>)'s `std::simd` uses this interface, and so does [Swift](<https://en.wikipedia.org/wiki/Swift_(programming_language)>) 2.0+.

C++ added `std::simd::vec<T, Abi>` (a data-parallel vector type) and `std::simd::mask<T, Abi>` (a data-parallel type with `bool` elements) in [C++26](https://en.wikipedia.org/wiki/C++26)<sup>[\[17\]](#cite_note-17)</sup>, where the [template parameters](https://en.wikipedia.org/wiki/Type_variable) `T` is the vectorizable type and `Abi` is the ABI tag, specifying its width and storage.

[Microsoft](https://en.wikipedia.org/wiki/Microsoft_Corporation) added SIMD to [.NET](https://en.wikipedia.org/wiki/.NET_Core) in RyuJIT.<sup>[\[18\]](#cite_note-18)</sup> The `System.Numerics.Vector<T>` class implements SIMD datatypes.<sup>[\[19\]](#cite_note-19)</sup> Java also has a new proposed API for SIMD instructions available in [OpenJDK](https://en.wikipedia.org/wiki/OpenJDK) 17 in an incubator [module](https://en.wikipedia.org/wiki/Java_Platform_Module_System), in the [standard library](https://en.wikipedia.org/wiki/Java_Class_Library) as `jdk.incubator.vector.Vector<E>`.<sup>[\[20\]](#cite_note-20)</sup> It also has a safe fallback mechanism on unsupported CPUs to simple loops.

Rust has an experimental `std::simd::Simd<T, N>` (a SIMD vector) and `std::simd::Mask<T, N>` (a SIMD vector mask) types, where `T` is the vectorizable type and `N` is the size, for portable SIMD<sup>[\[21\]](#cite_note-21)</sup>; it also has a target-specific `std::arch` module, but this API is unsafe.[\[22\]](#cite_note-22)

#### Vectorization hints

[
[edit](/w/index.php?title=Single_instruction,_multiple_data&action=edit§ion=11)]

Instead of providing an SIMD datatype, compilers can also be hinted to [auto-vectorize](https://en.wikipedia.org/wiki/Automatic_vectorization) some loops, potentially taking some assertions about the lack of data dependency. This is not as flexible as manipulating SIMD variables directly, but is easier to use. [OpenMP](https://en.wikipedia.org/wiki/OpenMP) 4.0+ has a `#pragma omp simd` hint.<sup>[\[23\]](#cite_note-23)</sup> This OpenMP interface has replaced a wide set of nonstandard extensions, including [Cilk](https://en.wikipedia.org/wiki/Cilk)'s `#pragma simd`,<sup>[\[24\]](#cite_note-24)</sup> GCC's `#pragma GCC ivdep`, and many more.[\[25\]](#cite_note-25)

"SIMD everywhere", a collection of C/C++ headers implementing platform-specific intrinsics for other platforms (e.g. SSE intrinsics for ARM NEON), includes the use of platform-specific intrinsics, generic vector interfaces, and vectorization hints. It can be used as a "Rosetta Stone" for comparing these different SIMD programming paradigms.[\[26\]](#cite_note-26)

#### SPMD-on-SIMD

[
[edit](/w/index.php?title=Single_instruction,_multiple_data&action=edit§ion=12)]

Another approach is [SPMD](https://en.wikipedia.org/wiki/Single_program,_multiple_data): write a program that looks as if it operates only one element on the time, then have a compiler widen it to match the SIMD vector width. This is the approach used by graphics [shaders](https://en.wikipedia.org/wiki/Shader) and more recently adopted by CPU-oriented tools such as Intel IPSC.[\[27\]](#cite_note-27)

### SIMD multi-versioning

[
[edit](/w/index.php?title=Single_instruction,_multiple_data&action=edit§ion=13)]

Consumer software is typically expected to work on a range of CPUs covering multiple generations, which could limit the programmer's ability to use new SIMD instructions to improve the computational performance of a program. The solution is to include multiple versions of the same code that uses either older or newer SIMD technologies, and pick one that best fits the user's CPU at run-time ([dynamic dispatch](https://en.wikipedia.org/wiki/Dynamic_dispatch)). There are two main camps of solutions:

- Function multi-versioning (FMV): a [subroutine](https://en.wikipedia.org/wiki/Subroutine) in the program or a library is duplicated and compiled for many instruction set extensions, and the program decides which one to use at run-time.
- Library multi-versioning (LMV): the entire [programming library](<https://en.wikipedia.org/wiki/Library_(computing)>) is duplicated for many instruction set extensions, and the operating system or the program decides which one to load at run-time.

FMV, manually coded in assembly language, is quite commonly used in a number of performance-critical libraries such as glibc and libjpeg-turbo. [Intel C++ Compiler](https://en.wikipedia.org/wiki/Intel_C++_Compiler), [GNU Compiler Collection](https://en.wikipedia.org/wiki/GNU_Compiler_Collection) since GCC 6, and [Clang](https://en.wikipedia.org/wiki/Clang) since clang 7 allow for a simplified approach, with the compiler taking care of function duplication and selection. GCC and clang requires explicit `target_clones` labels in the code to "clone" functions,<sup>[\[28\]](#cite_note-28)</sup> while ICC does so automatically (under the command-line option `/Qax`). Rust also supports FMV. The setup is similar to GCC and Clang in that the code defines what instruction sets to compile for, but cloning is manually done via inlining.[\[29\]](#cite_note-29)

As using FMV requires code modification on GCC and Clang, vendors more commonly use library multi-versioning: this is easier to achieve as only compiler switches need to be changed. [Glibc](https://en.wikipedia.org/wiki/Glibc) supports LMV and this functionality is adopted by the Intel-backed Clear Linux project.[\[30\]](#cite_note-clear-30)

### SIMD on the web

[
[edit](/w/index.php?title=Single_instruction,_multiple_data&action=edit§ion=14)]

In 2013 John McCutchan announced that he had created a high-performance interface to SIMD instruction sets for the [Dart](<https://en.wikipedia.org/wiki/Dart_(programming_language)>) programming language, bringing the benefits of SIMD to web programs for the first time. The interface consists of two types:[\[31\]](#cite_note-31)

- Float32x4, 4 single precision floating point values.
- Int32x4, 4 32-bit integer values.

Instances of these types are immutable and in optimized code are mapped directly to SIMD registers. Operations expressed in Dart typically are compiled into a single instruction without any overhead. This is similar to C and C++ intrinsics. Benchmarks for [4×4](https://en.wikipedia.org/wiki/4×4_matrix) [matrix multiplication](https://en.wikipedia.org/wiki/Matrix_multiplication), [3D vertex transformation](https://en.wikipedia.org/wiki/3D_vertex_transformation), and [Mandelbrot set](https://en.wikipedia.org/wiki/Mandelbrot_set) visualization show near 400% speedup compared to scalar code written in Dart.

Intel announced at IDF 2013 that they were implementing McCutchan's specification for both [V8](<https://en.wikipedia.org/wiki/V8_(JavaScript_engine)>) and [SpiderMonkey](https://en.wikipedia.org/wiki/SpiderMonkey).<sup>[\[32\]](#cite_note-32)</sup> However, by 2017, SIMD.js was taken out of the [ECMAScript](https://en.wikipedia.org/wiki/ECMAScript) standard queue in favor of pursuing a similar interface in [WebAssembly](https://en.wikipedia.org/wiki/WebAssembly).[\[33\]](#cite_note-33)

Support for SIMD was added to the [WebAssembly](https://en.wikipedia.org/wiki/WebAssembly) 2.0 specification, which was finished on 2022 and became official in December 2024.<sup>[\[34\]](#cite_note-34)</sup> LLVM's autovectoring, when compiling C or C++ to WebAssembly, can target WebAssembly SIMD to automatically make use of SIMD, while SIMD intrinsic are also available.[\[35\]](#cite_note-35)

## Commercial applications

[
[edit](/w/index.php?title=Single_instruction,_multiple_data&action=edit§ion=15)]

It has generally proven difficult to find sustainable commercial applications for SIMD-only processors in general-purpose computing.

One that has had some measure of success is the [GAPP](https://en.wikipedia.org/wiki/Geometric-Arithmetic_Parallel_Processor), which was developed by [Lockheed Martin](https://en.wikipedia.org/wiki/Lockheed_Martin) and taken to the commercial sector by their spin-off Teranex. The GAPP's recent incarnations have become a powerful tool in real-time [video processing](https://en.wikipedia.org/wiki/Digital_image_processing) applications like conversion between various video standards and frame rates ([NTSC](https://en.wikipedia.org/wiki/NTSC) to/from [PAL](https://en.wikipedia.org/wiki/PAL), NTSC to/from [high-definition television](https://en.wikipedia.org/wiki/High-definition_television) (HDTV) formats, etc.), [deinterlacing](https://en.wikipedia.org/wiki/Deinterlacing), image [noise reduction](https://en.wikipedia.org/wiki/Noise_reduction), adaptive [video compression](https://en.wikipedia.org/wiki/Video_compression), and image enhancement.

A more ubiquitous application for SIMD is found in [video games](https://en.wikipedia.org/wiki/Video_game): nearly every modern [video game console](https://en.wikipedia.org/wiki/Video_game_console) since [1998](<https://en.wikipedia.org/wiki/History_of_video_game_consoles_(sixth_generation)>) has incorporated a SIMD processor somewhere in its architecture. The [PlayStation 2](https://en.wikipedia.org/wiki/PlayStation_2) was unusual in that one of its vector-float units could function as an autonomous [digital signal processor](https://en.wikipedia.org/wiki/Digital_signal_processor) (DSP) executing its own instruction stream, or as a coprocessor driven by ordinary CPU instructions. 3D graphics applications tend to lend themselves well to SIMD processing as they rely heavily on operations with 4-dimensional vectors. [Microsoft](https://en.wikipedia.org/wiki/Microsoft)'s [Direct3D](https://en.wikipedia.org/wiki/Direct3D) 9.0 now chooses at runtime processor-specific implementations of its own math operations, including the use of SIMD-capable instructions.

A later processor that used vector processing is the [Cell processor](<https://en.wikipedia.org/wiki/Cell_(processor)>) used in the PlayStation 3, which was developed by [IBM](https://en.wikipedia.org/wiki/IBM) in cooperation with [Toshiba](https://en.wikipedia.org/wiki/Toshiba) and [Sony](https://en.wikipedia.org/wiki/Sony). It uses a number of SIMD processors (a [non-uniform memory access](https://en.wikipedia.org/wiki/Non-uniform_memory_access) (NUMA) architecture, each with independent [local store](https://en.wikipedia.org/wiki/Cache_memory) and controlled by a general purpose CPU) and is geared towards the huge datasets required by 3D and video processing applications. It differs from traditional ISAs by being SIMD from the ground up with no separate scalar registers.

Ziilabs produced an SIMD type processor for use on mobile devices, such as media players and mobile phones.[\[36\]](#cite_note-36)

Larger scale commercial SIMD processors are available from ClearSpeed Technology, Ltd. and Stream Processors, Inc. [ClearSpeed](https://en.wikipedia.org/wiki/ClearSpeed)'s CSX600 (2004) has 96 cores each with two double-precision floating point units while the CSX700 (2008) has 192. Stream Processors is headed by computer architect [Bill Dally](https://en.wikipedia.org/wiki/Bill_Dally). Their Storm-1 processor (2007) contains 80 SIMD cores controlled by a [MIPS](https://en.wikipedia.org/wiki/MIPS_architecture) CPU.

## See also

[
[edit](/w/index.php?title=Single_instruction,_multiple_data&action=edit§ion=16)]

- [Streaming SIMD Extensions](https://en.wikipedia.org/wiki/Streaming_SIMD_Extensions) ,[MMX](<https://en.wikipedia.org/wiki/MMX_(instruction_set)>) ,[SSE2](https://en.wikipedia.org/wiki/SSE2) ,[SSE3](https://en.wikipedia.org/wiki/SSE3) ,[Advanced Vector Extensions](https://en.wikipedia.org/wiki/Advanced_Vector_Extensions) ,[AVX-512](https://en.wikipedia.org/wiki/AVX-512)
- [Instruction set architecture](https://en.wikipedia.org/wiki/Instruction_set_architecture)
- [Flynn's taxonomy](https://en.wikipedia.org/wiki/Flynn's_taxonomy)
- SIMD within a register ([SWAR](https://en.wikipedia.org/wiki/SWAR) )
- [Single program, multiple data](https://en.wikipedia.org/wiki/Single_program,_multiple_data) (SPMD)
- [OpenCL](https://en.wikipedia.org/wiki/OpenCL)

## References

[
[edit](/w/index.php?title=Single_instruction,_multiple_data&action=edit§ion=17)]

1. [↑](#cite_ref-flynn-1972_1-0)[Flynn, Michael J.](https://en.wikipedia.org/wiki/Michael_J._Flynn) (September 1972).["Some Computer Organizations and Their Effectiveness"](https://www.cs.utah.edu/~hari/teaching/paralg/Flynn72.pdf) (PDF).*[IEEE Transactions on Computers](https://en.wikipedia.org/wiki/IEEE_Transactions_on_Computers)* .**C-21** (9): 948–960.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1109/TC.1972.5009071](https://doi.org/10.1109%2FTC.1972.5009071) .
2. [↑](#cite_ref-2)["Archived copy"](https://web.archive.org/web/20240427173522/https://apps.dtic.mil/sti/tr/pdf/ADA954882.pdf) (PDF). Archived from[the original](https://apps.dtic.mil/sti/tr/pdf/ADA954882.pdf) (PDF) on 2024-04-27.`{{`[cite web](https://en.wikipedia.org/wiki/Template:Cite_web) }}
:  CS1 maint: archived copy as title ([link](https://en.wikipedia.org/wiki/Category:CS1_maint:_archived_copy_as_title) )
3. [↑](#cite_ref-3)["MIMD1 - XP/S, CM-5"](http://www.cs.kent.edu/~walker/classes/pdc.f01/lectures/MIMD-1.pdf) (PDF).
4. [↑](#cite_ref-conte_4-0) Conte, G.; Tommesani, S.; Zanichelli, F. (2000). "The long and winding road to high-performance image processing with MMX/SSE".*Proc. Fifth IEEE Int'l Workshop on Computer Architectures for Machine Perception* .[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1109/CAMP.2000.875989](https://doi.org/10.1109%2FCAMP.2000.875989) .[hdl](<https://en.wikipedia.org/wiki/Hdl_(identifier)>) :[11381/2297671](https://hdl.handle.net/11381%2F2297671) .[S2CID](<https://en.wikipedia.org/wiki/S2CID_(identifier)>)[13180531](https://api.semanticscholar.org/CorpusID:13180531) .
5. [↑](#cite_ref-5) Lee, R.B. (1995). "Realtime MPEG video via software decompression on a PA-RISC processor".*digest of papers Compcon '95. Technologies for the Information Superhighway* . pp. 186–192.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1109/CMPCON.1995.512384](https://doi.org/10.1109%2FCMPCON.1995.512384) .[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[0-8186-7029-0](https://en.wikipedia.org/wiki/Special:BookSources/0-8186-7029-0) .[S2CID](<https://en.wikipedia.org/wiki/S2CID_(identifier)>)[2262046](https://api.semanticscholar.org/CorpusID:2262046) .
6. [↑](#cite_ref-6)["AMD Zen 4 AVX-512 Performance Analysis On The Ryzen 9 7950X Review"](https://www.phoronix.com/review/amd-zen4-avx512) .*www.phoronix.com* . Retrieved 2023-07-13.
7. [↑](#cite_ref-7) Patterson, David; Waterman, Andrew (18 September 2017).["SIMD Instructions Considered Harmful"](https://www.sigarch.org/simd-instructions-considered-harmful/) .*SIGARCH* .
8. [↑](#cite_ref-8) Lam, Chester.["GCN, AMD's GPU Architecture Modernization"](https://chipsandcheese.com/p/gcn-amds-gpu-architecture-modernization) .*chipsandcheese.com* .
9. [↑](#cite_ref-9) Lam, Chester.["Hot Chips 34 – AMD's Instinct MI200 Architecture"](https://chipsandcheese.com/p/hot-chips-34-amds-instinct-mi200-architecture) .*chipsandcheese.com* .On both NVIDIA and AMD, matrix instructions break the SIMT abstraction model and work across a whole wavefront (or "warp" on NVIDIA).
10. [↑](#cite_ref-10)["Version 2.3 8/27/2009 OpenCL Programming Guide for the CUDA Architecture"](https://www.nvidia.com/content/cudazone/download/opencl/nvidia_opencl_programmingguide.pdf) (PDF).
11. [↑](#cite_ref-11)[RE: SSE2 speed](https://marc.info/?l=openssl-dev&m=108530261323715&w=2) , showing how SSE2 is used to implement SHA hash algorithms
12. [↑](#cite_ref-12)[Salsa20 speed; Salsa20 software](http://cr.yp.to/snuffle.html#speed) , showing a stream cipher implemented using SSE2
13. [↑](#cite_ref-13)[Subject: up to 1.4x RSA throughput using SSE2](http://markmail.org/message/tygo74tyjagwwnp4) , showing RSA implemented using a non-SIMD SSE2 integer multiply instruction.
14. [↑](#cite_ref-14)["SIMD library math functions"](https://stackoverflow.com/a/36637424) .*Stack Overflow* . Retrieved 16 January 2020.
15. [↑](#cite_ref-15)["Vector Extensions"](https://gcc.gnu.org/onlinedocs/gcc/Vector-Extensions.html) .*Using the GNU Compiler Collection (GCC)* . Retrieved 16 January 2020.
16. [↑](#cite_ref-16)["Clang Language Extensions"](https://clang.llvm.org/docs/LanguageExtensions.html) .*Clang 11 documentation* . Retrieved 16 January 2020.
17. [↑](#cite_ref-17) cppreference.com.["Data-parallel types (SIMD) (since C++26)"](https://en.cppreference.com/cpp/numeric/simd) .*cppreference.com* . cppreference.com. Retrieved 16 August 2026.
18. [↑](#cite_ref-18)["RyuJIT: The next-generation JIT compiler for .NET"](https://devblogs.microsoft.com/dotnet/ryujit-the-next-generation-jit-compiler-for-net) . 30 September 2013.
19. [↑](#cite_ref-19)["The JIT finally proposed. JIT and SIMD are getting married"](https://devblogs.microsoft.com/dotnet/the-jit-finally-proposed-jit-and-simd-are-getting-married) . 7 April 2014.
20. [↑](#cite_ref-20)["JEP 338: Vector API"](https://openjdk.java.net/jeps/338) .
21. [↑](#cite_ref-21) The Rust Devs (14 July 2026).["Module simd"](https://doc.rust-lang.org/std/simd/index.html) .*doc.rust-lang.org* . The Rust Devs.
22. [↑](#cite_ref-22) The Rust Devs (14 July 2026).["Module arch"](https://doc.rust-lang.org/std/arch/index.html) .*doc.rust-lang.org* . The Rust Devs.
23. [↑](#cite_ref-23)["SIMD Directives"](https://www.openmp.org/spec-html/5.0/openmpsu42.html) .*www.openmp.org* .
24. [↑](#cite_ref-24)["Tutorial pragma simd"](https://web.archive.org/web/20201204055745/https://www.cilkplus.org/tutorial-pragma-simd) .*CilkPlus* . 18 July 2012. Archived from[the original](https://www.cilkplus.org/tutorial-pragma-simd) on 4 December 2020. Retrieved 9 August 2020.
25. [↑](#cite_ref-25) Kruse, Michael.["OMP5.1: Loop Transformations"](https://www.openmp.org/wp-content/uploads/OpenMP_SC20_Loop_Transformations.pdf) (PDF).
26. [↑](#cite_ref-26)["simd-everywhere/simde:  Implementations of SIMD instruction sets for systems which don't natively support them"](https://github.com/simd-everywhere/simde) .*GitHub* . SIMD Everywhere. 6 November 2025.
27. [↑](#cite_ref-27) Pharr, Matt; Mark, William R. (May 2012).[*ispc: A SPMD compiler for high-performance CPU programming*](https://ispc.github.io/papers/ispc_inpar_2012.pdf) (PDF). 2012 Innovative Parallel Computing (InPar). pp. 1–13.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1109/InPar.2012.6339601](https://doi.org/10.1109%2FInPar.2012.6339601) .
28. [↑](#cite_ref-28)["Function multi-versioning in GCC 6"](https://lwn.net/Articles/691932/) .*lwn.net* . 22 June 2016.
29. [↑](#cite_ref-29)["2045-target-feature"](https://rust-lang.github.io/rfcs/2045-target-feature.html) .*The Rust RFC Book* .
30. [↑](#cite_ref-clear_30-0)["Transparent use of library packages optimized for Intel® architecture"](https://clearlinux.org/news-blogs/transparent-use-library-packages-optimized-intel-architecture) .*Clear Linux* Project* . Retrieved 8 September 2019.
31. [↑](#cite_ref-31) John McCutchan.["Bringing SIMD to the web via Dart"](https://web.archive.org/web/20131203011540/https://www.dartlang.org/slides/2013/02/Bringing-SIMD-to-the-Web-via-Dart.pdf) (PDF). Archived from[the original](https://www.dartlang.org/slides/2013/02/Bringing-SIMD-to-the-Web-via-Dart.pdf) (PDF) on 2013-12-03.
32. [↑](#cite_ref-32)["SIMD in JavaScript"](https://01.org/node/1495) .*01.org* . 8 May 2014.
33. [↑](#cite_ref-33)["tc39/ecmascript_simd: SIMD numeric type for EcmaScript"](https://github.com/tc39/ecmascript_simd/) .*GitHub* . Ecma TC39. 22 August 2019. Retrieved 8 September 2019.
34. [↑](#cite_ref-34)["Wasm 2.0 Completed - WebAssembly"](https://webassembly.org/news/2025-03-20-wasm-2.0/) .
35. [↑](#cite_ref-35)["Using SIMD with WebAssembly"](https://emscripten.org/docs/porting/simd.html) .*Emscripten 4.0.11-git (dev) documentation* .
36. [↑](#cite_ref-36)["ZiiLABS ZMS-05 ARM 9 Media Processor"](https://web.archive.org/web/20110718153716/https://secure.ziilabs.com/products/processors/zms05.aspx) .*ZiiLabs* . Archived from[the original](https://secure.ziilabs.com/products/processors/zms05.aspx) on 2011-07-18. Retrieved 2010-05-24.

## External links

[
[edit](/w/index.php?title=Single_instruction,_multiple_data&action=edit§ion=18)]
