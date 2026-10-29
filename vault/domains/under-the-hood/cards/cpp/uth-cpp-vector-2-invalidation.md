---
id: uth-cpp-vector-2-invalidation
node: cpp.vector
type: qa
step: 2
---
## Q
**扩容后旧指针为什么悬空**｜C++ · std::vector

先取 `int* p = &v[0]`，再 `push_back` 或 `reserve`，之后用 `p` 为什么可能崩？

## A
**结构。** 迭代器本质上就是指向连续数组的指针。

**细节。**

- 触发扩容：所有迭代器、指针、引用全部失效，因为元素搬进了新块
- 没扩容的 `push_back`：只有 `end()` 失效
- 中间 `insert` / `erase`：该位置及其后面的迭代器失效
- 实测 `reserve(1000)` 之后，`&w[0]` 与原地址不同（libc++）

**为什么。** 连续内存换来 O(1) 随机访问和缓存友好；`std::list` 地址稳定，但每次访问都要跳指针。

**坑。** 遍历时往同一个 vector 里 `push_back` 是未定义行为；删除要用 `it = v.erase(it)`。

**对应 LeetCode：** LC 27 移除元素 · LC 283 移动零
