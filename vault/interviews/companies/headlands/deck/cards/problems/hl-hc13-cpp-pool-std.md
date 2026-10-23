---
id: hl-hc13-cpp-pool-std
node: problems.hc13-fixed-memory-pool
type: qa
step: 17
---
## Q
C++ 里为什么要内存池？标准做法 `std::pmr`、placement new、对齐，以及池放进共享内存做 IPC 分别怎么答？

## A
**为什么要池**：分配器耗时不稳定（锁、碎片、系统调用）；池的 `allocate/free` 常数时间、可预测，槽位连续、局部性好。

**标准做法 `std::pmr`**：`monotonic_buffer_resource`（只增长，整体释放）、`unsynchronized_pool_resource`（按大小分档的池，非线程安全）、`synchronized_pool_resource`（线程安全）；容器用 `std::pmr::vector` 等。自己写池是为了固定容量、可预测、能放进共享内存。

**placement new 与对齐**：`new (ptr) T(args)` 在已有内存上构造对象，`ptr` 必须满足 `alignof(T)`；`std::aligned_alloc` / `operator new(size, std::align_val_t)` 提供对齐内存；`alignas(64)` 让数据独占缓存行；`aligned_alloc` 要求 size 是 alignment 整数倍。

**Treiber 栈的内存回收**：槽位在固定数组里永不释放，没有「释放内存后还有人读」的问题（通用无锁结构要用 hazard pointer / epoch / RCU），tag 只处理 ABA。

**放进共享内存做 IPC**：可以。用**下标**（而不是指针）做链接，这正是 `IndexPool` / handle 的设计；arena 放进 `mmap` / `shm_open` 的内存，各进程映射到不同地址，下标仍有效；原子变量要求 `is_always_lock_free`（否则可能是进程私有的锁）。

**arena 释放**：用 `std::free` 释放不会逐个调用析构，要求对象平凡析构。

**tag 为什么放进同一个 64 位原子整数**：ABA 是 head 被改回原值但中间状态已变，tag 与槽位一起放进同一个 64 位原子整数，每次成功操作 +1，整体值不会「回到原样」。

**`IndexPool::free(-1)` 为何一次比较**：`static_cast<uint32_t>(-1) == 0xFFFFFFFF`，不小于容量，和超出上界的情况一样被一次 `b >= size` 拒绝。

**被移动的池**：默认移动对 `head_`、`available_` 只是拷贝，要手写移动让源对象恢复成合法的空池。

练习：把 `ConcurrentPool` 改成每线程缓存 + 批量补货，量吞吐，说清丢掉了哪些保证。
