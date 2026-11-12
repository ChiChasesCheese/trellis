---
slug: nested-list-weight-sum
---
## Q
**LC 339 嵌套列表加权和**｜Medium

嵌套整数列表 `nestedList`，元素是整数或子列表。整数的深度是嵌套层数（最外层为 `1`），求所有「值 × 深度」之和。

## A
**一句话。** 递归 DFS，整数乘当前深度累加，子列表带着深度加一递归。

```python
def depth_sum(nestedList):
    def dfs(items, depth):
        total = 0
        for item in items:
            if item.isInteger():
                total += item.getInteger() * depth
            else:
                total += dfs(item.getList(), depth + 1)
        return total

    return dfs(nestedList, 1)
```

**复杂度。** 时间 `O(N)`，空间 `O(D)`。

**易错点。**
- 初始深度写 `0`：最外层整数乘 `0`，`[1,[4,[6]]]` 得 `16`，应为 `27`。
- 不先判 `isInteger()` 就 `getInteger()`：子列表返回 `None`，乘法抛 `TypeError`。
- 递归时传 `item` 而非 `item.getList()`：`NestedInteger` 不可迭代。

**追问。**
- 权重反过来（越浅越重，LC 364）？：按层累加，每层整数和重复加进总和，层层滚动，一遍搞定。
- 嵌套很深怕爆栈？：改成按层 BFS，每层把子列表元素并入下一层。

**同模式。** LC 364 嵌套列表加权和 II、LC 341 扁平化嵌套列表迭代器、LC 385 迷你语法分析器、LC 394 字符串解码
