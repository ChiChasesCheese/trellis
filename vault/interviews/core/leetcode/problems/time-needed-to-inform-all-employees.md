---
slug: time-needed-to-inform-all-employees
---
## Q
**LC 1376 通知所有员工所需的时间**｜Medium

`manager[i]` 是 `i` 的直属经理，负责人 `headID`；员工 `i` 花 `informTime[i]` 分钟通知所有直属下属。求消息传到所有人的时间。

## A
**一句话。** 反转成「经理 → 下属」的树，答案是根到叶路径上 `informTime` 之和的最大值，递归求子树耗时。

```python
def num_of_minutes(n, head_id, manager, inform_time):
    subs = [[] for _ in range(n)]
    for e, m in enumerate(manager):
        if m >= 0:
            subs[m].append(e)

    def dfs(u):                  # u 收到后传完整棵子树要多久
        return inform_time[u] + max(
            (dfs(v) for v in subs[u]), default=0)

    return dfs(head_id)
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 把所有 `informTime` 相加：同一经理的下属是同时通知的，取最大路径而不是总和。
- 链状公司深 `10^5`：递归会超出默认深度，调大递归上限或改用栈。

**追问。**
- 不建树？：对每个员工沿 `manager` 往上走到根，记忆化每个人的到达时间。
- 为什么叶子 `informTime` 是 `0`？：没有下属的人不用通知别人，题目保证为 `0`。

**同模式。** LC 104 二叉树的最大深度、LC 559 N 叉树的最大深度
