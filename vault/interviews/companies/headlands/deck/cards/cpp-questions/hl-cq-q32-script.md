---
id: hl-cq-q32-script
node: cpp-questions.h-os
type: qa
step: 6
---
## Q
用英文 60 秒回答：Process vs thread. What is virtual memory, a page fault, and what happens on `malloc(1 GB)`?

## A
结构：独立 vs 共享地址空间、虚拟地址按需分配 → 实验：映射 512 MB 零缺页，碰每页 32,768 次缺页，`fork` 子进程写不影响父进程 → 延迟含义：预触碰、锁内存、大页 → `malloc(1 GB)` 只保留地址空间、overcommit 与 OOM killer。

- Processes have **separate address spaces**; threads share one and only have their own stacks and registers. Each process sees **virtual addresses**, translated through page tables, and memory is allocated **lazily**.
- In an experiment I mapped 512 MB: zero page faults and about 1 MB resident. Touching one byte per page then produced 32,768 **page faults**, and resident memory rose to 513 MB. After `fork` a child's write to a variable didn't change the parent's copy, while a thread's write did.
- For latency this matters: the first touch of memory is a fault costing microseconds, so low-latency systems **pre-fault** and often lock their memory, and use **huge pages** to reduce TLB misses.
- `malloc(1 GB)` just reserves address space; the OS may overcommit and the OOM killer steps in if it can't back it.
