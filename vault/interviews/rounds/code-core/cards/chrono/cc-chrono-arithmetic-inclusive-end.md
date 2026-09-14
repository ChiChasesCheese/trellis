---
id: cc-chrono-arithmetic-inclusive-end
node: chrono.arithmetic
type: qa
---
## Q
A right is granted at `t` for a duration `d`. Is the last instant it holds `t + d` or `t + d − 1`? Both conventions appear in specs — how do you keep from mixing them?

## A
**Pin the convention in one predicate and call it everywhere.**

- *Inclusive end* — held while `t <= start + d`; expired at `start + d + 1`. A `d = 0` grant is valid for exactly one instant.
- *Exclusive end / half-open* — held while `t < start + d`; free again exactly at `start + d`. A `d = 0` grant holds nothing.

```python
def active(now, expiry): return now <= expiry     # write it once, name it once
```

- Test `expiry − 1`, `expiry`, `expiry + 1` for every part. That triple is what hidden suites probe.
- The same-timestamp case is a separate decision: an event and a query at the same instant resolve in *input order*, not by the comparison.
- Mixing the two readings across parts is the single most common time bug in a multi-part problem.

## Q zh
某项权利在 `t` 授予、时长为 `d`。它生效的最后一刻是 `t + d` 还是 `t + d − 1`？两种约定在 spec 里都出现 —— 怎么避免混用？

## A zh
**把约定固定在一个谓词里，处处调用它。**

- *闭区间右端* —— `t <= start + d` 时有效；`start + d + 1` 过期。`d = 0` 恰好有效一个瞬间。
- *开区间右端 / 半开* —— `t < start + d` 时有效；恰好在 `start + d` 释放。`d = 0` 什么都不持有。

```python
def active(now, expiry): return now <= expiry     # 只写一次，只命名一次
```

- 每个 part 都测 `expiry − 1`、`expiry`、`expiry + 1`。隐藏测试探的就是这三个点。
- 同一时刻的情形是另一个决定：同一瞬间的事件与查询按*输入顺序*解决，而不是靠比较符。
- 在多 part 问题里跨 part 混用这两种读法，是最常见的时间 bug。
