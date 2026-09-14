---
id: cc-chrono-windows-no-midnight-wrap
node: chrono.windows
type: qa
---
## Q
A badge log for one door reads `23:30`, then `00:10`. Your "three uses within 60 minutes" check treats that gap as 40 minutes. Is it?

## A
**No — within a single day `00:10` is 20 minutes *before* `23:30`, not 40 minutes after it.** `HH:MM` with no date carries no midnight wrap; converted to minutes-since-midnight the two values are 10 and 1410.

- Sort each key's times before windowing — per-key input is rarely sorted, and the whole technique assumes order.
- With `k` events required, the test is `times[i] - times[i-k+1] <= w` over the sorted list: O(n) after the sort, no nested scan ([[cc-algorithms-sliding-window-k-in-window]]).
- Duplicate identical times are separate events and stay in the list; they make the difference 0, which correctly alerts.
- If the spec *does* span days, the timestamps must carry a date; then it is ordinary integer arithmetic and the wrap question disappears.

## Q zh
某扇门的刷卡日志是 `23:30`，然后是 `00:10`。你的「60 分钟内使用三次」检查把这段间隔当成 40 分钟。对吗？

## A zh
**不对 —— 在同一天内，`00:10` 是 `23:30` *之前* 20 分钟，而不是之后 40 分钟。** 不带日期的 `HH:MM` 没有跨午夜的概念；换算成距午夜的分钟数就是 10 和 1410。

- 开窗前先对每个 key 的时间排序 —— 按 key 的输入很少是有序的，而整个技巧都假设有序。
- 需要 `k` 个事件时，判据是有序列表上的 `times[i] - times[i-k+1] <= w`：排序后 O(n)，无需嵌套扫描（[[cc-algorithms-sliding-window-k-in-window]]）。
- 完全相同的重复时间是各自独立的事件，要保留在列表里；它们让差值为 0，从而正确触发。
- 如果 spec 确实跨天，时间戳就必须带日期；那样就是普通整数算术，跨午夜的问题自然消失。
