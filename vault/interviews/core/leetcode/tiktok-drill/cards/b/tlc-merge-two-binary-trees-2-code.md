---
id: tlc-merge-two-binary-trees-2-code
node: b.merge-two-binary-trees
type: qa
step: 2
---
## Q
**LC 617 合并二叉树**｜写出 Python 实现

两棵二叉树 `root1`、`root2`（节点数都在 `[0, 2000]`，`-10^4 <= Node.val <= 10^4`），重叠节点值相加，其余节点原样保留，返回合并后的树的根。

## A
**思路。** 递归。任一棵为空就返回另一棵（整棵子树原样保留）；两边都有就把值加到 `root1` 的节点上，再用递归结果接成它的左、右孩子，返回 `root1`。

```python
def merge_trees(root1: TreeNode | None, root2: TreeNode | None) -> TreeNode | None:
    if root1 is None:                        # 一边为空：另一边整棵子树原样保留（可能也是 None）
        return root2
    if root2 is None:
        return root1
    root1.val += root2.val                   # 两边都有：值相加，写在 root1 的节点上
    root1.left = merge_trees(root1.left, root2.left)
    root1.right = merge_trees(root1.right, root2.right)
    return root1
```

运行：`[1,3,2,5], [2,1,3,null,4,null,7]` → `[3,4,5,5,4,null,7]`，`[1], [1,2]` → `[2,2]`，`[], []` → `[]`，`[1], []` → `[1]`，`两条 2000 个节点的链` 在默认递归上限下抛 `RecursionError`，调高上限后合并出 `2000` 个节点。

**复杂度。** 时间 `O(min(n1, n2))`；空间 `O(h)`，`h` 为重叠部分的高度（递归栈，2000 层的链会触到默认递归上限）。

**写法要点。** 空节点的两种情况放在递归入口，主体只剩「值相加 + 合并左右」；`root1.left = merge_trees(root1.left, root2.left)` 用返回值重新接孩子，一边为空时「整棵搬过来」自然成立（包括两边都为 `None` 的情形）；结果直接写在 `root1` 上，不新建节点；`TreeNode | None` 是 3.10+ 的联合类型写法。
