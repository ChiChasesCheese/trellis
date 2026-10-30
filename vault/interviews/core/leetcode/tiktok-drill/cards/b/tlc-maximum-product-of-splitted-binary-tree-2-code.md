---
id: tlc-maximum-product-of-splitted-binary-tree-2-code
node: b.maximum-product-of-splitted-binary-tree
type: qa
step: 2
---
## Q
**LC 1339 分裂二叉树的最大乘积**｜写出 Python 实现

二叉树（节点数 `2 ~ 50000`，值 `1 ~ 10000`），删掉一条边得到两棵子树，求它们节点值之和的乘积的最大值，结果对 `10^9 + 7` 取模。注意树可能退化成长度 `50000` 的链。

## A
**思路。** `dfs(node)` 后序返回以 `node` 为根的子树和（自己加左加右），并把每个子树和追加进 `sums`；根处返回的就是整棵树的和 `total`。删掉某个非根节点与父亲的边，两部分的和是 `s` 和 `total - s`，对所有子树和取 `s * (total - s)` 的最大值，最后再取模。

```python
def max_product(root: TreeNode | None) -> int:
    MOD = 10**9 + 7
    sums: list[int] = []                        # 每个结点为根的子树和（后序顺序）

    def dfs(node: TreeNode | None) -> int:
        if node is None:
            return 0
        s = node.val + dfs(node.left) + dfs(node.right)   # 先子后父：子树和 = 自己 + 左 + 右
        sums.append(s)
        return s

    total = dfs(root)                           # 一遍后序：整棵树的和，顺便收集所有子树和
    # 先在精确整数上取最大，最后才取模；根的子树和是 total，乘积为 0，不影响最大值
    return max(s * (total - s) for s in sums) % MOD
```

运行：`[1,2,3,4,5,6]` → `110`，`[1,null,2,3,4,null,null,5,6]` → `90`，`[2,3,9,10,7,8,6,5,4,11,1]` → `1025`，`[1,1]` → `1`，`10 个节点的链，值都是 10000` → `499999986`。

**复杂度。** 时间 `O(n)`：每个节点访问一次，再枚举一遍；空间 `O(n)`：`sums` 列表加递归栈，递归栈深度等于树高。

**写法要点。** `dfs` 一边返回子树和、一边把它追加进外层的 `sums`（闭包只修改列表，不需要 `nonlocal`），所以一遍遍历同时拿到 `total` 和所有候选；`max(生成器表达式)` 不建中间列表；`% MOD` 放在 `max` 外面，利用 Python 整数不溢出，先精确比较再取模。根的子树和等于 `total`，乘积为 `0`，留在 `sums` 里不影响结果。深度：`1500` 个节点的链就会超过 CPython 默认递归上限（约 `1000`）而抛 `RecursionError`，迭代写法见追问卡。
