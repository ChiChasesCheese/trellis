---
id: cc-algorithms-sliding-window-k-in-window
node: algorithms.sliding-window
type: qa
---
## Q
"Alert when the same key is used at least 3 times within any 60 minutes." You hold that key's timestamps. One pass, no nested loop.

## A
**Compare each event with the one `k − 1` places back in the sorted list.**

```python
ts.sort()
alert = any(ts[i] - ts[i - k + 1] <= w for i in range(k - 1, len(ts)))
```

- If those k consecutive events span at most `w`, some window contains k events; if no such `i` exists, none does. That equivalence is the whole proof.
- The comparison is the specification: `<= w` makes exactly 60 minutes alert, `< w` does not. Read the sentence — "within", "at most", "more than" — and pin it ([[cc-chrono-windows-boundary]]).
- Sort first: per-key input is rarely in order, and a key with fewer than k events can never alert.
- Duplicate identical timestamps are separate events and stay in the list; they make the difference 0, which correctly alerts.
- Without a date, `HH:MM` values do not wrap past midnight ([[cc-chrono-windows-no-midnight-wrap]]).

## Q zh
「同一个 key 在任意 60 分钟内被使用至少 3 次就告警。」你手上有该 key 的时间戳。一趟扫描，不要嵌套循环。

## A zh
**在有序列表上，把每个事件与它前面第 `k − 1` 个比较。**

```python
ts.sort()
alert = any(ts[i] - ts[i - k + 1] <= w for i in range(k - 1, len(ts)))
```

- 如果这 k 个连续事件的跨度不超过 `w`，就存在包含 k 个事件的窗口；若不存在这样的 `i`，则一个也没有。这个等价关系就是全部证明。
- 比较符就是规范：`<= w` 让恰好 60 分钟触发告警，`< w` 则不会。读那句话 —— 「within」「at most」「more than」—— 并把它钉死（[[cc-chrono-windows-boundary]]）。
- 先排序：按 key 的输入很少有序，而事件数少于 k 的 key 永远不会告警。
- 完全相同的重复时间戳是各自独立的事件，要保留在列表里；它们让差值为 0，从而正确触发。
- 不带日期时，`HH:MM` 的值不会跨过午夜（[[cc-chrono-windows-no-midnight-wrap]]）。
