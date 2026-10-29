---
id: uth-cpp-priority-queue-deque-3-deque
node: cpp.priority-queue-deque
type: qa
step: 3
---
## Q
**deque 为什么两头都能 O(1)**｜C++ · std::deque

`std::deque` 的 `push_front` 不用搬元素，它是怎么存的？

## A
**结构。** 块指针数组，每个指针指向一块固定大小的连续内存。

**细节。**

- libstdc++ 每块 512 字节（元素 ≥ 512 字节时每块 1 个）
- libc++ 每块 4096 字节：实测 `deque<int>` 一块连续 1024 个
- 头尾增长只需新增块
- 实测 `push_back` 十万次后，最早元素的地址不变

**为什么。** 头部插入 O(1)，也不整体搬迁元素；代价是下标访问多一次间接寻址。

**坑。** `std::queue` 与 `std::stack` 默认底层容器就是 `deque`。

**对应 LeetCode：** LC 239 滑动窗口最大值 · LC 641 设计循环双端队列
