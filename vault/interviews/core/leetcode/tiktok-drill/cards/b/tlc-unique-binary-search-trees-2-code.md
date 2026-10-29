---
id: tlc-unique-binary-search-trees-2-code
node: b.unique-binary-search-trees
type: qa
step: 2
---
## Q
**LC 96 不同的二叉搜索树**｜写出 Python 实现

整数 `n`，`1 <= n <= 19`。返回由节点值 `1..n` 恰好构成的不同二叉搜索树的个数，结果在 32 位整数内。

## A
**思路。** `g[i]` 表示 `i` 个节点的 BST 数量，`g[0] = g[1] = 1`。对 `size` 从 `2` 到 `n`，枚举左子树节点数 `left`（`0` 到 `size - 1`），右子树节点数是 `size - 1 - left`，把乘积累加。

```python
def num_trees(n: int) -> int:
    g = [1, 1]                                  # g[i]：i 个节点的 BST 数量；空树算 1 种
    for size in range(2, n + 1):
        g.append(sum(g[left] * g[size - 1 - left] for left in range(size)))
    return g[n]
```

运行：`n = 1` → `1`，`n = 2` → `2`，`n = 3` → `5`，`n = 4` → `14`，`n = 5` → `42`，`n = 19` → `1767263190`。

**复杂度。** 时间 `O(n^2)`：外层 `n` 轮，每轮求和 `size` 项；空间 `O(n)`。

**写法要点。** 用 `append` 边算边存，`g` 的长度始终等于已算出的规模，不用预分配；`sum` 里放生成器表达式，不建中间列表；`g = [1, 1]` 一次性放好两个基准值。更短的是 `math.comb(2 * n, n) // (n + 1)`，但它隐藏了「选根 + 左右相乘」的推导，面试里先写 DP，再提公式作为优化。
