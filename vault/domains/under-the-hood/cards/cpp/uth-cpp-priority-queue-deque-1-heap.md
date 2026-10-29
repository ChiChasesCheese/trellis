---
id: uth-cpp-priority-queue-deque-1-heap
node: cpp.priority-queue-deque
type: qa
step: 1
---
## Q
**priority_queue 是怎么实现的**｜C++ · libstdc++ 16

`std::priority_queue` 是独立的数据结构吗？默认大顶还是小顶？

## A
**结构。** 不是，它只是 `vector` 加上 `push_heap` / `pop_heap` 的一层包装，堆就是数组下标 i 的孩子在 2i+1、2i+2。

**细节。**

- 默认比较器是 `less`，所以是大顶堆（实测依次压入 3 1 4 1 5，`top()` 为 5）
- 用一批数据直接构造时调用 `make_heap`，从最后一个非叶节点往前逐个下沉，总共 O(n)，比逐个 `push` 的 O(n log n) 快

**为什么。** 数组存堆没有指针，缓存友好。

**坑。** 小顶堆要写 `priority_queue<int, vector<int>, greater<int>>`；没有 decrease-key，Dijkstra 靠重复入堆、弹出时跳过过期项。

**对应 LeetCode：** LC 215 数组中的第 K 个最大元素 · LC 347 前 K 个高频元素 · LC 743 网络延迟时间
