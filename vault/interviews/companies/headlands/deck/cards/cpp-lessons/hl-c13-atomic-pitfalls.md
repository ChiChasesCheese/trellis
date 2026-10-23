---
id: hl-c13-atomic-pitfalls
node: cpp-lessons.c13-memory-model-atomics
type: qa
step: 17
---
## Q
`atomic` 与无锁相关有哪七个常见的坑？

## A
1. 用 `volatile` 做线程同步（C++ 里无效）。
2. 对 `atomic` 做「先读再写」两步（`if (a == 0) a = 1;`）：不是原子的，要用 CAS。
3. 把 `relaxed` 用到需要发布数据的地方。
4. 在 `atomic<T>` 外面再读写 `T` 的普通副本。
5. 伪共享：计数器数组 `atomic<long> c[8]` 被不同线程分别更新，正好在同一缓存行。
6. 无锁结构里的悬空指针（节点被另一线程释放）。
7. 在循环里自旋而不 `yield`/退避，占满核心。
