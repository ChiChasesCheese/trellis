---
id: tlc-tt-most-frequent-ties-smaller-3-why
node: p4.tt-most-frequent-ties-smaller
type: qa
step: 3
---
## Q
**出现次数最多的元素（并列取较小的）**｜正确性

求「出现次数最多、并列取最小」时，为什么不能直接用 `Counter(nums).most_common(1)` 或 `max(count, key=count.get)`？复合键 `(-count[x], x)` 保证了什么？给出反例。

## A
**复合键保证的顺序。** 元组按字典序比较：`(-c1, x1) < (-c2, x2)` 当且仅当 `c1 > c2`，或 `c1 == c2` 且 `x1 < x2`。所以 `min` 取到的就是「次数最多；其中数值最小」的元素，两条规则一次比较完成，不依赖遍历顺序。

**为什么那两种写法错。** `most_common` 和 `max(..., key=count.get)` 只比较次数；次数相同时，前者按元素**首次出现的顺序**排，后者返回遍历中先遇到的最大者。`Counter` 的遍历顺序是插入顺序（首次出现顺序），和数值大小无关。

**反例 `[3,1,3,1,2]`。** `3` 和 `1` 都出现 2 次，`3` 先出现。
- `Counter(...).most_common(1)` → `[(3, 2)]`，答案 `3`。
- `max(count, key=count.get)` → `3`。
- 复合键 `min(count, key=lambda x: (-count[x], x))` → `1`（正确）。

**另一个常见错误。** 键写成 `(count[x], x)` 再取 `max`：并列时取到数值**较大**的，同一输入得到 `3`。要用 `max` 就写 `(count[x], -x)`。
