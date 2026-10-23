---
id: hl-cq-q34-pitfall-pointers-objects
node: cpp-questions.h-os
type: qa
step: 13
---
## Q
为什么共享内存里不能放裸指针，也不能放有虚函数的对象或 `std::string` / `vector`？应该怎么办？

## A
- **裸指针**：同一个共享区在不同进程里的虚拟地址不同，指针会指向别处。用**偏移量**（相对共享区起点的下标）。
- **虚函数 / 内部堆分配**：vptr 指向的是创建者进程里的地址；`std::string` / `vector` 的缓冲区在创建者的私有堆里。
- 办法：用固定大小的 POD 结构，只放纯数据加无锁原子量。
