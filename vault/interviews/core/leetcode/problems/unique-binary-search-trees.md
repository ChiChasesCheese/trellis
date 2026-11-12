---
slug: unique-binary-search-trees
---
## Q
**LC 96 不同的二叉搜索树**｜Medium

节点值为 `1..n` 的二叉搜索树有多少种形态？

## A
**一句话。** 枚举根，左右子树互相独立、方案数相乘：`G(n) = Σ G(i-1)·G(n-i)`（卡特兰数）。

```python
def num_trees(n):
    g = [1, 1]           # g[k]：k 个节点的 BST 数；空树算 1
    for size in range(2, n + 1):
        g.append(sum(g[l] * g[size-1-l]
                     for l in range(size)))
    return g[n]
```

**复杂度。** 时间 `O(n²)`，空间 `O(n)`。

**易错点。**
- 空树当 `0` 种：`g[0]=0` 会让 `n=2` 得 `0`，应为 `2`。
- 右子树大小写成 `size - l`：根还占一个节点，应为 `size - 1 - l`。

**追问。**
- 要列出所有树？：递归 `build(lo, hi)`，枚举根后对左右列表做笛卡尔积（LC 95）。
- `n` 很大怎么算？：用公式 `C(2n, n) / (n + 1)`，`math.comb` 一步到位。

**同模式。** LC 95 不同的二叉搜索树 II、LC 241 为运算表达式设计优先级、LC 22 括号生成、LC 1130 叶值的最小代价生成树
