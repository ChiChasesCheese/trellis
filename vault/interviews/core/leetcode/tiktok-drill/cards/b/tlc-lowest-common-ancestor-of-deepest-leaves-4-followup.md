---
id: tlc-lowest-common-ancestor-of-deepest-leaves-4-followup
node: b.lowest-common-ancestor-of-deepest-leaves
type: qa
step: 4
---
## Q
**LC 1123 最深叶节点的最近公共祖先**｜Medium · 字节高频｜追问

面试官接着问：（1）白板上递归怎么写，有什么坑？（2）如果结点带父指针，有没有不用后序的做法？（3）改成给定任意一组目标结点，求它们的最近公共祖先（LC 1676）？

## A
1. **递归版**：
```python
def lca_deepest_leaves_recursive(root: TreeNode | None) -> TreeNode | None:
    def dfs(node: TreeNode | None) -> tuple[int, TreeNode | None]:
        if node is None:
            return 0, None
        ld, lca_l = dfs(node.left)
        rd, lca_r = dfs(node.right)
        if ld > rd:
            return ld + 1, lca_l
        if rd > ld:
            return rd + 1, lca_r
        return ld + 1, node
    return dfs(root)[1]
```
   坑：链状树有 `1000` 层，调用栈会超过 Python 默认上限，抛 `RecursionError`；面试里说明这一点，再给出 BFS 序倒推的迭代版，或者设置更大的递归上限。
2. **父指针**：逐层 BFS 到最后一层，得到最深层的全部结点集合；每次把集合里每个结点换成它的父结点（`set` 自动去重），直到只剩一个，那就是 LCA。`O(n)` 时间、`O(n)` 空间，不依赖递归。
3. **LC 1676**：后序递归，返回子树里命中的目标数；子树里的命中数（含结点自身）等于目标总数的那个最低结点，就是 LCA。

**Python 提醒**：`for x in lst:` 时往 `lst` 里追加是安全的，删除不是（会跳过元素）；字典以结点对象为键，比用 `val` 更稳妥，值有重复时不会混淆。
