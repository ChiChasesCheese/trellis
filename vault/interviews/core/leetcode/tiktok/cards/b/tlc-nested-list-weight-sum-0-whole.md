---
id: tlc-nested-list-weight-sum-0-whole
node: b.nested-list-weight-sum
type: qa
---
## Q
**LC 339 嵌套列表加权和**｜Medium · 近一年被问：美国 1 次、国内 0 次 · 最近 2026-02-27（面试记录）

给一个嵌套整数列表 `nestedList`，每个元素要么是整数，要么是一个列表（列表里的元素同样可以是整数或列表）。整数的**深度**是它所在的嵌套层数，最外层的整数深度为 `1`。返回所有整数「值 × 深度」之和。每个元素通过接口访问：`isInteger()` 判断是否整数，`getInteger()` 取整数值，`getList()` 取子列表。`1 <= nestedList.length <= 50`，整数值在 `[-100, 100]`，最大深度不超过 `50`。例：`[[1,1],2,[1,1]]` → `10`（四个深度 `2` 的 `1` 加一个深度 `1` 的 `2`）；`[1,[4,[6]]]` → `27`（`1*1 + 4*2 + 6*3`）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 按层广度优先：`level` 是当前深度的全部元素，整数乘 `depth` 累加，子列表的内容并进下一层，`depth` 加一；每个元素只处理一次，`O(N)`。

**识别。** 「嵌套结构 + 与深度有关的加权」：把列表看成内部节点、整数看成叶子，深度就是层号，层序遍历或带 `depth` 参数的 DFS 都能做。给的是接口而不是 Python 原生列表，要用 `isInteger()` 区分两种元素，不能直接 `isinstance`。

**推导。** DFS：`dfs(list, depth)` 对整数加 `值 × depth`，对子列表递归 `depth + 1`；深度不超过 `50`，递归完全安全，`O(N)` → 同样是 `O(N)`，但 BFS 的「层号就是深度」更直接，也为变体 LC 364（越浅权重越大）铺路：只要在遍历时记下每层的和，就不用事先知道最大深度 → 选 BFS 作主解：一层一层剥开，整数加权累加，子列表展开成下一层。

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

运行（`NestedInteger` 是题目给的接口）：`[[1,1],2,[1,1]]` → `10`；`[1,[4,[6]]]` → `27`；`[0]` → `0`；嵌套 `50` 层、最里面是 `1` 的列表 → `50`。

**复杂度。** 时间 `O(N)`，`N` 是整数与子列表的总个数；空间 `O(W)`，`W` 是元素最多的那一层的宽度。

**易错点。**
- `depth` 初值写成 `0`：最外层整数被乘 `0`，`[1,[4,[6]]]` 得到 `16`，正确是 `27`。
- 不先判断 `isInteger()` 就对元素调用 `getInteger()`：子列表的 `getInteger()` 返回 `None`，乘法抛 `TypeError`。
- 用 `nxt.append(item.getList())`：下一层的元素变成原生 `list`，再调用 `.isInteger()` 抛 `AttributeError`，要用 `extend` 把子列表**展开**。

**追问。**
- LC 364（权重反过来，越浅越重）：层序遍历时记下每层的整数之和，以及含整数的最深一层的下标 `last`，第 `i` 层（从 `0` 起）的权重是 `last + 1 - i`，一遍遍历完成，不用先单独求最大深度；`[[1,1],2,[1,1]]` → `8`，`[1,[4,[6]]]` → `17`。
- 嵌套深度没有保证、可能很深：递归会爆栈，BFS 版本本来就是迭代，不受影响。
- 只求最大嵌套层数：循环结束时的 `depth - 1`。

**同模式。** LC 364 嵌套列表加权和 II、LC 341 扁平化嵌套列表迭代器、LC 385 迷你语法分析器、LC 394 字符串解码。
