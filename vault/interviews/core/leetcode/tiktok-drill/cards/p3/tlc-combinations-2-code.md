---
id: tlc-combinations-2-code
node: p3.combinations
type: qa
step: 2
---
## Q
**LC 77 组合**｜写出 Python 实现

整数 `n`、`k`（`1 <= n <= 20`，`1 <= k <= n`），返回 `[1, n]` 中所有 `k` 个数的组合，顺序任意。

## A
**思路。** `dfs(start)` 表示下一个数从 `start` 起选。路径满 `k` 个就收集；否则逐个尝试 `x`，选中后递归到 `x + 1`，再撤销。尝试范围的上界用「剩余的数够不够」收紧。

```python
def combine(n: int, k: int) -> list[list[int]]:
    res: list[list[int]] = []
    path: list[int] = []

    def dfs(start: int) -> None:
        if len(path) == k:
            res.append(path[:])
            return
        need = k - len(path)                       # 还差几个数
        for x in range(start, n - need + 2):       # 剪枝：x 之后剩的数不够就别进
            path.append(x)
            dfs(x + 1)                             # 只往后选，保证组合不重复
            path.pop()

    dfs(1)
    return res
```

运行：`combine(4, 2)` → `[[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]`，`combine(1, 1)` → `[[1]]`，`len(combine(20, 10))` → `184756`，`combine(20, 20)[0][:3]` → `[1, 2, 3]`。

**复杂度。** 时间 `O(k · C(n, k))`：叶子 `C(n, k)` 个，每个拷贝 `k` 个数，内部节点数与叶子同阶；空间 `O(k)`：递归深度和 `path` 长度都不超过 `k`，不含输出。

**写法要点。** `range(start, n - need + 2)` 的上界是「最后一个允许的起点 `n - need + 1`」加 `1`（右开）；`path[:]` 拷贝后才能继续复用 `path`；同样的结果也可以用 `itertools.combinations(range(1, n + 1), k)` 一行生成，它按字典序产出元组，需要 `list(c)` 转成列表。
