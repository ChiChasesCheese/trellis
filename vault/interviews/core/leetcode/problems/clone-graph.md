---
slug: clone-graph
---
## Q
**LC 133 克隆图**｜Medium

给无向连通图中一个节点，返回整张图的深拷贝（节点含 `val` 和 `neighbors`）。

## A
**一句话。** 递归 DFS，哈希表 `copies` 既当 visited 又存「原节点 → 拷贝」，环在这里断开。

```python
def clone_graph(node):
    copies = {}                    # 原节点 -> 拷贝

    def dfs(cur):
        if cur in copies:
            return copies[cur]
        copies[cur] = clone = Node(cur.val)   # 先登记再递归
        clone.neighbors = [dfs(nb) for nb in cur.neighbors]
        return clone

    return dfs(node) if node else None
```

**复杂度。** 时间 `O(V + E)`，空间 `O(V)`。

**易错点。**
- 没有映射、每次都新建：`[[2],[1]]` 互为邻居，递归无限，抛 `RecursionError`。
- 先递归后登记：环上节点会无限递归，登记必须在递归邻居之前。
- 忘记判空：入参 `None` 时 `node.val` 报 `AttributeError`。

**追问。**
- BFS 为什么要在入队前登记？：出队才登记会让同一节点被多次入队，建出多份拷贝。
- 链状图上千节点会怎样？：超出递归上限，改用 BFS 或调高 `setrecursionlimit`。

**同模式。** LC 138 随机链表的复制、LC 207 课程表、LC 797 所有可能的路径、LC 399 除法求值
