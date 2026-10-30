---
id: tlc-lowest-common-ancestor-of-deepest-leaves-4-followup
node: b.lowest-common-ancestor-of-deepest-leaves
type: qa
step: 4
---
## Q
**LC 1123 最深叶节点的最近公共祖先**｜Medium · 字节高频｜追问

面试官接着问：（1）链状树让递归爆栈怎么办？（2）如果结点带父指针，有没有不用后序的做法？（3）改成给定任意一组目标结点，求它们的最近公共祖先（LC 1676）？

## A
1. **递归爆栈**：链状树有 `1000` 层，递归超过 Python 默认上限约 `1000`，抛 `RecursionError`。调大 `sys.setrecursionlimit`，或用 BFS 序倒推的迭代版：

```python
def lca_deepest_leaves_iter(root: TreeNode | None) -> TreeNode | None:
    if root is None:
        return None
    order = [root]                     # BFS 序：父结点一定排在子结点前面
    for node in order:                 # 遍历列表的同时往后追加，等价于队列
        order.extend(child for child in (node.left, node.right) if child)
    info: dict[TreeNode, tuple[int, TreeNode | None]] = {}   # (最深叶子的深度, 它们的最近公共祖先)
    empty = (0, None)                  # 空子树
    for node in reversed(order):       # 逆 BFS 序：孩子先于父亲，等价于后序遍历
        (ld, lca_l), (rd, lca_r) = info.get(node.left, empty), info.get(node.right, empty)
        if ld > rd:
            info[node] = (ld + 1, lca_l)
        elif rd > ld:
            info[node] = (rd + 1, lca_r)
        else:
            info[node] = (ld + 1, node)
    return info[root][1]
```
2. **父指针**：逐层 BFS 到最后一层，得到最深层的全部结点集合；每次把集合里每个结点换成它的父结点（`set` 自动去重），直到只剩一个，那就是 LCA。`O(n)` 时间、`O(n)` 空间，不依赖递归，也不依赖后序。
3. **LC 1676**：后序递归，返回子树里命中的目标数；子树里的命中数（含结点自身）等于目标总数的那个最低结点，就是 LCA。

**Python 提醒**：`for x in lst:` 时往 `lst` 里追加是安全的，删除不是（会跳过元素）；字典以结点对象为键，比用 `val` 更稳妥，值有重复时不会混淆。
