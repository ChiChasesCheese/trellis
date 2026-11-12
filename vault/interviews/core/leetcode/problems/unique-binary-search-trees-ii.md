---
slug: unique-binary-search-trees-ii
---
## Q
**LC 95 不同的二叉搜索树 II**｜Medium

给整数 `n`，生成所有由节点值 `1` 到 `n` 组成的不同二叉搜索树（BST）。例：`n = 3` → 5 棵。

## A
**一句话。** 区间分治：`build(lo, hi)` 枚举根，左右子树分别取自两侧区间的所有 BST，两两组合，空区间返回 `[None]`，`@cache` 复用相同区间。

```python
def generate_trees(n):
    @cache
    def build(lo, hi):
        if lo > hi:
            return [None]       # 空区间：一种形态，空树
        return [
            TreeNode(root, left, right)
            for root in range(lo, hi + 1)       # 枚举根
            for left, right in product(build(lo, root - 1),
                                       build(root + 1, hi))
        ]
    return build(1, n)
```

**复杂度。** 时间 `O(C_n)`（卡特兰数 `C_n ≈ 4^n / n^1.5`），空间 `O(C_n)`。

**易错点。**
- 空区间返回 `[]` 而不是 `[None]`：`product` 遇空列表得空集，带空子树的根全消失，`n = 3` 得 `0` 棵，应为 `5`。
- 共享子树：多棵树共用节点，调用方改其中一棵会连带改其他棵，要独立副本需深拷贝。

**追问。**
- 只求数量（LC 96）？：卡特兰数 DP `g[i] = Σ g[j-1] · g[i-j]`，或 `comb(2n, n) // (n + 1)`。
- 要每棵树独立？：组合时对左右子树各 `deepcopy`，只去掉 `@cache` 不够，代价 `O(n · C_n)`。

**同模式。** LC 96 不同的二叉搜索树、LC 241 为运算表达式设计优先级、LC 894 所有可能的真二叉树、LC 22 括号生成
