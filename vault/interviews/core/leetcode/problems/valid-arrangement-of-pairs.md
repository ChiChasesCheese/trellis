---
slug: valid-arrangement-of-pairs
---
## Q
**LC 2097 合法重新排列数对**｜Hard

数对 `[start, end]` 看成有向边，重新排列使每个数对的 `start` 等于前一个的 `end`。保证有解，返回任意一个排列。

## A
**一句话。** 用掉每条边恰好一次就是有向图的欧拉路径：起点选出度比入度多 1 的点（没有就任取），Hierholzer 后序收点再反转。

**图解。** `11` 出度比入度多 1，是起点；一笔画 `11→9→4→5→1` 用完全部边。

```mermaid
flowchart TB
    a(("11")) -->|"[11,9]"| b(("9"))
    b -->|"[9,4]"| c(("4"))
    c -->|"[4,5]"| d(("5"))
    d -->|"[5,1]"| e(("1"))
```

```python
def valid_arrangement(pairs):
    g = defaultdict(list)
    deg = defaultdict(int)         # 出度 - 入度
    for a, b in pairs:
        g[a].append(b)
        deg[a] += 1
        deg[b] -= 1
    start = next((x for x in deg if deg[x] == 1),
                 pairs[0][0])
    path = []
    def dfs(u):                    # Hierholzer：走过就删边
        while g[u]:
            dfs(g[u].pop())
        path.append(u)             # 出边用完才入栈
    dfs(start)
    path.reverse()
    return [[path[i], path[i + 1]]
            for i in range(len(path) - 1)]
```

**复杂度。** 时间 `O(m)`，空间 `O(m)`。

**易错点。**
- 进入点时就记录（先序）：遇到死胡同会把子环插错位置，必须出边用完后再记，最后反转。
- 递归深度可达 `10^5`：CPython 要调高递归上限或改成显式栈。

**追问。**
- 存在欧拉路径的条件？：弱连通，且要么所有点入度等于出度（欧拉回路），要么恰有一个点出度多 1、一个点入度多 1。
- 无向图呢？：奇度点为 0 或 2 个，删边时要同时删掉反向那条。

**同模式。** LC 332 重新安排行程、LC 753 破解保险箱
