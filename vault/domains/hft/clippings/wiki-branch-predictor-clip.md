---
title: Branch predictor - Wikipedia
source: https://en.wikipedia.org/wiki/Branch_predictor
published: '2003-12-30'
site: Wikimedia Foundation, Inc.
clipped: '2026-10-23'
---

# Branch predictor - Wikipedia

# Branch predictor

In [computer architecture](https://en.wikipedia.org/wiki/Computer_architecture), a **branch predictor**[\[1\]](#cite_note-dbp-class-report-1)[\[2\]](#cite_note-schemes-and-performances-2)[\[3\]](#cite_note-3)[\[4\]](#cite_note-4)<sup>[\[5\]](#cite_note-5)</sup> is a [digital circuit](https://en.wikipedia.org/wiki/Digital_electronics) that tries to guess which way a [branch](<https://en.wikipedia.org/wiki/Branch_(computer_science)>) (e.g., an [if–then–else structure](<https://en.wikipedia.org/wiki/Conditional_(programming)>)) will go before this is known definitively. The purpose of the branch predictor is to improve the flow in the [instruction pipeline](https://en.wikipedia.org/wiki/Instruction_pipeline). Branch predictors play a critical role in achieving high [performance](https://en.wikipedia.org/wiki/Computer_performance) in many modern [pipelined](https://en.wikipedia.org/wiki/Instruction_pipelining) [microprocessor](https://en.wikipedia.org/wiki/Microprocessor) architectures.

Two-way branching is usually implemented with a [conditional jump](<https://en.wikipedia.org/wiki/Branch_(computer_science)>) instruction. A conditional jump can either be "taken" and jump to a different place in program memory, or it can be "not taken" and continue execution immediately after the conditional jump.  It is not known for certain whether a conditional jump will be taken or not taken until the condition has been calculated and the conditional jump has passed the execution stage in the instruction pipeline (see fig. 1).

Without branch prediction, the processor would have to wait until the conditional jump instruction has passed the execute stage before the next instruction can enter the fetch stage in the pipeline. The branch predictor attempts to avoid this waste of time by trying to guess whether the conditional jump is most likely to be taken or not taken. The branch that is guessed to be the most likely is then fetched and [speculatively executed](https://en.wikipedia.org/wiki/Speculative_execution). If it is later detected that the guess was wrong, then the speculatively executed or partially executed instructions are discarded and the pipeline starts over with the correct branch, incurring a delay.

The time that is wasted in case of a **branch misprediction** is equal to the number of stages in the pipeline from the fetch stage to the execute stage. Modern microprocessors tend to have quite long pipelines so that the misprediction delay is between 10 and 20 [clock cycles](https://en.wikipedia.org/wiki/Clock_cycle). As a result, making a pipeline longer increases the need for a more advanced branch predictor.[\[6\]](#cite_note-6)

The first time a conditional jump instruction is encountered, there is not much information to base a prediction on. However, the branch predictor keeps records of whether or not branches are taken, so when it encounters a conditional jump that has been seen several times before, it can base the prediction on the recorded history. The branch predictor may, for example, recognize that the conditional jump is taken more often than not, or that it is taken every second time.

Branch prediction is not the same as [branch target prediction](https://en.wikipedia.org/wiki/Branch_target_predictor). Branch prediction attempts to guess whether a conditional jump will be taken or not. Branch target prediction attempts to guess the target of a taken conditional or unconditional jump before it is computed by decoding and executing the instruction itself. Branch prediction and branch target prediction are often combined into the same circuitry.

## Implementation

[
[edit](/w/index.php?title=Branch_predictor&action=edit§ion=1)]

### Static branch prediction

[
[edit](/w/index.php?title=Branch_predictor&action=edit§ion=2)]

Static prediction is the simplest branch prediction technique because it does not rely on information about the dynamic history of code executing. Instead, it predicts the outcome of a branch based solely on the branch instruction.<sup>[\[7\]](#cite_note-7)</sup> Early implementations of [SPARC](https://en.wikipedia.org/wiki/SPARC) and [MIPS](https://en.wikipedia.org/wiki/MIPS_architecture) (two of the first commercial [RISC](https://en.wikipedia.org/wiki/RISC) architectures) used single-direction static branch prediction: they always predict that a conditional jump will not be taken, so they always fetch the next sequential instruction. Only when the branch or jump is evaluated and found to be taken, does the instruction pointer get set to a non-sequential address.

Both CPUs fetch instructions in one cycle and evaluate branches in the decode stage. As a result, the branch target recurrence is two cycles long, and the machine always fetches the instruction immediately after any taken branch. Both architectures define [branch delay slots](https://en.wikipedia.org/wiki/Branch_delay_slot) in order to utilize these fetched instructions.

A more-advanced form of static prediction assumes that backward branches will be taken and forward branches will not. (A backward branch is one that has a target address that is lower than its own address.) This rule increases prediction accuracy in loops, which can be constructed with a backward branch at the end that is mostly taken, or a forward branch at the beginning that is mostly not taken. With processors that use this prediction method, ordering the instructions can maximize branch-prediction accuracy. The [RISC-V](https://en.wikipedia.org/wiki/RISC-V) ISA recommends that software written for RISC-V harts (hardware threads), or generated to run on RISC-V harts, be optimized with the assumption that backward branches are taken and forward branches are not. (Even when the processor incorporates a more-advanced predictor that diminishes the relative value of static prediction.)[\[8\]](#cite_note-RISC-V_ISA_20240411-8)

Some processors accept branch-prediction hints that override the static prediction. The [Intel](https://en.wikipedia.org/wiki/Intel) [Pentium 4](https://en.wikipedia.org/wiki/Pentium_4) and [Pentium 4E](https://en.wikipedia.org/wiki/Pentium_4E) accept branch-prediction hints as prefixes. In the presence of dynamic prediction, static prediction offers almost no benefit, and overriding the static prediction helps even less. Intel's subsequent [Pentium M](https://en.wikipedia.org/wiki/Pentium_M) and [Core2](https://en.wikipedia.org/wiki/Intel_Core_2) processors ignore branch-prediction hint prefixes.<sup>[\[9\]](#cite_note-Fog_Microarchitecture-9)</sup> No x86 manufacturer has re-introduced prediction hints.

Dynamic branch predictors naturally fall back on static branch prediction when they have no cached information (such as the first time a given branch is encountered). Both the Motorola [MPC7450 (G4e)](https://en.wikipedia.org/wiki/PowerPC_G4#PowerPC_7450_.22Voyager.22) and the Intel Pentium 4 fall back on static prediction.[\[10\]](#cite_note-10)

In static prediction, all decisions are made at compile time, before the execution of the program.[\[11\]](#cite_note-11)

### Dynamic branch prediction

[
[edit](/w/index.php?title=Branch_predictor&action=edit§ion=3)]

Dynamic branch prediction<sup>[\[2\]](#cite_note-schemes-and-performances-2)</sup> uses information about taken or not-taken branches gathered at run-time to predict the outcome of a branch.[\[1\]](#cite_note-dbp-class-report-1)

### Random branch prediction

[
[edit](/w/index.php?title=Branch_predictor&action=edit§ion=4)]

Random branch prediction means taking a random guess at whether a branch will be taken, each time it is executed. The cost for a pseudorandom number generator is low compared to other techniques. Random prediction guarantees a 50% correct prediction rate that cannot be increased or reduced by any means. (And it makes timing even more nondeterministic or unpredictable than other methods.) Static branch prediction (assuming forward branches are taken and backward branches are not) predicts each branch with an accuracy ranging from 0% to 100%, with the overall success rate somewhere in-between. Unoptimized code is very likely to run with better than 50% prediction success; even 90% is likely. If the compiler does some instruction reordering, it makes the correct branch prediction rate higher than for unoptimized code. Static branch prediction long ago surpassed random branch prediction. Dynamic branch prediction has surpassed static branch prediction and is commonplace, despite the added complexity.

### Next-line prediction

[
[edit](/w/index.php?title=Branch_predictor&action=edit§ion=5)]

Some [superscalar processors](https://en.wikipedia.org/wiki/Superscalar_processor) (MIPS [R8000](https://en.wikipedia.org/wiki/R8000), [Alpha 21264](https://en.wikipedia.org/wiki/Alpha_21264), and [Alpha 21464](https://en.wikipedia.org/wiki/Alpha_21464) (EV8)) fetch each line of instructions with a pointer to the next line. This next-line predictor handles [branch target prediction](https://en.wikipedia.org/wiki/Branch_target_predictor) as well as branch direction prediction.

When a next-line predictor points to aligned groups of 2, 4, or 8 instructions, the branch target will usually not be the first instruction fetched, and so the initial instructions fetched are wasted. Assuming for simplicity, a uniform distribution of branch targets, 0.5, 1.5, and 3.5 instructions fetched are discarded, respectively.

Since the branch itself will generally not be the last instruction in an aligned group, instructions after the taken branch (or its [delay slot](https://en.wikipedia.org/wiki/Delay_slot)) will be discarded. Once again, assuming a uniform distribution of branch instruction placements, 0.5, 1.5, and 3.5 instructions fetched are discarded.

The discarded instructions at the branch and destination lines add up to nearly a complete fetch cycle, even for a single-cycle next-line predictor.

### One-level branch prediction

[
[edit](/w/index.php?title=Branch_predictor&action=edit§ion=6)]

#### Saturating counter

[
[edit](/w/index.php?title=Branch_predictor&action=edit§ion=7)]

A 1-bit saturating counter (essentially a [flip-flop](<https://en.wikipedia.org/wiki/Flip-flop_(electronics)>)) records the last outcome of the branch. This is the most simple version of dynamic branch predictor possible, although it is not very accurate.

A 2-bit [saturating counter](https://en.wikipedia.org/wiki/Saturation_arithmetic)<sup>[\[1\]](#cite_note-dbp-class-report-1)</sup> is a [state machine](https://en.wikipedia.org/wiki/State_machine) with four states:

- Strongly not taken
- Weakly not taken
- Weakly taken
- Strongly taken

When a branch is evaluated, the corresponding state machine is updated. Branches evaluated as not taken change the state toward strongly not taken, and branches evaluated as taken change the state toward strongly taken. The advantage of the two-bit counter scheme over a one-bit scheme is that a conditional jump has to deviate twice from what it has done most in the past before the prediction changes. For example, a loop-closing conditional jump is mispredicted once rather than twice.

The original, non-MMX [Intel Pentium](<https://en.wikipedia.org/wiki/Pentium_(original)>) processor uses a saturating counter, though with an imperfect implementation.[\[9\]](#cite_note-Fog_Microarchitecture-9)

On the [SPEC](https://en.wikipedia.org/wiki/Standard_Performance_Evaluation_Corporation)'89 benchmarks, very large bimodal predictors saturate at 93.5% correct, once every branch maps to a unique counter.[\[12\]](#cite_note-decwrl-tn-36-12)<sup>: 3</sup> 

The predictor table is indexed with the instruction [address](https://en.wikipedia.org/wiki/Memory_address) bits, so that the processor can fetch a prediction for every instruction before the instruction is decoded.

### Two-level predictor

[
[edit](/w/index.php?title=Branch_predictor&action=edit§ion=8)]

The Two-Level Branch Predictor, also referred to as Correlation-Based Branch Predictor, uses a two-dimensional table of counters, also called "Pattern History Table". The table entries are two-bit counters.

#### Two-level adaptive predictor

[
[edit](/w/index.php?title=Branch_predictor&action=edit§ion=9)]

If an `if` statement is executed three times, the decision made on the third execution might depend upon whether the previous two were taken or not. In such scenarios, a two-level adaptive predictor works more efficiently than a saturation counter. Conditional jumps that are taken every second time or have some other regularly recurring pattern are not predicted well by the saturating counter. A two-level adaptive predictor remembers the history of the last n occurrences of the branch and uses one saturating counter for each of the possible 2<sup>n</sup> history patterns. This method is illustrated in figure 3.

Consider the example of n = 2. This means that the last two occurrences of the branch are stored in a two-bit [shift register](https://en.wikipedia.org/wiki/Shift_register). This branch history register can have four different [binary](https://en.wikipedia.org/wiki/Binary_numeral_system) values, 00, 01, 10, and 11, where zero means "not taken" and one means "taken". A pattern history table contains four entries per branch, one for each of the 2<sup>2</sup> = 4 possible branch histories, and each entry in the table contains a two-bit saturating counter of the same type as in figure 2 for each branch. The branch history register is used for choosing which of the four saturating counters to use. If the history is 00, then the first counter is used; if the history is 11, then the last of the four counters is used.

Assume, for example, that a conditional jump is taken every third time. The branch sequence is 001001001... In this case, entry number 00 in the pattern history table will go to state "strongly taken", indicating that after two zeroes comes a one. Entry number 01 will go to state "strongly not taken", indicating that after 01 comes a zero. The same is the case with entry number 10, while entry number 11 is never used because there are never two consecutive ones.

The general rule for a two-level adaptive predictor with an n-bit history is that it can predict any repetitive sequence with any period if all n-bit [sub-sequences](https://en.wikipedia.org/wiki/Subsequence) are different.[\[9\]](#cite_note-Fog_Microarchitecture-9)

The advantage of the two-level adaptive predictor is that it can quickly learn to predict an arbitrary repetitive pattern. This method was invented by T.-Y. Yeh and [Yale Patt](https://en.wikipedia.org/wiki/Yale_Patt) at the [University of Michigan](https://en.wikipedia.org/wiki/University_of_Michigan).<sup>[\[14\]](#cite_note-14)</sup> Since the initial publication in 1991, this method has become very popular, with it being used for later Pentium processors like the Pentium MMX.<sup>[\[15\]](#cite_note-15)</sup> Variants of this prediction method are used in most modern microprocessors.<sup>[*[contradictory](#Neural_branch_prediction)*]</sup><sup>[*[citation needed](https://en.wikipedia.org/wiki/Wikipedia:Citation_needed)*]</sup>

#### Two-level neural predictor

[
[edit](/w/index.php?title=Branch_predictor&action=edit§ion=10)]

A two-level branch predictor where the second level is replaced with a [neural network](https://en.wikipedia.org/wiki/Neural_network) has been proposed.[\[16\]](#cite_note-16)

### Local branch prediction

[
[edit](/w/index.php?title=Branch_predictor&action=edit§ion=11)]

A local branch predictor has a separate history buffer for each conditional jump instruction. It may use a two-level adaptive predictor. The history buffer is separate for each conditional jump instruction, while the pattern history table may be separate as well or it may be shared between all conditional jumps.

The [Intel](https://en.wikipedia.org/wiki/Intel) [Pentium MMX](https://en.wikipedia.org/wiki/Pentium_MMX), [Pentium II](https://en.wikipedia.org/wiki/Pentium_II), and [Pentium III](https://en.wikipedia.org/wiki/Pentium_III) have local branch predictors with a local 4-bit history and a local pattern history table with 16 entries for each conditional jump.

On the [SPEC](https://en.wikipedia.org/wiki/Standard_Performance_Evaluation_Corporation)'89 benchmarks, very large local predictors saturate at 97.1% correct.[\[12\]](#cite_note-decwrl-tn-36-12)<sup>: 6</sup> 

### Global branch prediction

[
[edit](/w/index.php?title=Branch_predictor&action=edit§ion=12)]

A global branch predictor does not keep a separate history record for each conditional jump. Instead it keeps a shared history of all conditional jumps. The advantage of a shared history is that any [correlation](https://en.wikipedia.org/wiki/Correlation) between different conditional jumps is part of making the predictions. The disadvantage is that the history is diluted by irrelevant information if the different conditional jumps are uncorrelated, and that the history buffer may not include any bits from the same branch if there are many other branches in between. It may use a two-level adaptive predictor.

This scheme is better than the saturating counter scheme only for large table sizes, and it is rarely as good as local prediction. The history buffer must be longer in order to make a good prediction. The size of the pattern history table grows [exponentially](https://en.wikipedia.org/wiki/Exponential_function) with the size of the history buffer. Hence, the big pattern history table must be shared among all conditional jumps.

A two-level adaptive predictor with globally shared history buffer and pattern history table is called a "gshare" predictor if it [xors](https://en.wikipedia.org/wiki/XOR_gate) the global history and branch PC, and "gselect" if it [concatenates](https://en.wikipedia.org/wiki/Concatenation) them. Global branch prediction is used in [AMD](https://en.wikipedia.org/wiki/Advanced_Micro_Devices) processors, and in Intel [Pentium M](https://en.wikipedia.org/wiki/Pentium_M), [Core](https://en.wikipedia.org/wiki/Intel_core), [Core 2](https://en.wikipedia.org/wiki/Intel_core_2), and [Silvermont](https://en.wikipedia.org/wiki/Silvermont)-based [Atom](https://en.wikipedia.org/wiki/Intel_Atom) processors.

### Alloyed branch prediction

[
[edit](/w/index.php?title=Branch_predictor&action=edit§ion=13)]

An alloyed branch predictor<sup>[\[17\]](#cite_note-17)</sup> combines the local and global prediction principles by [concatenating](https://en.wikipedia.org/wiki/Concatenation) local and global branch histories, possibly with some bits from the [program counter](https://en.wikipedia.org/wiki/Program_counter) as well. Tests indicate that the [VIA Nano](https://en.wikipedia.org/wiki/VIA_Nano) processor may be using this technique.[\[9\]](#cite_note-Fog_Microarchitecture-9)

### Agree predictor

[
[edit](/w/index.php?title=Branch_predictor&action=edit§ion=14)]

An agree predictor is a two-level adaptive predictor with globally shared history buffer and pattern history table, and an additional local saturating counter. The outputs of the local and the global predictors are XORed with each other to give the final prediction. The purpose is to reduce contentions in the pattern history table where two branches with opposite prediction happen to share the same entry in the pattern history table.[\[18\]](#cite_note-18)

### Hybrid predictor

[
[edit](/w/index.php?title=Branch_predictor&action=edit§ion=15)]

A hybrid predictor, also called combined predictor, implements more than one prediction mechanism. The final prediction is based either on a meta-predictor that remembers which of the predictors has made the best predictions in the past, or a majority vote function based on an odd number of different predictors.

[Scott McFarling](https://en.wikipedia.org/wiki/Scott_McFarling?action=edit&redlink=1) proposed combined branch prediction in his 1993 paper.[\[12\]](#cite_note-decwrl-tn-36-12)

On the SPEC'89 benchmarks, such a predictor is about as good as the local predictor.<sup>[*[citation needed](https://en.wikipedia.org/wiki/Wikipedia:Citation_needed)*]</sup>

Predictors like gshare use multiple table entries to track the behavior of any particular branch. This multiplication of entries makes it much more likely that two branches will map to the same table entry (a situation called aliasing), which in turn makes it much more likely that prediction accuracy will suffer for those branches. Once you have multiple predictors, it is beneficial to arrange that each predictor will have different aliasing patterns, so that it is more likely that at least one predictor will have no aliasing. Combined predictors with different indexing functions for the different predictors are called *gskew* predictors, and are analogous to [skewed associative caches](https://en.wikipedia.org/wiki/CPU_cache#Two-way_skewed_associative_cache) used for data and instruction caching.

### Loop predictor

[
[edit](/w/index.php?title=Branch_predictor&action=edit§ion=16)]

A [conditional jump](https://en.wikipedia.org/wiki/Conditional_jump) that controls a [loop](https://en.wikipedia.org/wiki/Control_flow#Loops) is best predicted with a special loop predictor. A conditional jump in the bottom of a loop that repeats N times will be taken N-1 times and then not taken once. If the conditional jump is placed at the top of the loop, it will be not taken N-1 times and then taken once. A conditional jump that goes many times one way and then the other way once is detected as having loop behavior. Such a conditional jump can be predicted easily with a simple counter. A loop predictor is part of a hybrid predictor where a meta-predictor detects whether the conditional jump has loop behavior.

### Indirect branch predictor

[
[edit](/w/index.php?title=Branch_predictor&action=edit§ion=17)]

An [indirect jump](https://en.wikipedia.org/wiki/Indirect_branch) instruction can choose among more than two branches. Some processors have specialized indirect branch predictors.[\[19\]](#cite_note-19)<sup>[\[20\]](#cite_note-20)</sup> Newer processors from Intel<sup>[\[21\]](#cite_note-21)</sup> and AMD<sup>[\[22\]](#cite_note-22)</sup> can predict indirect branches by using a two-level adaptive predictor. This kind of instruction contributes more than one bit to the history buffer. The [zEC12](<https://en.wikipedia.org/wiki/IBM_zEC12_(microprocessor)>) and later [z/Architecture](https://en.wikipedia.org/wiki/Z/Architecture) processors from IBM support a BRANCH PREDICTION PRELOAD instruction that can preload the branch predictor entry for a given instruction with a branch target address constructed by adding the contents of a general-purpose register to an immediate displacement value.[\[23\]](#cite_note-23)[\[24\]](#cite_note-24)

Processors without this mechanism will simply predict an indirect jump to go to the same target as it did last time.[\[9\]](#cite_note-Fog_Microarchitecture-9)

### Prediction of function returns

[
[edit](/w/index.php?title=Branch_predictor&action=edit§ion=18)]

A [function](https://en.wikipedia.org/wiki/Subroutine) will normally return to where it is called from. The [return instruction](https://en.wikipedia.org/wiki/Return_statement) is an indirect jump that reads its target address from the [call stack](https://en.wikipedia.org/wiki/Call_stack). Many microprocessors have a separate prediction mechanism for return instructions. This mechanism is based on a so-called *return stack buffer*, which is a local mirror of the call stack. The size of the return stack buffer is typically 4–16 entries.[\[9\]](#cite_note-Fog_Microarchitecture-9)

### Overriding branch prediction

[
[edit](/w/index.php?title=Branch_predictor&action=edit§ion=19)]

The [trade-off](https://en.wikipedia.org/wiki/Trade-off) between fast branch prediction and good branch prediction is sometimes dealt with by having two branch predictors. The first branch predictor is fast and simple. The second branch predictor, which is slower, more complex, and with bigger tables, will override a possibly wrong prediction made by the first predictor.

The Alpha 21264 and Alpha EV8 microprocessors used a fast single-cycle next-line predictor to handle the branch target recurrence and provide a simple and fast branch prediction. Because the next-line predictor is so inaccurate, and the branch resolution recurrence takes so long, both cores have two-cycle secondary branch predictors that can override the prediction of the next-line predictor at the cost of a single lost fetch cycle.

The [Intel Core i7](https://en.wikipedia.org/wiki/Intel_Core_i7) has two [branch target buffers](https://en.wikipedia.org/wiki/Branch_target_predictor) and possibly two or more branch predictors.[\[25\]](#cite_note-25)

### Neural branch prediction

[
[edit](/w/index.php?title=Branch_predictor&action=edit§ion=20)]

[Machine learning](https://en.wikipedia.org/wiki/Machine_learning) for branch prediction using [LVQ](https://en.wikipedia.org/wiki/Learning_vector_quantization) and [multilayer perceptrons](https://en.wikipedia.org/wiki/Multilayer_perceptron), called "[neural](<https://en.wikipedia.org/wiki/Neural_network_(machine_learning)>) branch prediction", was proposed by Lucian Vintan ([Lucian Blaga University of Sibiu](https://en.wikipedia.org/wiki/Lucian_Blaga_University_of_Sibiu)).<sup>[\[26\]](#cite_note-26)</sup>
One year later he developed the perceptron branch predictor.<sup>[\[27\]](#cite_note-27)</sup>
The neural branch predictor research was developed much further by Daniel Jimenez.<sup>[\[28\]](#cite_note-jimenez-perceptrons-28)</sup>
In 2001,<sup>[\[28\]](#cite_note-jimenez-perceptrons-28)</sup> the first [perceptron](https://en.wikipedia.org/wiki/Perceptron) predictor was presented that was feasible to implement in hardware. The first commercial implementation of a perceptron branch predictor was in AMD's [Piledriver microarchitecture](<https://en.wikipedia.org/wiki/Piledriver_(microarchitecture)>).[\[29\]](#cite_note-29)

The main advantage of the neural predictor is its ability to exploit long histories while requiring only linear resource growth. Classical predictors require exponential resource growth. Jimenez reports a global improvement of 5.7% over a McFarling-style hybrid predictor.<sup>[\[30\]](#cite_note-jimenez-micro-36-30)</sup> He also used a gshare/perceptron overriding hybrid predictors.[\[30\]](#cite_note-jimenez-micro-36-30)

The main disadvantage of the perceptron predictor is its high latency. Even after taking advantage of high-speed arithmetic tricks, the computation latency is relatively high compared to the clock period of many modern microarchitectures. In order to reduce the prediction latency, Jimenez proposed in 2003 the *fast-path neural predictor*, where the perceptron predictor chooses its weights according to the current branch's path, rather than according to the branch's PC. Many other researchers developed this concept (A. Seznec, M. Monchiero, D. Tarjan & K. Skadron, V. Desmet, Akkary et al., K. Aasaraai, Michael Black, etc.).<sup>[*[citation needed](https://en.wikipedia.org/wiki/Wikipedia:Citation_needed)*]</sup>

Most of the state-of-the-art branch predictors are using a perceptron predictor (see Intel's "Championship Branch Prediction Competition"<sup>[\[31\]](#cite_note-31)</sup>). Intel already implements this idea in one of the [IA-64](https://en.wikipedia.org/wiki/IA-64)'s simulators (2003).[\[32\]](#cite_note-32)

The [AMD](https://en.wikipedia.org/wiki/AMD) [Ryzen](https://en.wikipedia.org/wiki/Ryzen)[\[33\]](#cite_note-33)[\[34\]](#cite_note-34)<sup>[\[35\]](#cite_note-35)</sup> multi-core processor's [Infinity Fabric](https://en.wikipedia.org/wiki/Infinity_Control_Fabric) and the [Samsung](https://en.wikipedia.org/wiki/Samsung) [Exynos](https://en.wikipedia.org/wiki/Exynos) processors include perceptron-based neural branch predictors.

## History

[
[edit](/w/index.php?title=Branch_predictor&action=edit§ion=21)]

The [IBM 7030 Stretch](https://en.wikipedia.org/wiki/IBM_7030_Stretch), designed in the late 1950s, pre-executes all unconditional branches and any conditional branches that depended on the index registers. For other conditional branches, the first two production models implemented predict untaken; subsequent models were changed to implement predictions based on the current values of the indicator bits (corresponding to today's condition codes).<sup>[\[36\]](#cite_note-36)</sup> The Stretch designers had considered static hint bits in the branch instructions early in the project but decided against them. Misprediction recovery was provided by the lookahead unit on Stretch, and part of Stretch's reputation for less-than-stellar performance was blamed on the time required for misprediction recovery. Subsequent IBM large computer designs did not use branch prediction with speculative execution until the [IBM 3090](https://en.wikipedia.org/wiki/IBM_3090) in 1985.

Two-bit predictors were introduced by Tom McWilliams and Curt Widdoes in 1977 for the Lawrence Livermore National Lab S-1 supercomputer and independently by Jim Smith in 1979 at CDC.[\[37\]](#cite_note-37)

Microprogrammed processors, popular from the 1960s to the 1980s and beyond, took multiple cycles per instruction, and generally did not require branch prediction. However, in addition to the IBM 3090, there are several other examples of microprogrammed designs that incorporated branch prediction.

The [Burroughs B4900](https://en.wikipedia.org/wiki/Burroughs_B2500), a microprogrammed COBOL machine released around 1982, was pipelined and used branch prediction. The B4900 branch prediction history state is stored back into the in-memory instructions during program execution. The B4900 implements 4-state branch prediction by using 4 semantically equivalent branch opcodes to represent each branch operator type. The opcode used indicated the history of that particular branch instruction. If the hardware determines that the branch prediction state of a particular branch needs to be updated, it rewrites the opcode with the semantically equivalent opcode that hinted the proper history. This scheme obtains a 93% hit rate. [US patent 4,435,756](https://patents.google.com/patent/US4435756) and others were granted on this scheme.

The DEC [VAX 9000](https://en.wikipedia.org/wiki/VAX_9000), announced in 1989, is both microprogrammed and pipelined, and performs branch prediction.[\[38\]](#cite_note-38)

The first commercial RISC processors, the [MIPS](https://en.wikipedia.org/wiki/MIPS_Technologies) [R2000](<https://en.wikipedia.org/wiki/R2000_(microprocessor)>) and [R3000](https://en.wikipedia.org/wiki/R3000) and the earlier [SPARC](https://en.wikipedia.org/wiki/SPARC) processors, do only trivial "not-taken" branch prediction. Because they use branch delay slots, fetched just one instruction per cycle, and execute in-order, there is no performance loss. The later [R4000](https://en.wikipedia.org/wiki/R4000) uses the same trivial "not-taken" branch prediction, and loses two cycles to each taken branch because the branch resolution recurrence is four cycles long.

Branch prediction became more important with the introduction of pipelined superscalar processors like the Intel [Pentium](<https://en.wikipedia.org/wiki/Pentium_(brand)>), DEC [Alpha 21064](https://en.wikipedia.org/wiki/Alpha_21064), the MIPS [R8000](https://en.wikipedia.org/wiki/R8000), and the [IBM POWER](https://en.wikipedia.org/wiki/IBM_Power_microprocessors) series. These processors all rely on one-bit or simple bimodal predictors.

The DEC [Alpha 21264](https://en.wikipedia.org/wiki/Alpha_21264) (EV6) uses a next-line predictor overridden by a combined local predictor and global predictor, where the combining choice is made by a bimodal predictor.[\[39\]](#cite_note-seznec-39)

The [AMD K8](https://en.wikipedia.org/wiki/AMD_K8) has a combined bimodal and global predictor, where the combining choice is another bimodal predictor. This processor caches the base and choice bimodal predictor counters in bits of the L2 cache otherwise used for ECC. As a result, it has effectively very large base and choice predictor tables, and parity rather than ECC on instructions in the L2 cache. The parity design is sufficient, since any instruction suffering a parity error can be invalidated and refetched from memory.

The [Alpha 21464](https://en.wikipedia.org/wiki/Alpha_21464)<sup>[\[39\]](#cite_note-seznec-39)</sup> (EV8, cancelled late in design) had a minimum branch misprediction penalty of 14 cycles. It was to use a complex but fast next-line predictor overridden by a combined bimodal and majority-voting predictor. The majority vote was between the bimodal and two gskew predictors.

In 2018 a catastrophic [security vulnerability](<https://en.wikipedia.org/wiki/Vulnerability_(computing)>) called [Spectre](<https://en.wikipedia.org/wiki/Spectre_(security_vulnerability)>) was made public by Google's [Project Zero](https://en.wikipedia.org/wiki/Project_Zero) and other researchers. Affecting virtually all modern [CPUs](https://en.wikipedia.org/wiki/Central_processing_unit), the vulnerability involves priming the branch predictors so another process (or the kernel) will mispredict a branch and use secret data as an array index, evicting one of the attacker's cache lines.  The attacker can time access to their own array to find out which one, turning this CPU internal (microarchitectural) state into a value the attacker can save which has information about values they could not read directly.[\[40\]](#cite_note-40)

## See also

[
[edit](/w/index.php?title=Branch_predictor&action=edit§ion=22)]

- [Branch target predictor](https://en.wikipedia.org/wiki/Branch_target_predictor)
- [Branch prediction analysis attacks](https://en.wikipedia.org/wiki/Branch_prediction_analysis_attacks) – on[RSA cryptosystem](https://en.wikipedia.org/wiki/RSA_cryptosystem)[public-key cryptography](https://en.wikipedia.org/wiki/Public-key_cryptography)
- [Branch queue](https://en.wikipedia.org/wiki/Branch_queue)
- [Instruction unit](https://en.wikipedia.org/wiki/Instruction_unit)
- [Cache prefetching](https://en.wikipedia.org/wiki/Cache_prefetching)
- [Indirect branch control](https://en.wikipedia.org/wiki/Indirect_branch_control) (IBC)
- [Indirect branch prediction barrier](https://en.wikipedia.org/wiki/Indirect_branch_prediction_barrier) (IBPB)
- [Indirect branch restricted speculation](https://en.wikipedia.org/wiki/Indirect_branch_restricted_speculation) (IBRS)
- [Predication (computer architecture)](<https://en.wikipedia.org/wiki/Predication_(computer_architecture)>)
- [Single thread indirect branch predictor](https://en.wikipedia.org/wiki/Single_thread_indirect_branch_predictor) (STIBP)

## References

[
[edit](/w/index.php?title=Branch_predictor&action=edit§ion=23)]

1. [1](#cite_ref-dbp-class-report_1-0)[2](#cite_ref-dbp-class-report_1-1)[3](#cite_ref-dbp-class-report_1-2) Malishevsky, Alexey; Beck, Douglas; Schmid, Andreas; Landry, Eric.["Dynamic Branch Prediction"](https://web.archive.org/web/20190717130447/http://web.engr.oregonstate.edu/~benl/Projects/branch_pred/) . Archived from[the original](http://web.engr.oregonstate.edu/~benl/Projects/branch_pred/) on 2019-07-17. Retrieved 2017-03-22.
2. [1](#cite_ref-schemes-and-performances_2-0)[2](#cite_ref-schemes-and-performances_2-1) Cheng, Chih-Cheng.["The Schemes and Performances of Dynamic Branch predictors"](http://bwrcs.eecs.berkeley.edu/Classes/CS252/Projects/Reports/terry_chen.pdf) (PDF).
3. [↑](#cite_ref-3) Parihar, Raj.["Branch Prediction Techniques and Optimizations"](https://web.archive.org/web/20170516211522/http://www.cse.iitd.ernet.in/~srsarangi/col_718_2017/papers/branchpred/branch-pred-many.pdf) (PDF). Archived from[the original](http://www.cse.iitd.ernet.in/~srsarangi/col_718_2017/papers/branchpred/branch-pred-many.pdf) (PDF) on 2017-05-16. Retrieved 2017-04-02.
4. [↑](#cite_ref-4)[Mutlu, Onur](https://en.wikipedia.org/wiki/Onur_Mutlu) (2013-02-11).["18-447 Computer Architecture Lecture 11: Branch Prediction"](https://web.archive.org/web/20150325083615/https://www.ece.cmu.edu/~ece447/s13/lib/exe/fetch.php?media=onur-447-spring13-lecture11-branch-prediction-afterlecture.pdf) (PDF). Archived from[the original](https://www.ece.cmu.edu/~ece447/s13/lib/exe/fetch.php?media=onur-447-spring13-lecture11-branch-prediction-afterlecture.pdf) (PDF) on 2015-03-25.
5. [↑](#cite_ref-5) Michaud, Pierre; Seznec, André; Uhlig, Richard (September 1996).[*Skewed branch predictors*](https://hal.science/inria-00073720/en/) .*HAL* (report).[S2CID](<https://en.wikipedia.org/wiki/S2CID_(identifier)>)[3712157](https://api.semanticscholar.org/CorpusID:3712157) .
6. [↑](#cite_ref-6) Eyerman, S.; Smith, J.E.; Eeckhout, L. (2006).*Characterizing the branch misprediction penalty* . 2006 IEEE International Symposium on Performance Analysis of Systems and Software. IEEE. pp. 48–58.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1109/ispass.2006.1620789](https://doi.org/10.1109%2Fispass.2006.1620789) .[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[1-4244-0186-0](https://en.wikipedia.org/wiki/Special:BookSources/1-4244-0186-0) .[S2CID](<https://en.wikipedia.org/wiki/S2CID_(identifier)>)[72217](https://api.semanticscholar.org/CorpusID:72217) .
7. [↑](#cite_ref-7) Shen, John P.; Lipasti, Mikko (2005).[*Modern processor design: fundamentals of superscalar processors*](https://archive.org/details/modernprocessord00shen) . Boston:[McGraw-Hill Higher Education](https://en.wikipedia.org/wiki/McGraw-Hill_Higher_Education) . pp.[455](https://archive.org/details/modernprocessord00shen/page/n236) .[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[0-07-057064-7](https://en.wikipedia.org/wiki/Special:BookSources/0-07-057064-7) .
8. [↑](#cite_ref-RISC-V_ISA_20240411_8-0)["The RISC-V Instruction Set Manual Volume I Unprivileged Architecture"](https://drive.google.com/file/d/1uviu1nH-tScFfgrovvFCrj7Omv8tFtkp/view?usp=drive_link) .*Google Docs* .
9. [1](#cite_ref-Fog_Microarchitecture_9-0)[2](#cite_ref-Fog_Microarchitecture_9-1)[3](#cite_ref-Fog_Microarchitecture_9-2)[4](#cite_ref-Fog_Microarchitecture_9-3)[5](#cite_ref-Fog_Microarchitecture_9-4)[6](#cite_ref-Fog_Microarchitecture_9-5) Fog, Agner (2016-12-01).["The microarchitecture of Intel, AMD, and VIA CPUs"](https://www.agner.org/optimize/microarchitecture.pdf) (PDF). pp. 26, 38. Retrieved 2017-03-22.
10. [↑](#cite_ref-10)["The Pentium 4 and the G4e: an Architectural Comparison"](https://arstechnica.com/features/2001/05/p4andg4e/#page-4) .*[Ars Technica](https://en.wikipedia.org/wiki/Ars_Technica)* . 12 May 2001.
11. [↑](#cite_ref-11) Plusquellic, Jim.["CMSC 611: Advanced Computer Architecture, Chapter 4 (Part V)"](https://ece-research.unm.edu/jimp/611/slides/chap4_5.html) .
12. [1](#cite_ref-decwrl-tn-36_12-0)[2](#cite_ref-decwrl-tn-36_12-1)[3](#cite_ref-decwrl-tn-36_12-2) McFarling, Scott (June 1993).["Combining Branch Predictors"](https://web.archive.org/web/20221103005540/https://hplabs.itcs.hp.com/techreports/Compaq-DEC/WRL-TN-36.pdf) (PDF). Digital Western Research Lab (WRL) Technical Report, TN-36. Archived from[the original](https://hplabs.itcs.hp.com/techreports/Compaq-DEC/WRL-TN-36.pdf) (PDF) on 2022-11-03.
13. [↑](#cite_ref-13)["New Algorithm Improves Branch Prediction: 3/27/95"](https://www.cs.cmu.edu/afs/cs/academic/class/15213-f00/docs/mpr-branchpredict.pdf) (PDF).*[Microprocessor Report](https://en.wikipedia.org/wiki/Microprocessor_Report)* .**9** (4). March 27, 1995.[Archived](https://web.archive.org/web/20150310190847/https://www.cs.cmu.edu/afs/cs/academic/class/15213-f00/docs/mpr-branchpredict.pdf) (PDF) from the original on 2015-03-10. Retrieved 2016-02-02.
14. [↑](#cite_ref-14) Yeh, T.-Y.;[Patt, Y. N.](https://en.wikipedia.org/wiki/Yale_Patt) (1991). "Two-Level Adaptive Training Branch Prediction".*Proceedings of the 24th annual international symposium on Microarchitecture* . Albuquerque, New Mexico, Puerto Rico: ACM. pp. 51–61.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1145/123465.123475](https://doi.org/10.1145%2F123465.123475) .
15. [↑](#cite_ref-15) Fog, Agner.["Branch prediction in the Pentium family"](https://web.archive.org/web/20080513032603/http://x86.ddj.com/articles/branch/branchprediction.htm) .*Dr. Dobb's Journal* . Archived from[the original](http://x86.ddj.com/articles/branch/branchprediction.htm) on 13 May 2008.
16. [↑](#cite_ref-16) Egan, Colin; Steven, Gordon; Quick, P.; Anguera, R.; Vintan, Lucian (December 2003).["Two-Level Branch Prediction using Neural Networks"](https://www.researchgate.net/publication/264708564) .*Journal of Systems Architecture* .**49** (12–15): 557–570.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1016/S1383-7621(03)00095-X](https://doi.org/10.1016%2FS1383-7621%2803%2900095-X) .
17. [↑](#cite_ref-17) Skadron, K.; Martonosi, M.; Clark, D. W. (October 2000).["A Taxonomy of Branch Mispredictions, and Alloyed Prediction as a Robust Solution to Wrong-History Mispredictions"](https://www.cs.virginia.edu/~skadron/Papers/alloy_pact00.pdf) (PDF).*Proceedings of the 2000 International Conference on Parallel Architectures and Compilation Techniques* . Philadelphia. pp. 199–206.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1109/PACT.2000.888344](https://doi.org/10.1109%2FPACT.2000.888344) .
18. [↑](#cite_ref-18) Sprangle, E.; Chappell, R.S.; Alsup, M.;[Patt, Y.N.](https://en.wikipedia.org/wiki/Yale_Patt) (June 1997).["The Agree Predictor: A Mechanism for Reducing Negative Branch History Interference"](http://meseec.ce.rit.edu/eecc722-fall2006/papers/branch-prediction/5/agree_isca24.pdf) (PDF).*Proceedings of the 24th International Symposium on Computer Architecture* . Denver.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1145/264107.264210](https://doi.org/10.1145%2F264107.264210) .
19. [↑](#cite_ref-19)["Cortex-A15 MPCore Technical Reference Manual, section 6.5.3 "Indirect predictor""](http://infocenter.arm.com/help/index.jsp?topic=/com.arm.doc.ddi0438h/BABEHAJJ.html) .*[ARM Holdings](https://en.wikipedia.org/wiki/ARM_Holdings)* .
20. [↑](#cite_ref-20) Driesen, Karel; Hölzle, Urs (1997-06-25).["Limits of Indirect Branch Prediction"](https://web.archive.org/web/20160506213742/http://hoelzle.org/publications/TRCS97-10.pdf) (PDF). Archived from[the original](http://hoelzle.org/publications/TRCS97-10.pdf) (PDF) on 2016-05-06.
21. [↑](#cite_ref-21) Stokes, Jon (2004-02-25).["A Look at Centrino's Core: The Pentium M"](https://arstechnica.com/features/2004/02/pentium-m/) . pp. 2–3.
22. [↑](#cite_ref-22) Kanter, Aaron (2008-10-28).["Performance Analysis for Core 2 and K8: Part 1"](https://www.realworldtech.com/cpu-perf-analysis/5/) . p. 5.
23. [↑](#cite_ref-23)[*z/Architecture Principles of Operation*](https://publibfp.dhe.ibm.com/epubs/pdf/a227832d.pdf) (PDF) (Fourteenth ed.).[IBM](https://en.wikipedia.org/wiki/IBM) . May 2022. pp. 7-42 – 7-45. SA22-7832-13.
24. [↑](#cite_ref-24)["IBM zEnterprise BC12 Technical Guide"](https://www.redbooks.ibm.com/redbooks/pdfs/sg248138.pdf) (PDF).[IBM](https://en.wikipedia.org/wiki/IBM) . February 2014. p. 78.
25. [↑](#cite_ref-25)[WO 2000/014628](https://worldwide.espacenet.com/textdoc?DB=EPODOC&IDX=WO2000/014628) , Yeh, Tse-Yu & Sharangpani, H. P., "A method and apparatus for branch prediction using a second level branch prediction table", published 2000-03-16
26. [↑](#cite_ref-26) Vintan, Lucian N. (1999).["Towards a High Performance Neural Branch Predictor"](https://web.archive.org/web/20190713224752/http://webspace.ulbsibiu.ro/lucian.vintan/html/USA.pdf) (PDF).*Proceedings International Journal Conference on Neural Networks (IJCNN)* .[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1109/IJCNN.1999.831066](https://doi.org/10.1109%2FIJCNN.1999.831066) . Archived from[the original](http://webspace.ulbsibiu.ro/lucian.vintan/html/USA.pdf) (PDF) on 2019-07-13. Retrieved 2010-12-02.
27. [↑](#cite_ref-27) Vintan, Lucian N. (2000).["Towards a Powerful Dynamic Branch Predictor"](http://webspace.ulbsibiu.ro/lucian.vintan/html/Rom_JIST.pdf) (PDF).*Romanian Journal of Information Science and Technology* .**3** (3). Bucharest: Romanian Academy: 287–301.[ISSN](<https://en.wikipedia.org/wiki/ISSN_(identifier)>)[1453-8245](https://search.worldcat.org/issn/1453-8245) .
28. [1](#cite_ref-jimenez-perceptrons_28-0)[2](#cite_ref-jimenez-perceptrons_28-1) Jimenez, D. A.; Lin, C. (2001).["Dynamic Branch Prediction with Perceptrons"](https://www.cs.utexas.edu/~lin/papers/hpca01.pdf) (PDF).*Proceedings of the 7th International Symposium on High Performance Computer Architecture (HPCA-7)* . Monterrey, NL, Mexico. pp. 197–296.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1109/HPCA.2001.903263](https://doi.org/10.1109%2FHPCA.2001.903263) .
29. [↑](#cite_ref-29) Walton, Jarred (2012-05-15).["The AMD Trinity Review (A10-4600M): A New Hope"](https://web.archive.org/web/20120517123516/http://www.anandtech.com/show/5831/amd-trinity-review-a10-4600m-a-new-hope) .*[AnandTech](https://en.wikipedia.org/wiki/AnandTech)* . Archived from[the original](http://www.anandtech.com/show/5831/amd-trinity-review-a10-4600m-a-new-hope) on May 17, 2012.
30. [1](#cite_ref-jimenez-micro-36_30-0)[2](#cite_ref-jimenez-micro-36_30-1) Jimenez, Daniel A. (December 2003).[*Fast Path-Based Neural Branch Prediction*](https://web.archive.org/web/20160331115200/http://www.microarch.org/micro36/html/pdf/jimenez-FastPath.pdf) (PDF). The 36th Annual IEEE/ACM International Symposium on Microarchitecture (MICRO-36). San Diego, USA. pp. 243–252.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1109/MICRO.2003.1253199](https://doi.org/10.1109%2FMICRO.2003.1253199) . Archived from[the original](http://www.microarch.org/micro36/html/pdf/jimenez-FastPath.pdf) (PDF) on 2016-03-31. Retrieved 2018-04-08.
31. [↑](#cite_ref-31)["Championship Branch Prediction"](https://www.jilp.org/cbp2016/) .
32. [↑](#cite_ref-32) Brekelbaum, Edward; Rupley, Jeff; Wilkerson, Chris; Black, Bryan (December 2002). "Hierarchical scheduling windows".*Proceedings of the 35th International Symposium on Microarchitecture* . Istanbul, Turkey.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1109/MICRO.2002.1176236](https://doi.org/10.1109%2FMICRO.2002.1176236) .
33. [↑](#cite_ref-33) James, Dave (2017-12-06).["AMD Ryzen reviews, news, performance, pricing, and availability"](https://www.pcgamesn.com/amd/amd-zen-release-date-specs-prices-rumours) .*[PCGamesN](https://en.wikipedia.org/wiki/PCGamesN)* .
34. [↑](#cite_ref-34)["AMD Takes Computing to a New Horizon with Ryzen™ Processors"](https://www.amd.com/en/press-releases/amd-takes-computing-2016dec13) (Press release).[AMD](https://en.wikipedia.org/wiki/AMD) . Retrieved 2016-12-14.
35. [↑](#cite_ref-35)["AMD's Zen CPU is now called Ryzen, and it might actually challenge Intel"](http://arstechnica.co.uk/gadgets/2016/12/amd-zen-performance-details-release-date/) .*Ars Technica UK* . Retrieved 2016-12-14.
36. [↑](#cite_ref-36)["IBM Stretch (7030) -- Aggressive Uniprocessor Parallelism"](https://people.computing.clemson.edu/~mark/stretch.html) .
37. [↑](#cite_ref-37)["S-1 Supercomputer"](https://people.computing.clemson.edu/~mark/s1.html) .
38. [↑](#cite_ref-38) Murray, J.E.; Salett, R.M.; Hetherington, R.C.; McKeen, F.X. (1990). "Micro-architecture of the VAX 9000".*Digest of Papers Compcon Spring '90. Thirty-Fifth IEEE Computer Society International Conference on Intellectual Leverage* . pp. 44–53.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1109/CMPCON.1990.63652](https://doi.org/10.1109%2FCMPCON.1990.63652) .[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[0-8186-2028-5](https://en.wikipedia.org/wiki/Special:BookSources/0-8186-2028-5) .[S2CID](<https://en.wikipedia.org/wiki/S2CID_(identifier)>)[24999559](https://api.semanticscholar.org/CorpusID:24999559) .
39. [1](#cite_ref-seznec_39-0)[2](#cite_ref-seznec_39-1) Seznec, A.; Felix, S.; Krishnan, V.; Sazeides, Y.["Design Tradeoffs for the Alpha EV8 Conditional Branch Predictor"](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=988c6e59d2c44b85b8aacc68bc2958cacf76eaf1) .*Proceedings 29th Annual International Symposium on Computer Architecture* .[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1109/ISCA.2002.1003587](https://doi.org/10.1109%2FISCA.2002.1003587) .
40. [↑](#cite_ref-40) Gibbs, Samuel (2018-01-04).["Meltdown and Spectre: 'worst ever' CPU bugs affect virtually all computers"](https://www.theguardian.com/technology/2018/jan/04/meltdown-spectre-worst-cpu-bugs-ever-found-affect-computers-intel-processors-security-flaw) .*the Guardian* . Retrieved 2018-05-18.

## External links

[
[edit](/w/index.php?title=Branch_predictor&action=edit§ion=24)]

- Seznec et al. (1996). "[Multiple-Block Ahead Branch Predictors](https://dl.acm.org/doi/pdf/10.1145/237090.237169) " –  demonstrates prediction accuracy is not impaired by indexing with previous branch address.
- Seznec et al. (2002). "[Design Tradeoffs for the Alpha EV8 Conditional Branch Predictor](https://bpb-us-w2.wpmucdn.com/sites.coecis.cornell.edu/dist/7/587/files/2023/06/Seznec_2022_Design.pdf) " –  describes the Alpha EV8 branch predictor. This paper does an excellent job discussing how they arrived at their design from various hardware constraints and simulation studies.
- Jimenez (2003). "[Reconsidering Complex Branch Predictors](https://people.engr.tamu.edu/djimenez/taco/pdfs/reconsidering.pdf) " –  describes the EV6 and K8 branch predictors, and pipelining considerations.
- Fog, Agner (2009). ["The microarchitecture of Intel, AMD, and VIA CPUs"](https://www.agner.org/optimize/#manuals) . Retrieved 2009-10-01.
- Andrews, Jeff (2007-10-30). ["Branch and Loop Reorganization to Prevent Mispredicts"](https://web.archive.org/web/20181111133652/https://software.intel.com/en-us/articles/branch-and-loop-reorganization-to-prevent-mispredicts) .*Intel Software Network* . Archived from[the original](https://software.intel.com/en-us/articles/branch-and-loop-reorganization-to-prevent-mispredicts) on 2018-11-11. Retrieved 2018-11-10.
- Yee, Alexander (Jun 27, 2012). ["What is Branch Prediction? (first answer, Answer 35214) Why is processing a sorted array faster than processing an unsorted array?"](https://stackoverflow.com/questions/11227809/why-is-processing-a-sorted-array-faster-than-processing-an-unsorted-array) .*Stack Overflow: Java* .
