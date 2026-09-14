---
id: cc-toolbox-deque-window-sum
node: toolbox.deque
type: qa
---
## Q
A rolling window over a timestamped stream of 10^6 events must answer "sum of weights currently inside the window" after every event. Structure and cost?

## A
**A deque of `(ts, weight)` plus a running total** — each event is appended once and popped once, so the whole run is O(n) amortized.

```python
while ev and ev[0][0] <= t - window:
    total -= ev.popleft()[1]
ev.append((t, w)); total += w
```

- Never recompute `sum(...)` over the window: that alone turns a linear pass quadratic.
- Store only entries that are genuinely *in* the window — a rejected event must not be appended ([[cc-chrono-windows-denied-not-recorded]]).
- The eviction comparison is the specification, not a detail: `<=` versus `<` moves the boundary event in or out ([[cc-chrono-windows-boundary]]).
- If the window is by **count** rather than time, `deque(maxlen=k)` evicts for you — but it drops the value silently, so you must subtract it before appending, which usually makes the explicit pop clearer.

## Q zh
一个带时间戳的 10^6 事件流上的滚动窗口，需要在每个事件后回答「当前窗口内权重之和」。用什么结构，代价多少？

## A zh
**一个存 `(ts, weight)` 的 deque 加一个运行和** —— 每个事件恰好入队一次、出队一次，整轮摊销 O(n)。

```python
while ev and ev[0][0] <= t - window:
    total -= ev.popleft()[1]
ev.append((t, w)); total += w
```

- 绝不要对窗口重新 `sum(...)`：单这一点就能把线性一趟变成二次。
- 只存真正*在*窗口内的条目 —— 被拒绝的事件不能追加（[[cc-chrono-windows-denied-not-recorded]]）。
- 驱逐的比较符是规范而非细节：`<=` 与 `<` 决定边界事件在窗内还是窗外（[[cc-chrono-windows-boundary]]）。
- 如果窗口按**数量**而非时间划分，`deque(maxlen=k)` 会替你驱逐 —— 但它悄悄丢掉那个值，所以你得在追加前先减掉它，这通常让显式 pop 更清晰。
