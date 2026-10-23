---
id: hl-cq-q34-shared-memory
node: cpp-questions.h-os
type: qa
step: 11
---
## Q
面试题：进程间共享内存是怎么工作的？有哪些陷阱？
How does shared memory work between processes, and what are the pitfalls?

## A
- `shm_open` 创建一个命名的内存对象，`ftruncate` 定大小，各进程 `mmap(MAP_SHARED)` 映射同一份物理页；之后读写就是普通内存访问。
- 要点：
  - 共享区里**不能放指针、虚函数、`std::string` / `vector`** 这类依赖进程私有地址的东西，只放纯数据 + 无锁 `std::atomic`；
  - 同步靠原子量的 acquire / release；
  - 结束时 `shm_unlink`，否则一直留在系统里；
  - 还要考虑对端崩溃发生在写到一半时。
