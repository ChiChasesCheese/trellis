---
slug: amazon-lowest-common-manager
---
## Q
**组织架构的最低共同上级**｜Medium

组织架构 `{经理: [直属下属]}` 是一棵树。给两名员工，返回他们的最低共同上级（本人也算自己的上级）；有人不在架构里返回 `None`。组织可能很深，不能递归。

## A
**一句话。** 一次 BFS 建父指针和深度，深的人先上爬到同一深度，再两人一起上爬，第一次相遇就是答案。

```python
def lowest_common_manager(reports, a, b):
    subs = {s for v in reports.values() for s in v}
    root = next(m for m in reports if m not in subs)
    parent, depth = {root: None}, {root: 0}
    q = deque([root])
    while q:                  # BFS 建父指针，不怕深
        u = q.popleft()
        for v in reports.get(u, []):
            parent[v], depth[v] = u, depth[u] + 1
            q.append(v)
    if a not in depth or b not in depth:
        return None
    while depth[a] > depth[b]:
        a = parent[a]
    while depth[b] > depth[a]:
        b = parent[b]
    while a != b:             # 同深度后一起往上
        a, b = parent[a], parent[b]
    return a
```

**复杂度。** 时间建表 `O(n)`、每次查询 `O(树高)`，空间 `O(n)`。

**易错点。**
- 不先对齐深度就一起上爬：两人一快一慢永远错开，最后一起走到 `None`。
- 根取字典第一个键：根是唯一不当别人下属的经理，不一定排第一。

**追问。**
- 查询很多？：倍增表 `up[k][v]`，`O(n log n)` 预处理，每次查询 `O(log n)`。
- `k` 个员工的共同上级？：LCA 满足结合律，逐个折叠 `lca(lca(a, b), c)`。

**同模式。** LC 236 二叉树的最近公共祖先、LC 1650 二叉树的最近公共祖先 III、LC 1123 最深叶节点的最近公共祖先、LC 1483 树节点的第 K 个祖先
