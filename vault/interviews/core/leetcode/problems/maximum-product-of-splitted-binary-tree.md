---
slug: maximum-product-of-splitted-binary-tree
---
## Q
**LC 1339 分裂二叉树的最大乘积**｜Medium

删除一条边把二叉树分成两棵子树，求两棵子树节点和的乘积的最大值，对 `10^9 + 7` 取模。

## A
**一句话。** 后序算出每个子树的和 `s`，枚举 `s * (total - s)` 取最大，最后才取模。

```python
def max_product(root):
    sums = []   # 每个子树的和

    def dfs(node):
        if node is None:
            return 0
        s = node.val + dfs(node.left) + dfs(node.right)
        sums.append(s)
        return s

    total = dfs(root)
    return max(s * (total - s) for s in sums) % (10**9 + 7)
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 先取模再比较：取模后大小关系乱了，会选错最大值；Python 整数不溢出，用精确值比，最后再 `% MOD`。
- 误以为根要排除：根的 `s * (total - s)` 为 `0`，不影响最大值。

**追问。**
- 链形树太深怎么办？：改迭代，先序记下父亲下标，倒序把子树和累加给父亲。
- 要返回切的是哪条边？：枚举时记下取最大的那个节点。

**同模式。** LC 508 出现次数最多的子树元素和、LC 563 二叉树的坡度、LC 543 二叉树的直径、LC 337 打家劫舍 III
