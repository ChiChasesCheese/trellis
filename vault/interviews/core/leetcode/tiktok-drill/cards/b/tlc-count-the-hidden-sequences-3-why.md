---
id: tlc-count-the-hidden-sequences-3-why
node: b.count-the-hidden-sequences
type: qa
step: 3
---
## Q
**LC 2145 统计隐藏数组数目**｜正确性

为什么个数是 `(upper - lower) - (max - min) + 1`？为什么前缀和必须包含开头的 `0`、结果还要和 `0` 取最大值？给出这两处写错的输出。

## A
**不变量。** 起点 `x = hidden[0]` 一旦确定，数组就确定为 `x + prefix[i]`（`i = 0..n`，`prefix[0] = 0`）。数组合法 ⇔ 最小元素不低于 `lower`、最大元素不高于 `upper` ⇔ `x + min(prefix) >= lower` 且 `x + max(prefix) <= upper`。

**个数的推导。** 满足条件的整数 `x` 构成闭区间 `[lower - min(prefix), upper - max(prefix)]`，个数 `(upper - max(prefix)) - (lower - min(prefix)) + 1 = (upper - lower) - (max - min) + 1`。区间为空时这个值 `<= 0`，所以取 `max(0, ...)`。

**为什么要包含 `0`。** `prefix[0] = 0` 对应 `hidden[0]` 自己，它也必须在 `[lower, upper]` 内。漏掉它，`max` / `min` 就没把起点算进去。

**反例 1：漏掉开头的 `0`。** `differences = [1, 2]`，`lower = 1`，`upper = 3`：
- 正确的偏移是 `[0, 1, 3]`，跨度 `3`，`(3 - 1) - 3 + 1 = 0`：数组 `[x, x+1, x+3]` 的跨度 `3` 放不进长度 `2` 的区间，答案 `0`。
- 漏掉 `0` 的错误写法：`prefix = [1, 3]`，跨度 `2`，`(3 - 1) - 2 + 1 = 1`，返回 `1`，错。

**反例 2：不和 `0` 取最大。** `differences = [4, -7, 2]`，`lower = 3`，`upper = 6`：偏移 `[0, 4, -3, -1]`，跨度 `7`，公式值 `(6 - 3) - 7 + 1 = -3`；不取最大就返回 `-3`，答案应当是 `0`。
