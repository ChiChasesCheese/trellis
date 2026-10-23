%% trellis:begin %%
# 内存序、x86 TSO 与原子操作的成本
*硬件：CPU 与内存*

编译器和 CPU 都会重排内存访问；x86 的 TSO 只允许"写后读"重排；屏障（fence）与带 lock 前缀的原子指令的代价。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/hft/map/machine.coherence|缓存一致性（MESI）与核间通信成本]], [[domains/hft/map/machine.pipeline-ooo|流水线、超标量与乱序执行]]

**Unlocks:** [[domains/hft/map/cpp.atomics|std::atomic 与 memory_order]], [[domains/hft/map/java.memory-model|Java 内存模型、volatile 与 VarHandle]]

## Readings
- [[mechanical-sympathy-barriers|Memory Barriers/Fences]]
- [[preshing-acquire-release|Acquire and Release Semantics]]

## Cards (4)
1. [[hft-machine-memory-ordering-why-reorder]]
2. [[hft-machine-memory-ordering-x86-tso-vs-arm]]
3. [[hft-machine-memory-ordering-atomic-cost]]
4. [[hft-machine-memory-ordering-volatile-vs-release]]
%% trellis:end %%

## Notes
