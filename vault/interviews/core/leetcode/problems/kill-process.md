---
slug: kill-process
---
## Q
**LC 582 杀掉进程**｜Medium

进程 `pid[i]` 的父进程是 `ppid[i]`（根的父为 0）。杀掉进程 `kill` 时它的所有子孙也会被杀，返回被杀的全部进程（任意顺序）。

## A
**一句话。** 用 `ppid` 建「父 → 孩子」的邻接表，从 `kill` 出发 DFS 收集整棵子树。

```python
def kill_process(pid, ppid, kill):
    children = defaultdict(list)
    for c, p in zip(pid, ppid):
        children[p].append(c)
    ans = []

    def dfs(u):                # 杀掉 u 和它的全部子孙
        ans.append(u)
        for v in children[u]:
            dfs(v)

    dfs(kill)
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 对每个进程沿 `ppid` 往上找是否经过 `kill`：最坏 `O(n²)`。
- 邻接表方向建反：要从父找孩子，键是 `ppid`。

**追问。**
- 进程树很深？：改用 BFS 队列，避免递归过深。
- 频繁查询不同的 `kill`？：先做一次欧拉序，子树对应一段连续区间，直接切片返回。

**同模式。** LC 133 克隆图、LC 1376 通知所有员工所需的时间、LC 2368 受限条件下可到达节点的数目
