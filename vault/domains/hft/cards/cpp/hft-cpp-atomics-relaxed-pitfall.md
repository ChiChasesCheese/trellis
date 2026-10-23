---
id: hft-cpp-atomics-relaxed-pitfall
node: cpp.atomics
type: qa
step: 4
---
## Q
把 `memory_order_relaxed` 用在不该用的地方，会出什么问题？请用两个线程的小例子说明为什么“我先写了所以你应该能看到”是错的。

## A
经典例子（store-buffering）：初始 `x = y = 0`。
- 线程 1：`x = 1; r1 = y;`
- 线程 2：`y = 1; r2 = x;`

直觉上 `r1` 和 `r2` 不可能同时为 0，因为总有一个线程的写在先。但在 relaxed 下，每个线程的写先留在**存储缓冲**里，别的核还看不到，就去读对方的变量，于是两个都读到 0。一次实测中，20 万轮里 relaxed 有约 19.9 万轮出现“双零”，`seq_cst` 一次都没有。

第二个典型错误：用 relaxed 的 `ready` 标志去发布数据。消费者看到 `ready == true`，却读到未更新的数据，因为 relaxed 不建立“先于”关系。

这类 bug 难以复现：在 x86 上常常碰巧正常，换到 ARM 或换个编译器版本才出问题。准则：默认 `seq_cst`；只有计数器、统计这类**不用来保护其他数据**的变量才用 relaxed。
