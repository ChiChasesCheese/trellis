%% trellis:begin %%
# std::atomic 与 memory_order
*低延迟 C++*

relaxed、acquire、release、seq_cst 各保证什么，在 x86 上分别编译成什么指令，以及什么时候用哪个。

**Requires:** [[domains/hft/map/machine.memory-ordering|内存序、x86 TSO 与原子操作的成本]]

**Unlocks:** [[domains/hft/map/cpp.spsc-seqlock|SPSC 环形队列与 seqlock]]

## Readings
- [[lea-jdk9-memory-modes|Using JDK 9 Memory Order Modes]]
- [[preshing-acquire-release|Acquire and Release Semantics]]
- [[rigtorp-ringbuffer|Optimizing a ring buffer for throughput]]

## Cards (4)
1. [[hft-cpp-atomics-why-atomic]]
2. [[hft-cpp-atomics-memory-order]]
3. [[hft-cpp-atomics-x86-cost]]
4. [[hft-cpp-atomics-relaxed-pitfall]]
%% trellis:end %%

## Notes
