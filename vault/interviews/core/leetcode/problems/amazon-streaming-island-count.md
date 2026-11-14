---
slug: amazon-streaming-island-count
---
## Q
**逐行流式网格的岛屿数与最大面积**｜Hard

0/1 网格一行一行到达，内存只够 `O(列数)`。读完全部行后返回岛屿数和最大岛屿面积（四连通）。

## A
**一句话。** 只留上一行每格的标签，新陆地只连左边和正上方，用并查集合并并累加面积；一个块在新一行里不再出现就不会再长，当场结算并删掉。

```python
def stream_islands(rows):
    parent, area = {}, {}     # 只存还碰到上一行的块
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    prev, nid, done, best = [], 0, 0, 0
    for row in rows:
        cur = [0] * len(row)
        for c, v in enumerate(row):
            if not v:
                continue
            nid += 1
            cur[c] = parent[nid] = nid
            area[nid] = 1
            up = prev[c] if prev else 0
            left = cur[c - 1] if c else 0
            for o in (up, left):
                if o:
                    a, b = find(nid), find(o)
                    if a != b:
                        parent[a] = b
                        area[b] += area.pop(a)
        cur = [find(x) if x else 0 for x in cur]
        alive = set(cur)
        for r in [r for r in area if r not in alive]:
            done += 1         # 本行没碰到：再也长不大
            best = max(best, area.pop(r))
        parent = {r: r for r in alive if r}  # 丢掉旧标签
        prev = cur
    return done + len(area), max([best, *area.values()])
```

**复杂度。** 时间 `O(行数 × 列数 × α)`，空间 `O(列数)`。

**易错点。**
- 块还碰到最新一行就结算：U 形的两条竖臂在最后一行才连上，会被数成两个岛。
- 每行不压缩旧标签：`parent` 随行数增长，内存不再是 `O(列数)`。

**追问。**
- 每读一行就要报当前岛数？：`done + len(area)` 就是已读部分的岛数，但之后的行可能把它们合并，要先和面试官说清语义。
- 和 LC 305 什么关系？：同样是并查集增量合并；这里多了「块不再出现就结算、删除」来封住内存。

**同模式。** LC 200 岛屿数量、LC 695 岛屿的最大面积、LC 305 岛屿数量 II、LC 547 省份数量
