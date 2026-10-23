%% trellis:begin %%
# 虚拟内存、TLB 与大页（huge pages）
*硬件：CPU 与内存*

虚拟地址到物理地址的翻译、TLB 缓存翻译结果、TLB miss 引发页表遍历；2 MB / 1 GB 大页如何减少 miss。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/hft/map/machine.memory-hierarchy|存储层级与延迟数字]]

**Unlocks:** [[domains/hft/map/os-network.page-faults|缺页、mlock 与预触内存]], [[domains/hft/map/java.tuning|低延迟 JVM 调优]]

## Readings
- [[drepper-memory|What Every Programmer Should Know About Memory]]
- [[kernel-hugetlbpage|Linux HugeTLB Pages]]
- [[rigtorp-virtual-memory|Virtual memory for low latency applications]]

## Cards (4)
1. [[hft-machine-tlb-hugepages-translation-and-tlb]]
2. [[hft-machine-tlb-hugepages-coverage-numbers]]
3. [[hft-machine-tlb-hugepages-explicit-vs-thp]]
4. [[hft-machine-tlb-hugepages-random-access-heap]]
%% trellis:end %%

## Notes
