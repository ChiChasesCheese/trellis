---
id: hl-javaq-f-q26-numbers
node: java-questions.f-concurrency
type: qa
step: 5
---
## Q
4 个线程各对计数器做 100 万次 `++`，`volatile`、`synchronized`、`AtomicInteger` 的最终结果各是多少？说明了什么？

## A
期望值 4,000,000：
- `volatile ++`：**684,857**（另一次运行得到 2,148,166）。
- `synchronized`：4,000,000。
- `AtomicInteger`：4,000,000。

**每次不同但都远小于 4,000,000**，正是数据竞争的特征，丢了几十万到三百多万次更新。

计数器用原子类或 `LongAdder`；volatile 只用于状态标志和发布不可变状态。
