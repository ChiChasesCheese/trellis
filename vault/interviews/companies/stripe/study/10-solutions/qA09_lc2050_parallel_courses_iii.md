# qA09 · LC 2050 并行课程 III（带权 DAG 最长路）

> `problems/qA09_lc2050_parallel_courses_iii/` · 3 个 part · LC Stripe tag 频率 44–67
> **主题：Kahn 拓扑 + 最早完成时间；n = 5·10^4 必须写成迭代。**

## 一句话题意

`n` 个任务，`relations` 是先修边，`time[i]` 是任务 i 的耗时。
所有无依赖的任务可以同时开始。求全部完成的最短总时间。

## 解题思路

### Part 1 — Kahn

```python
from collections import deque
def minimum_time(n, relations, time) -> int:
    g = [[] for _ in range(n)]; indeg = [0] * n
    for u, v in relations:                    # ★ relations 是 1-based，time 是 0-based
        g[u-1].append(v-1); indeg[v-1] += 1
    finish = [0] * n
    dq = deque()
    for i in range(n):
        if indeg[i] == 0: finish[i] = time[i]; dq.append(i)
    while dq:
        u = dq.popleft()
        for v in g[u]:
            finish[v] = max(finish[v], finish[u] + time[v])    # ★ 每次松弛都更新
            indeg[v] -= 1
            if indeg[v] == 0: dq.append(v)
    return max(finish)
```

O(n + m)。**递归 DFS 在 5·10^4 长的链上会爆栈 —— 写迭代。**

### Part 2 — 关键路径

返回一条最长链（1-based，按执行顺序）。
**确定性选择**：终点取 `finish` 最大的（平手取 id 最小），往回走时每步取
`finish` 最大的先修（平手取 id 最小）。
不变量：`sum(time[j-1] for j in path) == minimum_time(...)`。

### Part 3 — k 个工人（设计题）

最多 `k` 个任务同时跑。返回 `Slot(job, start, end)`，按 `(start, job)` 排。
**这是经典的 list scheduling 启发式 —— k 受限的调度是 NP-hard，
面试官要的是一个"好且确定"的方案 + 诚实说明它不总是最优。**

1. `tail[j] = time[j] + max(tail[s] for j → s)` —— 从 j 到任一汇点的最长链（在**反图**上跑 Part 1）。
   这是优先级：tail 长的更紧急。
2. 事件模拟：有空闲工人且有就绪任务时，启动 `tail` 最大（平手 id 最小）的；
   没有空闲工人（或没有就绪任务）时，把 `now` 跳到最早的结束时刻，退休那些任务并释放后继。
3. `k >= n`（或 ≥ DAG 的宽度）复现 Part 1；`k = 1` 给 `sum(time)`。任务不可抢占。

## 坑

1. **`relations` 是 1-based，`time` 是 0-based** —— 两个方向的 off-by-one 都是经典 bug。
2. 没有边 → `max(time)`；单任务 → `time[0]`。
3. **5·10^4 长的链**：递归 DFS 爆栈；答案可达 5·10^8。
4. 多个先修在同一时刻完成（平手）→ Part 2 的最小 id 规则。
5. **关键路径不一定经过耗时最长的那个单任务。**
6. Part 3：`k = 1` 必须等于 `sum(time)`；`k >= n` 必须等于 Part 1；
   任务绝不早于所有先修的 `end` 开始；任何时刻不超过 k 个重叠。

## 变体

- LC 1136（单位耗时）、LC 210（只要顺序）—— 同一个 Kahn 循环。
- q29 部署窗口：DAG 是隐式的（服务互相依赖），权重是窗口不是时长。
- "该给哪个任务提速？" → Part 2（**只有关键路径上的提速才会改变总时长**）。

## Code Core 节点

**`algorithms.topological`** · `algorithms.graph-traversal` · `toolbox.deque` ·
`algorithms.greedy`（list scheduling） · `performance.budget`（迭代 vs 递归）

## 自测清单

- [ ] 1-based / 0-based 的对齐（手算一个 3 节点的例子）
- [ ] 无边 / 单任务
- [ ] 5·10^4 长链（确认没爆栈）
- [ ] 同时刻完成的平手
- [ ] 关键路径不经过最长单任务的例子
- [ ] `k = 1` == `sum(time)`；`k >= n` == Part 1
- [ ] 任何时刻不超过 k 个重叠
