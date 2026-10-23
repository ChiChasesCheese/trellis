---
id: hl-os-virtual-memory
node: foundations.os-processes-threads-ipc
type: qa
step: 5
---
## Q
虚拟内存（virtual memory）是什么？页大小是多少？为什么需要它（四点）？

## A
每个进程以为自己独占一大片连续地址空间。这些**虚拟地址**不直接对应物理内存：CPU 里的 **MMU** 借助内核维护的**页表**（page table）把虚拟地址翻译成物理地址，翻译单位是**页**（page）：x86-64 Linux 默认 4 KB，**Apple 芯片 16 KB**（`sysctl hw.pagesize` = 16384）。

为什么需要：
1. **隔离**：每个进程页表不同，A 的 0x1000 和 B 的 0x1000 指向不同物理页；
2. **按需分配**：`malloc` 一大块只是登记，用到某页才分配物理页（**缺页中断 page fault**）；
3. **映射文件**：把文件的某范围当成内存（`mmap`）；
4. **共享**：两个进程的页表可把不同虚拟地址指向同一物理页，即**共享内存**的原理。
