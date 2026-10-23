---
id: hft-machine-tlb-hugepages-translation-and-tlb
node: machine.tlb-hugepages
type: qa
step: 1
---
## Q
程序用的是虚拟地址，CPU 怎么把它变成物理地址？TLB 是什么，为什么需要它？

## A
操作系统给每个进程一个独立的虚拟地址空间，把它切成固定大小的页（page，x86 上默认 4 KB），用**页表**（page table，一张"虚拟页 → 物理页"的映射表）记录每一页对应物理内存的哪里。

问题：页表本身存放在主内存里，而且是多级的（x86-64 通常 4 级）。如果每次访问都去查表，一次内存访问会变成最多 5 次内存访问，太慢。

解决：CPU 里有一块小而快的缓存叫 **TLB**（Translation Lookaside Buffer，翻译后备缓冲），专门保存最近用过的"虚拟页 → 物理页"翻译结果。
- TLB 命中：翻译几乎不花时间。
- TLB 未命中（TLB miss）：硬件要沿着页表逐级读内存（页表遍历，page walk），可能额外花几十到上百个周期。

所以访问内存的真实成本，既取决于数据在不在缓存里，也取决于它的翻译在不在 TLB 里。
