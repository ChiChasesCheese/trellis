---
id: hl-hc04-why-not-arraydeque
node: problems.hc04-queue-mean-snapshot
type: qa
step: 6
---
## Q
为什么队列均值不直接用 `ArrayDeque<Long>` 或 `LinkedList<Long>`？C++ 里 `std::deque` 和环形数组怎么选？

## A
**Java**：`ArrayDeque` 本身也是环形数组，push/pop 也是 O(1)，差别在常数因子：
- **装箱**（boxing）：每个元素一个 `Long` 对象（16–24 字节 + 8 字节引用）；
- **指针追逐**：先读引用再跳到别处，缓存不友好；
- GC 压力。

`long[]` 环形缓冲是连续内存，100 万元素 8 MB 且预取友好。口述：「复杂度一样。我用 `long[]` 避免装箱、提升缓存局部性；没有性能要求我会直接用 `ArrayDeque`，少写代码。」

**C++**：环形缓冲区是一块连续内存、一次分配，缓存友好；`std::deque` 是分块的，每个块单独分配，但扩容不用整体复制。两者都是合理答案，要说得出取舍。接口再包一层 `std::queue` 只是适配器。

C++ 陷阱：默认的移动构造函数对 `int / size_t / __int128` 成员只是拷贝，`QueueMean b = std::move(a);` 之后 `a` 的 `buf_` 已空但 `size_` 还是旧值，`a.push(1)` 越界写；`std::vector<QueueMean>` 扩容时只有移动构造 `noexcept` 才会用移动，否则退回拷贝；`-x`、`std::abs(x)` 对 `LLONG_MIN` 是 UB。
