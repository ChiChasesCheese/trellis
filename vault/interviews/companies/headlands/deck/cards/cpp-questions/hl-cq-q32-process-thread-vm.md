---
id: hl-cq-q32-process-thread-vm
node: cpp-questions.h-os
type: qa
step: 1
---
## Q
面试题：进程和线程的区别？什么是虚拟内存、缺页（page fault）？`malloc(1 GB)` 时发生了什么？
Process vs thread. What is virtual memory, a page fault, and what happens on `malloc(1 GB)`?

## A
- **进程**有独立的地址空间；**线程**共享所在进程的地址空间（堆、全局变量），只有各自的栈和寄存器。
- 每个进程看到的是**虚拟地址**，由 MMU 通过页表映射到物理页。
- 内存**按需分配**：`malloc` / `mmap` 一大块只是登记地址范围，第一次真正写到某页时才发生**缺页**，由内核分配物理页。
- `malloc(1 GB)` 通常不会立刻占 1 GB 物理内存：分配器向内核要（大块用 `mmap`），内核只记账。Linux 默认允许**超额承诺**（overcommit），物理内存真不够时 OOM killer 会杀进程。
