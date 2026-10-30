---
id: tlc-nested-list-weight-sum-4-followup
node: a.nested-list-weight-sum
type: qa
step: 4
---
## Q
**LC 339 嵌套列表加权和**｜追问

面试官接着问：（1）权重反过来，越浅的整数权重越大（最深的权重为 `1`）？（2）用递归写，并且深度没有 `50` 的上限呢？（3）想一边遍历一边求出最大深度？分别怎么改。

## A
1. **反向加权（LC 364）**：权重 = `最大深度 - 深度 + 1`，最大深度按「含整数的最深一层」计。层序遍历时先记下每层整数之和 `level_sums`，以及含整数的最深一层的下标 `last`，最后第 `i` 层的权重就是 `last + 1 - i`：

```python
def depth_sum_inverse(nestedList: list[NestedInteger]) -> int:
    level_sums: list[int] = []                     # 第 i 层所有整数之和（i 从 0 起）
    last = -1                                      # 含整数的最深一层的下标
    level = nestedList
    while level:
        nxt: list[NestedInteger] = []
        s, has_int = 0, False
        for item in level:
            if item.isInteger():
                s += item.getInteger()
                has_int = True
            else:
                nxt.extend(item.getList())
        if has_int:
            last = len(level_sums)
        level_sums.append(s)
        level = nxt
    return sum(s * (last + 1 - i) for i, s in enumerate(level_sums[: last + 1]))
```

   `[[1,1],2,[1,1]]` → `8`，`[1,[4,[6]]]` → `17`。只在含整数的最深一层之前计权重，所以像 `[5, []]` 这样带空列表的输入不会被空列表多乘一层：结果是 `5`。
2. **递归版与深度**：`dfs(lst, depth)` 一行一个分支，写起来最短，但深度一旦达到几千就 `RecursionError`；没有深度上限时用上面的层序迭代，或者用显式栈 `[(lst, 1)]`。
3. **最大嵌套层数**：基础版的层序循环结束时 `depth - 1` 就是最大嵌套层数（每处理完一层 `depth` 加一，最后一次循环多加了一次）；只有空列表的那一层也算一层，要按「含整数的最深一层」计时，用上面的 `last + 1`。

**Python 提醒**：`level = nxt` 是重新绑定名字，不会改动调用者传入的 `nestedList`；如果写成 `level.extend(...)` 边遍历边扩充同一个列表，遍历顺序与层号都会乱。
