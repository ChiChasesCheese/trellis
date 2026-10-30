---
id: tlc-nested-list-weight-sum-3-why
node: a.nested-list-weight-sum
type: qa
step: 3
---
## Q
**LC 339 嵌套列表加权和**｜正确性

层序解法里，`depth` 为什么从 `1` 开始，并且为什么展开子列表要用 `extend` 而不是 `append`？各给一个写错时的错误输出。

## A
**不变量。** 每次进入 `while` 循环时，`level` 恰好是深度为 `depth` 的所有元素（整数或子列表），不多也不少；循环体结束后，`nxt` 恰好是深度 `depth + 1` 的所有元素。

**为什么 `depth` 从 `1`。** 题目规定最外层整数的深度是 `1`。`level = nestedList` 就是第一层，所以初始 `depth = 1`。

**反例一：`depth` 从 `0` 开始。** `[1,[4,[6]]]`：
- 最外层的 `1` 乘以 `0`，`4` 乘 `1`，`6` 乘 `2`，结果 `0 + 4 + 12 = 16`。
- 正确结果 `1 + 8 + 18 = 27`。

**为什么 `extend`。** `item.getList()` 返回的是一个列表，其中每个元素才是下一层的节点。`nxt.extend(...)` 把这些元素逐个放进 `nxt`，下一轮每个 `item` 都是 `NestedInteger`。

**反例二：`nxt.append(item.getList())`。** `nxt` 的元素变成原生 `list`，下一轮调用 `item.isInteger()` 抛 `AttributeError: 'list' object has no attribute 'isInteger'`。
