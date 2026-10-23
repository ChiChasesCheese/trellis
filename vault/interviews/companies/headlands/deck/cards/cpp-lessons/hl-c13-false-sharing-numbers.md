---
id: hl-c13-false-sharing-numbers
node: cpp-lessons.c13-memory-model-atomics
type: qa
step: 14
---
## Q
两个线程各对自己的 `atomic<long>` 计数器自增 5000 万次：相邻存放、`alignas(64)` 填充、`alignas(128)` 填充各耗时多少？`sizeof` 各是多少？

## A
```cpp
struct Adjacent { std::atomic<long> a{0}; std::atomic<long> b{0}; };
struct Padded64 { alignas(64) std::atomic<long> a{0}; alignas(64) std::atomic<long> b{0}; };
```
- `sizeof`：Adjacent = 16，Padded64 = 128，Padded128 = 256。
- 耗时：相邻（同一缓存行）**612.7 ms**，`alignas(64)` **68.8 ms**，`alignas(128)` 68.7 ms。
- 相邻存放比各占一行慢约 **10 倍**。
