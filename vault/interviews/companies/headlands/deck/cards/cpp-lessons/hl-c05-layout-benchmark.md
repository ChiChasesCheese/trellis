---
id: hl-c05-layout-benchmark
node: cpp-lessons.c05-stl-containers
type: qa
step: 19
---
## Q
对 200 万个 `int` 求和，`vector`、`deque`、`list`、`set`、`unordered_map` 每元素各是多少纳秒？说明了什么？

## A
实测每元素耗时（都是 O(n)）：
- `vector`：0.044 ns
- `deque`：0.24 ns
- `list`（按分配顺序）：0.86 ns
- `list`（乱序）：**59.8 ns**
- `set`（红黑树）：2.5 ns
- `unordered_map`：1.2 ns

读法：`vector` 连续内存，硬件预取和 SIMD 都能发挥；**乱序 `list` 每个元素一次缓存未命中**，慢两个数量级。结论：同样的 O(n)，常数差 10–1000 倍，这就是"**默认用 `vector`**"的依据。
