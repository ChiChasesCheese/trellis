%% trellis:begin %%
# 伪共享（false sharing）
*硬件：CPU 与内存*

两个线程写不同变量，但变量在同一缓存行，导致缓存行来回弹跳；用填充（padding）和对齐解决。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/hft/map/machine.coherence|缓存一致性（MESI）与核间通信成本]]

**Unlocks:** [[domains/hft/map/cpp.spsc-seqlock|SPSC 环形队列与 seqlock]], [[domains/hft/map/java.disruptor|LMAX Disruptor]]

## Readings
- [[lmax-disruptor-paper|LMAX Disruptor 技术论文]]
- [[mechanical-sympathy-false-sharing|False Sharing]]
- [[wiki-mesi|MESI 缓存一致性协议]]

## Drills
- [[machine-false-sharing-debug|练习：两个互不相干的线程，为什么互相拖慢]]

## Cards (4)
1. [[hft-machine-false-sharing-mechanism]]
2. [[hft-machine-false-sharing-magnitude]]
3. [[hft-machine-false-sharing-padding-vs-sharding]]
4. [[hft-machine-false-sharing-padding-pitfalls]]
%% trellis:end %%

## Notes
