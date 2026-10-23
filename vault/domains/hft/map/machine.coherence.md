%% trellis:begin %%
# 缓存一致性（MESI）与核间通信成本
*硬件：CPU 与内存*

多核各有私有缓存，MESI 协议保证一致；一个核写、另一个核读时缓存行要在核之间搬运，代价几十纳秒。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/hft/map/machine.cache-lines|缓存行、局部性与预取]]

**Unlocks:** [[domains/hft/map/machine.false-sharing|伪共享（false sharing）]], [[domains/hft/map/machine.memory-ordering|内存序、x86 TSO 与原子操作的成本]]

## Readings
- [[lwn-drepper-cache|Memory part 2: CPU caches]]
- [[wiki-mesi|MESI 缓存一致性协议]]

## Drills
- [[machine-false-sharing-debug|练习：两个互不相干的线程，为什么互相拖慢]]

## Cards (4)
1. [[hft-machine-coherence-mesi-mechanism]]
2. [[hft-machine-coherence-cross-core-cost]]
3. [[hft-machine-coherence-single-writer]]
4. [[hft-machine-coherence-shared-counter-bottleneck]]
%% trellis:end %%

## Notes
