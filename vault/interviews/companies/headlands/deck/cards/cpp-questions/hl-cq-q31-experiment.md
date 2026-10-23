---
id: hl-cq-q31-experiment
node: cpp-questions.g-concurrency
type: qa
step: 19
---
## Q
4 个线程各自累加自己的 `atomic<long>` 计数器，每个 2000 万次：计数器相邻（间隔 8 字节）、间隔 64 字节、间隔 128 字节，各花多少时间？差多少倍？实验里的 `Slot` 怎么写？

## A
```cpp
template <std::size_t Pad> struct Slot { alignas(Pad) std::atomic<long> v{0}; };
Slot<Pad> slots[4];    // 线程 t 累加 slots[t].v
```
- 相邻：约 **404 ms**；间隔 64 字节：约 **30 ms**；间隔 128 字节：约 **30 ms**。
- 差距约 **13 倍**，代码逻辑完全相同。
- `std::hardware_destructive_interference_size` 是标准给出的“避免伪共享所需的间隔”常量；libc++ 在这里给出保守的 256。
