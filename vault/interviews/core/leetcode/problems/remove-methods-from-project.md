---
slug: remove-methods-from-project
---
## Q
**LC 3310 移除可疑的方法**｜Medium

`n` 个方法，`[a, b]` 表示 `a` 调用 `b`。方法 `k` 及它直接或间接调用的都是可疑方法；若有组外方法调用组内方法，就一个都不删，否则全删。返回剩下的方法。

## A
**一句话。** 从 `k` 出发 BFS 标出可疑集合，再扫一遍边：存在「组外 → 组内」的调用就全部保留，否则删掉可疑集合。

```python
def remaining_methods(n, k, invocations):
    g = [[] for _ in range(n)]
    for a, b in invocations:
        g[a].append(b)
    bad = [False] * n
    bad[k] = True
    q = deque([k])
    while q:                    # k 能调到的都可疑
        u = q.popleft()
        for v in g[u]:
            if not bad[v]:
                bad[v] = True
                q.append(v)
    if any(not bad[a] and bad[b] for a, b in invocations):
        return list(range(n))   # 组外有人调用组内
    return [i for i in range(n) if not bad[i]]
```

**复杂度。** 时间 `O(n + m)`，空间 `O(n + m)`。

**易错点。**
- 沿反向边扩展：可疑的是 `k` 调用的方法，不是调用 `k` 的方法。
- 递归 DFS：调用链可长达 `10^5`，Python 默认递归深度不够，用 BFS 或显式栈。

**追问。**
- 组内方法调用组外方法要紧吗？：不要紧，删除只怕组内被外部依赖。
- 多个 bug 方法？：多源 BFS，其余判断不变。

**同模式。** LC 200 岛屿数量、LC 841 钥匙和房间、LC 207 课程表
