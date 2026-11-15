---
slug: validate-binary-tree-nodes
---
## Q
**LC 1361 验证二叉树**｜Medium

`n` 个结点编号 `0..n-1`，`leftChild[i]`、`rightChild[i]` 是结点 `i` 的左右孩子（没有为 `-1`）。判断这些结点是否恰好构成一棵有效的二叉树。

## A
**一句话。** 有效二叉树当且仅当：每个结点入度至多 1，恰有一个入度为 0 的根，且从根出发能到达全部 `n` 个结点。

```python
def validate_binary_tree_nodes(n, left_child, right_child):
    indeg = [0] * n
    for c in left_child + right_child:
        if c != -1:
            indeg[c] += 1
            if indeg[c] > 1:
                return False           # 两个父结点
    roots = [i for i in range(n) if indeg[i] == 0]
    if len(roots) != 1:
        return False                   # 必须恰有一个根
    seen, q = {roots[0]}, deque(roots)
    while q:
        u = q.popleft()
        for c in (left_child[u], right_child[u]):
            if c != -1:
                seen.add(c)
                q.append(c)
    return len(seen) == n              # 全部连通
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 只检查入度：入度都 `≤ 1` 且有一个根时，仍可能有一个不连通的环，要靠连通性检查排除。
- 找不到根就继续：没有入度为 0 的结点说明全是环，直接返回 `False`。
- 根唯一性漏检：多个根是森林而不是树。

**追问。**
- 另一种判定？：一棵树恰有 `n - 1` 条边、入度至多 1、且连通，三个条件。
- 并查集怎么做？：合并父子，遇到已在同一集合或孩子已有父亲就失败，最后看集合数是否为 1。

**同模式。** LC 207 课程表、LC 684 冗余连接（Redundant Connection）、LC 2196 根据描述创建二叉树
