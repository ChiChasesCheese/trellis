---
slug: employee-importance
---
## Q
**LC 690 员工的重要性**｜Medium

每个员工有唯一 `id`、重要度 `importance` 和直接下属的 `id` 列表 `subordinates`。给定员工列表和某个 `id`，返回该员工及其所有直接、间接下属的重要度之和。

## A
**一句话。** 先建 `id` 到员工的哈希表，再从给定员工出发 DFS 累加整棵下属树。

```python
def get_importance(employees, id):
    by_id = {e.id: e for e in employees}
    def dfs(i):
        e = by_id[i]
        total = e.importance
        for sub in e.subordinates:
            total += dfs(sub)        # 下属的下属也要算
        return total
    return dfs(id)
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 只加直接下属：间接下属同样计入。
- 在列表里按 `id` 线性查找：每次 `O(n)`，总共 `O(n^2)`，先建哈希表。

**追问。**
- 不递归怎么做？：栈或队列装待处理的 `id`，弹出时累加并把下属压进去。
- 汇报关系出现环会怎样？：递归死循环，需要 `seen` 集合。

**同模式。** LC 559 N 叉树的最大深度、LC 1376 通知所有员工所需的时间、LC 429 N 叉树的层序遍历
