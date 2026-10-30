---
id: tlc-random-pick-with-weight-3-why
node: p4.random-pick-with-weight
type: qa
step: 3
---
## Q
**LC 528 按权重随机选择**｜正确性

前缀和加二分的解法里，为什么 `randrange(total)` 必须配 `bisect_right`（或者 `randint(1, total)` 配 `bisect_left`）？写出配错的反例，并说明每个下标的概率为什么恰好是 `w[i] / sum(w)`。

## A
**不变量。** 下标 `i` 管辖的整数是 `[prefix[i] - w[i], prefix[i])`，共 `w[i]` 个，这些区间互不重叠并铺满 `[0, total)`。`r` 在 `[0, total)` 里均匀，所以落进第 `i` 段的概率是 `w[i] / total`。`bisect_right(prefix, r)` 返回第一个 `prefix[i] > r` 的 `i`，正好是 `r` 所在的段。

**反例 `w = [1, 3]`。** `prefix = [1, 4]`，`r` 取 `0, 1, 2, 3`。
- 正确的 `bisect_right`：映射为 `[0, 1, 1, 1]`，下标 `0` 的概率 `1/4`。
- 换成 `bisect_left`：`r = 1` 时 `prefix[0] = 1 >= 1`，被映射到下标 `0`，整体映射为 `[0, 0, 1, 1]`，下标 `0` 的概率变成 `2/4`，错了。

原因是区间左闭右开：`r` 等于前缀和时它已经属于下一段。`randint(1, total)` 取值落在 `[1, total]`，区间变成左开右闭，这时才轮到 `bisect_left`。
