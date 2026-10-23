%% trellis:begin %%
# 缓存行、局部性与预取
*硬件：CPU 与内存*

64 字节缓存行、空间局部性与时间局部性、硬件预取器（prefetcher）喜欢顺序访问、指针追逐（pointer chasing）为什么慢。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/hft/map/machine.memory-hierarchy|存储层级与延迟数字]]

**Unlocks:** [[domains/hft/map/machine.coherence|缓存一致性（MESI）与核间通信成本]], [[domains/hft/map/cpp.containers|容器选择：vector、扁平哈希表]], [[domains/hft/map/cpp.warm-cache|缓存预热：让热路径保持热]], [[domains/hft/map/java.object-layout|对象布局与机械同理心（mechanical sympathy）]]

## Readings
- [[drepper-memory|What Every Programmer Should Know About Memory]]
- [[lwn-drepper-cache|Memory part 2: CPU caches]]

## Drills
- [[machine-false-sharing-debug|练习：两个互不相干的线程，为什么互相拖慢]]

## Cards (4)
1. [[hft-machine-cache-lines-what-a-line-is]]
2. [[hft-machine-cache-lines-sequential-vs-pointer-chasing]]
3. [[hft-machine-cache-lines-java-boxed-objects]]
4. [[hft-machine-cache-lines-hot-fields-layout]]
%% trellis:end %%

## Notes
