---
id: mlp-coding-pc14-followups
node: coding.pc14
step: 2
type: qa
---
## Q
**流式报价缓冲：追问与变体**｜编程轮

报价缓冲写完后，面试官会往哪些方向追问？

## A
- **只要最新 N 条，不要高低价：** `collections.deque(maxlen=N)`，满了之后 `append` 自动挤掉最左边的一条，不用手写淘汰。
- **环形缓冲（ring buffer，固定长度数组，写指针转圈覆盖最老的数据）：** 预分配 N 个槽，写下标 `i % N`，不产生新对象，内存和延迟最稳定；低延迟系统偏爱它，Python 里 `deque(maxlen=N)` 已经够用。
- **时间窗口而不是条数窗口：** 窗口是"最近 5 秒"。每次写入和每次查询前，先从左边弹掉时间戳不晚于 `now - 5s` 的报价（同时扣掉总和、出单调队列），再计算。

```python
def evict(q, now, span):
    while q and q[0][0] <= now - span:   # 队首时间戳已出窗口
        q.popleft()
```

- **为什么高低价不每次扫窗口：** 扫一遍窗口是 O(N)，行情每秒数万条时跟不上；单调队列让每条报价最多进出各一次。
- **线程安全：** 最简单是一把锁保护全部状态，如上；锁争用成为瓶颈时按 symbol 分片，每个 symbol 一把锁，或者让每个 symbol 只由一个线程写，读线程读取快照。
- **平均价的浮点误差：** 用 `Decimal`，或者累加整数的最小价格单位（tick size），不用 `float` 反复加减。
- **乱序到达：** 报价带时间戳且可能晚到时，deque 的"到达顺序等于时间顺序"假设不成立，要改成按时间戳排序插入的列表（和价格存储是同一个问题）。
- **会多花一个测试用例的边界：** 未写入过的 symbol（抛 `KeyError`）；窗口未满时的平均价；`N = 1`；连续相同价格（单调队列要用 `<=` 和 `>=` 弹出，才不会留下重复项）；价格单调上升或下降；被挤掉的恰好是当前最高价。

**英文答法。**
- "If I only need the last N quotes, **`deque(maxlen=N)`** evicts for me."
- "For a **time window**, I pop from the left while the timestamp is older than now minus the span, before every read and write."
- "If quotes can arrive **out of order**, arrival order no longer equals time order, so I'd keep a sorted structure instead."
