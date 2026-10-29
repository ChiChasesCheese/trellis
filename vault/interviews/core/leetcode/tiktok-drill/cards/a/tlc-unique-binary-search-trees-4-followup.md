---
id: tlc-unique-binary-search-trees-4-followup
node: a.unique-binary-search-trees
type: qa
step: 4
---
## Q
**LC 96 不同的二叉搜索树**｜追问

面试官接着问：（1）为什么答案就是卡特兰数，有没有更快的写法？（2）如果要把所有的树列出来（LC 95），怎么写、数量多大？（3）`n` 大到 `10^5`、结果对 `10^9 + 7` 取模呢？

## A
1. **卡特兰数公式**：`G(n) = C(2n, n) / (n + 1)`。Python 里 `math.comb` 返回精确整数，`//` 之后仍精确，因为 `C(2n, n)` 能被 `n + 1` 整除。

```python
from math import comb

def num_trees_catalan(n: int) -> int:
    return comb(2 * n, n) // (n + 1)
```

`n = 19` → `1767263190`，对 `n = 1..19` 与 DP 结果一致。
2. **列出所有树**：`build(lo, hi)` 返回区间 `[lo, hi]` 里所有 BST；枚举根 `r`，对 `build(lo, r - 1)` 和 `build(r + 1, hi)` 做笛卡尔积（`itertools.product`），空区间返回 `[None]`。数量是卡特兰数，`n = 19` 就有约 `1.77 * 10^9` 棵，所以只能用于很小的 `n`；同一棵子树对象可以在多棵树里共享。
3. **大 `n` 取模**：模数是素数时，预处理阶乘和逆阶乘，`G(n) = (2n)! * inv(n!) * inv(n! * (n + 1)) mod p`，`O(n)` 预处理 + `O(1)` 查询；用 `pow(x, p - 2, p)` 或 `pow(x, -1, p)` 求逆元。

**Python 提醒**：`comb(2 * n, n) / (n + 1)` 用 `/` 会变成浮点数，`n` 稍大就丢精度，必须用 `//`；`math.comb` 需要 Python 3.8 及以上。
