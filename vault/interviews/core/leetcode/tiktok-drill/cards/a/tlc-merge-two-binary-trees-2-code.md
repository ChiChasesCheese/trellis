---
id: tlc-merge-two-binary-trees-2-code
node: a.merge-two-binary-trees
type: qa
step: 2
---
## Q
**LC 617 合并二叉树**｜写出 Python 实现

两棵二叉树 `root1`、`root2`（节点数都在 `[0, 2000]`，`-10^4 <= Node.val <= 10^4`），重叠节点值相加，其余节点原样保留，返回合并后的树的根。

## A
**思路。** 用栈保存「位置相同、都存在」的节点对。弹出一对，值加到 `root1` 的节点上；对左、右孩子分别处理：`root1` 一侧为空就直接接上 `root2` 的子树，两边都有就入栈。

```python
def merge_trees(root1: TreeNode | None, root2: TreeNode | None) -> TreeNode | None:
    if root1 is None:
        return root2
    if root2 is None:
        return root1
    stack = [(root1, root2)]                 # 每项是一对位置相同、都存在的节点
    while stack:
        a, b = stack.pop()
        a.val += b.val                       # 合并结果直接写在 root1 的节点上
        if a.left is None:
            a.left = b.left                  # root1 缺左孩子：整棵挂过来（可能为 None）
        elif b.left is not None:
            stack.append((a.left, b.left))   # 两边都有：继续往下合并
        if a.right is None:
            a.right = b.right
        elif b.right is not None:
            stack.append((a.right, b.right))
    return root1
```

运行：`[1,3,2,5], [2,1,3,null,4,null,7]` → `[3,4,5,5,4,null,7]`，`[1], [1,2]` → `[2,2]`，`[], []` → `[]`，`[1], []` → `[1]`，`两条 2000 个节点的链` → `2000`。

**复杂度。** 时间 `O(min(n1, n2))`；空间 `O(h)`，`h` 为重叠部分的高度。

**写法要点。** 先处理根为空的两种情况，循环里就不用再判断；`a.left = b.left` 在 `a.left` 为 `None` 时一句话完成「整棵搬过来」，包括 `b.left` 也为 `None` 的情形；用 `list` 当栈，`append` 与 `pop()` 都是 `O(1)`；`TreeNode | None` 是 3.10+ 的联合类型写法。
