---
id: hl-cq-cs20-os-lowlatency
node: cpp-questions.cheatsheet
type: qa
step: 20
---
## Q
一句话背诵：系统与低延迟的关键数字——缺页、IPC 共享内存的做法、条件变量对自旋、SPSC 队列、异常、分支。

## A
- 线程共享地址空间，进程不共享（`fork` 写时复制）；映射 512 MB 零缺页，碰过每页才有 **32,768** 次缺页。
- IPC：pipe / socketpair / TCP / **共享内存**（`shm_open` + `ftruncate` + `mmap`，只放 POD + 无锁原子，不放指针）。
- `condition_variable` 往返 **2.4 µs**，自旋 **82 ns**。
- SPSC 环形队列缓存对方索引：**72 → 2 ns/项**。
- 异常：不抛≈零成本，一次抛出 **3–4 µs**。
- 随机分支 **47 ms**，排序后 **8 ms**，无分支 **6 ms**。
