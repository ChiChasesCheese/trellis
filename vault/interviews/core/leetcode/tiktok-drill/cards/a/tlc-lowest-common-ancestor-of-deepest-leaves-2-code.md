---
id: tlc-lowest-common-ancestor-of-deepest-leaves-2-code
node: a.lowest-common-ancestor-of-deepest-leaves
type: qa
step: 2
---
## Q
**LC 1123 最深叶节点的最近公共祖先**｜Medium · 字节高频｜写出 Python 实现

二叉树的根结点 `root`（结点数 `1` 到 `1000`，值互不相同）。返回最深叶结点们的最近公共祖先结点。要求 `O(n)`，且在 `1000` 个结点的链状树上不能因递归深度失败。

## A
**思路。** 先用 BFS 得到结点序 `order`，父在子前。再倒着遍历：每个结点从两个孩子的记录里读出 `(最深叶深度, 该深度叶子的 LCA)`，左右一样深就记自己，否则取更深那一边。根的记录里的 LCA 就是答案。

```python
def lca_deepest_leaves(root: TreeNode | None) -> TreeNode | None:
    if root is None:
        return None
    order = [root]                     # BFS 序：父结点一定排在子结点前面
    for node in order:                 # 遍历列表的同时往后追加，等价于队列
        order.extend(child for child in (node.left, node.right) if child)
    # info[node] = (子树里最深叶子的深度（以 node 为 1）, 这些最深叶子的最近公共祖先)
    info: dict[TreeNode, tuple[int, TreeNode | None]] = {}
    empty = (0, None)                  # 空子树
    for node in reversed(order):       # 逆 BFS 序：孩子先于父亲，等价于后序遍历
        (ld, lca_l), (rd, lca_r) = info.get(node.left, empty), info.get(node.right, empty)
        if ld > rd:
            info[node] = (ld + 1, lca_l)       # 最深的叶子都在左边
        elif rd > ld:
            info[node] = (rd + 1, lca_r)       # 最深的叶子都在右边
        else:
            info[node] = (ld + 1, node)        # 左右一样深（含叶子本身）：node 就是汇合点
    return info[root][1]
```

运行（返回结点的值）：`[3,5,1,6,2,0,8,null,null,7,4]` → `2`，`[1]` → `1`，`[0,1,3,null,2]` → `2`，`[1,2,3]` → `1`，`[1,2,null,3]` → `3`；`1000` 个结点的链状树 → `999`。

**复杂度。** 时间 `O(n)`；空间 `O(n)`。

**写法要点。** `for node in order:` 在遍历时往同一个列表追加，Python 的列表迭代器每步检查下标是否小于当前长度，所以等价于队列，且不需要 `deque`（只追加，不要删除）；`reversed(order)` 给出孩子先于父亲的次序，等价于后序；`info.get(node.left, empty)` 对 `None` 键也能取到默认值，省去判空；结点类默认按对象身份哈希，可以直接做字典的键；`(ld, lca_l), (rd, lca_r) = ...` 嵌套解包一次拿到四个量。
