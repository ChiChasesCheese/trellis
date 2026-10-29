---
id: tlc-unique-binary-search-trees-ii-0-whole
node: a.unique-binary-search-trees-ii
type: qa
---
## Q
**LC 95 不同的二叉搜索树 II**｜Medium · CodeTop 国内累计 1 次 · 最近 2026-01-15（CodeTop）

给整数 `n`，生成并返回所有由 `n` 个节点组成、节点值为 `1` 到 `n` 互不相同的**不同二叉搜索树**（BST），可以按任意顺序返回。`1 <= n <= 8`。例：`n = 3` → `[[1,null,2,null,3],[1,null,3,2],[2,1,3],[3,1,null,null,2],[3,2,null,1]]`（共 5 棵）；`n = 1` → `[[1]]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 区间分治：`build(lo, hi)` 返回值域 `[lo, hi]` 上的所有 BST；枚举根 `root`，左子树取自 `build(lo, root-1)`、右子树取自 `build(root+1, hi)`，两两组合；空区间返回 `[None]`；`@cache` 让相同区间只构造一次，子树在多棵树之间共享。

**识别。** 「生成**所有**树」→ 要真正构造出来，不是计数 → 分治 / 回溯。BST 的性质：选定根 `root` 后，左子树恰好由 `[lo, root-1]` 组成、右子树由 `[root+1, hi]` 组成，两边**独立** → 子问题是一个**值域区间**，答案是左右结果的笛卡尔积（`itertools.product`）。`n <= 8`：树的数量是卡特兰数 `C_8 = 1430`，输出本身就是指数级，算法只要与输出同阶。

**推导。** 暴力：枚举 `n!` 个插入顺序，逐个插入 BST，再按结构去重，`O(n! · n)`，`n = 8` 时 `40320` 个排列，多数重复。浪费在于不同插入顺序生成同一棵树。直接按结构构造就没有重复：根有 `n` 种选法，选定后左右子树互不影响，所有组合恰好是全部 BST、且每棵只出现一次。不同的根会反复请求同一区间（比如 `[3, 5]`），用 `@cache` 记住区间结果，子树对象被多棵树共享，每个区间只新建「根」节点。

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

运行：`n = 3` → `[[1,null,2,null,3],[1,null,3,2],[2,1,3],[3,1,null,null,2],[3,2,null,1]]`；`n = 1` → `[[1]]`；`n = 1..8` 的树数依次为 `1, 2, 5, 14, 42, 132, 429, 1430`。

**复杂度。** 输出 `C_n` 棵树。带缓存时，每个长度为 `len` 的区间只新建 `C_len` 个根节点，总共新建 `Σ (n - len + 1) · C_len` 个节点（`n = 8` 时 `2974` 个），与 `C_n` 同阶，时间和空间都是 `O(C_n)`，`C_n ≈ 4^n / n^1.5`。若要求每棵树独立（不共享节点），至少要 `O(n · C_n)`。

**易错点。**
- 空区间返回 `[]` 而不是 `[None]`：`product` 和空列表组合得到空集，所有带空子树的根都消失，`n = 3` 返回 `0` 棵树（正确 `5`）。`[None]` 表示「有一种形态：空树」。
- 共享子树：返回的多棵树共用节点，只读没有问题；调用方若修改其中一棵（比如给某个节点改值），会同时改动其他树。需要独立副本时，对每棵树做一次深拷贝。

**追问。**
- 只求数量（LC 96）：卡特兰数 DP，`g[i] = Σ g[j-1] · g[i-j]`（`j` 为根），或 `math.comb(2n, n) // (n + 1)`。
- 值域换成任意有序数组：区间改成下标区间，结构相同。
- 要求每棵树独立：组合时对左右子树各做一次 `copy.deepcopy`；只去掉 `@cache` 不够，列表推导里同一个 `left` 仍会被多个 `right` 共用。代价是 `O(n · C_n)`。

**同模式。** LC 96 不同的二叉搜索树、LC 241 为运算表达式设计优先级、LC 894 所有可能的真二叉树、LC 22 括号生成。
