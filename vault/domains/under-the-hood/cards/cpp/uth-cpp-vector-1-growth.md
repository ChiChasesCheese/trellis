---
id: uth-cpp-vector-1-growth
node: cpp.vector
type: qa
step: 1
---
## Q
**push_back 为什么是均摊 O(1)**｜C++ · libstdc++ / libc++ / MSVC

`std::vector` 连续 `push_back` 时，容量是怎样增长的？

## A
**结构。** 三根指针（begin、end、end_of_storage）指向一整块连续堆内存。

**细节。**

- 满了就申请更大的新块，把旧元素搬过去，再释放旧块
- libstdc++ 与 libc++ 是 2 倍，MSVC 是 1.5 倍
- libc++ 实测连续 push_back 100 次，容量依次为 1 2 4 8 16 32 64 128

**为什么。** 容量按倍数增长，每个元素平均只被搬常数次，总搬运量小于 2n；若每次只加固定的 k，总搬运量就是 O(n²)。

**坑。** 提前知道个数就先 `reserve(n)`，省掉所有中间的重新分配。

**对应 LeetCode：** LC 380 O(1) 时间插入、删除和获取随机元素 · LC 155 最小栈
