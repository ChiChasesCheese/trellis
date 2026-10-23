---
id: hl-cq-q34-script
node: cpp-questions.h-os
type: qa
step: 16
---
## Q
用英文 60 秒回答：How does shared memory work between processes, and what are the pitfalls?

## A
结构：`shm_open`、`ftruncate`、`mmap(MAP_SHARED)` → 陷阱：地址不同所以不用指针、无 vtable/`string`/`vector`，只放 POD 加无锁原子 → acquire/release 同步（SPSC 环形实验 100 万条校验和正确）、进程共享互斥/信号量 → 清理 `shm_unlink` 与对端崩溃。

- I create a named object with `shm_open`, size it with `ftruncate`, and each process **`mmap`s it with `MAP_SHARED`**, so both map the same physical pages. Then communication is plain memory access with no system calls.
- The pitfalls: the region can be at **different virtual addresses** in each process, so no raw pointers - use offsets; no vtables, `std::string` or `vector`, because their internals point into one process's private heap; so the shared layout is **plain old data plus lock-free atomics**.
- For synchronization I use atomics with **acquire/release**; in my test a single-producer single-consumer ring moved a million messages between a parent and a forked child and the checksum was correct. For mutual exclusion across processes there are process-shared mutexes or semaphores.
- I also plan for **cleanup** with `shm_unlink` and for a peer crashing mid-write.
