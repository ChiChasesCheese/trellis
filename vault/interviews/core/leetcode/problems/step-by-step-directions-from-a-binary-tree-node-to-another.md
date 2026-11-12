---
slug: step-by-step-directions-from-a-binary-tree-node-to-another
---
## Q
**LC 2096 从二叉树一个节点到另一个节点每一步的方向**｜Medium

节点值互不相同的二叉树，求从 `startValue` 到 `destValue` 最短路径的每步方向：`L` 左孩子、`R` 右孩子、`U` 父节点。

## A
**一句话。** 分别求根到起点和终点的 `L/R` 路径，去掉公共前缀（到最近公共祖先），起点剩余步数全换成 `U` 再接终点剩余路径。

```python
def get_directions(root, startValue, destValue):
    def find(node, target, path):
        if node is None:
            return False
        if node.val == target:
            return True
        path.append("L")
        if find(node.left, target, path):
            return True
        path[-1] = "R"           # 复用位置改试右子树
        if find(node.right, target, path):
            return True
        path.pop()               # 都没有：撤销
        return False

    to_start, to_dest = [], []
    find(root, startValue, to_start)
    find(root, destValue, to_dest)
    common = 0
    limit = min(len(to_start), len(to_dest))
    while (common < limit
           and to_start[common] == to_dest[common]):
        common += 1              # 公共前缀 = 根到 LCA
    ups = "U" * (len(to_start) - common)
    return ups + "".join(to_dest[common:])
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- 失败分支漏了 `path.pop()`：`L`、`R` 残留在路径里，前缀错误。
- 把终点剩余路径也换成 `U`：只有起点一侧向上走。
- 链状树深 `10^5`：递归超过 CPython 默认上限，要调高或改迭代。

**追问。**
- 同一棵树查询很多次？：预处理父指针和深度，用倍增 LCA，每次 `O(log n)`。

**同模式。** LC 236 二叉树的最近公共祖先、LC 235 二叉搜索树的最近公共祖先、LC 257 二叉树的所有路径、LC 863 二叉树中所有距离为 K 的结点
