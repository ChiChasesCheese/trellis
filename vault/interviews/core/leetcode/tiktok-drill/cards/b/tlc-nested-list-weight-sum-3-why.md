---
id: tlc-nested-list-weight-sum-3-why
node: b.nested-list-weight-sum
type: qa
step: 3
---
## Q
**LC 339 嵌套列表加权和**｜正确性

递归解法里，`depth` 为什么从 `1` 开始，并且为什么子列表要用 `getList()` 取出元素再递归、而不是把 `item` 本身传下去？各给一个写错时的错误输出。

## A
**不变量。** `dfs(items, depth)` 被调用时，`items` 恰好是某个深度为 `depth` 的列表里的全部元素；它返回的是这些元素（含所有更深的后代）贡献的加权和。最外层 `nestedList` 就是深度为 `1` 的那一组。

**为什么 `depth` 从 `1`。** 题目规定最外层整数的深度是 `1`。`nestedList` 就是第一组元素，所以初始 `depth = 1`。

**反例一：`depth` 从 `0` 开始。** `[1,[4,[6]]]`：
- 最外层的 `1` 乘以 `0`，`4` 乘 `1`，`6` 乘 `2`，结果 `0 + 4 + 12 = 16`。
- 正确结果 `1 + 8 + 18 = 27`。

**为什么用 `getList()`。** `item` 是一个 `NestedInteger`，它的子元素要通过 `item.getList()` 取出来；`dfs` 遍历的是元素列表，每个 `item` 都是 `NestedInteger`。

**反例二：`dfs(item, depth + 1)`（漏掉 `getList()`）。** 函数里的 `for item in items` 会去迭代一个 `NestedInteger`，抛 `TypeError: 'NestedInteger' object is not iterable`。
