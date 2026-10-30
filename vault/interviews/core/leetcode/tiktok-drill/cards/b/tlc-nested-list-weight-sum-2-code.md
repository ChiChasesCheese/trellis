---
id: tlc-nested-list-weight-sum-2-code
node: b.nested-list-weight-sum
type: qa
step: 2
---
## Q
**LC 339 嵌套列表加权和**｜写出 Python 实现

嵌套整数列表 `nestedList`（`1 <= 长度 <= 50`，整数值 `[-100, 100]`，最大深度 `<= 50`），元素通过 `isInteger()`、`getInteger()`、`getList()` 访问，最外层深度为 `1`，返回所有整数「值 × 深度」之和。

## A
**思路。** 用 `level` 保存当前深度的全部元素。扫描 `level`：整数就加上 `值 × depth`，子列表就把它的元素追加到 `nxt`。一层结束后 `level = nxt`，`depth += 1`，直到没有元素。

```python
def depth_sum(nestedList: list[NestedInteger]) -> int:
    total, depth = 0, 1
    level = nestedList
    while level:                                   # 一层一层剥：level 是当前深度的所有元素
        nxt: list[NestedInteger] = []
        for item in level:
            if item.isInteger():
                total += item.getInteger() * depth
            else:
                nxt.extend(item.getList())         # 子列表的元素留给下一层
        level = nxt
        depth += 1
    return total
```

运行（`NestedInteger` 是题目给的接口）：`[[1,1],2,[1,1]]` → `10`；`[1,[4,[6]]]` → `27`；`[0]` → `0`；嵌套 `50` 层的 `[[...[1]...]]` → `50`。

**复杂度。** 时间 `O(N)`：每个整数和子列表各处理一次；空间 `O(W)`：同时只保留两层，`W` 是最宽的那一层。

**写法要点。** `list.extend` 把子列表的元素**展开**到下一层，用 `append` 会多套一层列表；`total, depth = 0, 1` 一行初始化两个不同含义的变量；`while level` 利用空列表为假作为终止条件，不需要单独计算最大深度。
