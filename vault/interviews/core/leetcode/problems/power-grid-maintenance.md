---
slug: power-grid-maintenance
---
## Q
**LC 3607 电网维护**｜Medium

`c` 个电站由固定的无向连接组成电网。查询 `[1, x]`：`x` 在线返回 `x`，否则返回同分量中编号最小的在线电站，没有返回 `-1`；`[2, x]`：`x` 离线。

## A
**一句话。** 离线不改变连通性：并查集先定分量，每个分量一个小根堆；离线只打标记，查询时从堆顶懒删除离线的电站。

```python
def process_queries(c, connections, queries):
    fa = list(range(c + 1))

    def find(x):
        while fa[x] != x:
            fa[x] = fa[fa[x]]
            x = fa[x]
        return x

    for a, b in connections:
        fa[find(a)] = find(b)
    heaps = defaultdict(list)
    for x in range(1, c + 1):     # 按编号递增加入，本身就是堆
        heaps[find(x)].append(x)
    off = [False] * (c + 1)
    ans = []
    for t, x in queries:
        if t == 2:
            off[x] = True         # 只打标记
        elif not off[x]:
            ans.append(x)
        else:
            h = heaps[find(x)]
            while h and off[h[0]]:
                heappop(h)        # 懒删除
            ans.append(h[0] if h else -1)
    return ans
```

**复杂度。** 时间 `O((c + q) log c)`，空间 `O(c)`。

**易错点。**
- 离线时去堆里找它删掉：堆不支持按值删除，`O(c)`；只打标记，用到堆顶时再弹。
- 查询时没先看 `x` 自己是否在线：在线就直接返回 `x`，不是最小编号。

**追问。**
- 不用堆？：倒着处理查询，把离线变成上线，每个分量维护最小在线编号；或每个分量一个有序集合。
- 电站可以重新上线？：懒删除不够用了，改用有序集合按值增删。

**同模式。** LC 684 冗余连接、LC 1319 连通网络的操作次数、LC 2349 设计数字容器系统
