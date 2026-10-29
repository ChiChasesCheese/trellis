---
id: tlc-unique-binary-search-trees-ii-2-code
node: b.unique-binary-search-trees-ii
type: qa
step: 2
---
## Q
**LC 95 不同的二叉搜索树 II**｜写出 Python 实现

给 `n`（`1 <= n <= 8`），返回所有由值 `1..n` 组成的结构不同的 BST（返回根节点列表，任意顺序）。

## A
**思路。** `build_range(lo, hi)` 返回值域 `[lo, hi]` 上所有 BST 的根。空区间返回 `[None]`。枚举根，左右子树分别递归，用 `product` 取两边所有组合，各新建一个根节点。`@cache` 让同一区间只算一次。

```python
from functools import cache
from itertools import product


def generate_trees(n: int) -> list[TreeNode | None]:
    @cache
    def build_range(lo: int, hi: int) -> list[TreeNode | None]:
        if lo > hi:
            return [None]                         # 空区间：只有「空树」这一种形态
        return [
            TreeNode(root, left, right)
            for root in range(lo, hi + 1)         # 枚举根
            for left, right in product(build_range(lo, root - 1), build_range(root + 1, hi))
        ]
    return build_range(1, n)
```

运行：`n = 3` → `[[1,null,2,null,3],[1,null,3,2],[2,1,3],[3,1,null,null,2],[3,2,null,1]]`；`n = 1` → `[[1]]`；`n = 2` → `[[1,null,2],[2,1]]`；`n = 8` → `1430` 棵。

**复杂度。** 输出 `C_n`（卡特兰数）棵树；共享子树后新建节点数与 `C_n` 同阶，时间、空间 `O(C_n)`；递归深度至多 `n`。

**写法要点。** `itertools.product(A, B)` 替代两层嵌套循环，表达「左右任意组合」；`@cache` 放在闭包上，缓存随每次 `generate_trees` 调用新建，不会跨调用残留；`TreeNode(root, left, right)` 用构造函数一次接好左右孩子；列表推导里多个 `for` 从左到右即外层到内层。
