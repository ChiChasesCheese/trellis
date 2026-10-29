---
id: tlc-zui-xiao-tiao-yue-ci-shu-5-alt
node: a.zui-xiao-tiao-yue-ci-shu
type: qa
step: 5
---
## Q
**LCP 09 最小跳跃次数**｜另一种解法

不用前缀指针，换成「跳过已访问」的并查集写 BFS 怎么写？它适合什么情况，和指针写法怎么选？

## A
**思路。** `nxt[x]` 指向 `x` 及其右边第一个**未访问**的下标（`n` 作哨兵）。访问 `x` 后令 `nxt[x] = x + 1`；`find` 带路径压缩，跳过一整段已访问的点。向左扫 `0..i-1` 时从 `find(0)` 开始，每次 `find(x + 1)`，只碰到未访问的点。

```python
from collections import deque


def minimum_jump_dsu(jump: list[int]) -> int:
    n = len(jump)
    nxt = list(range(n + 1))             # nxt[x]：x 及右边第一个未访问的下标
    def find(x: int) -> int:
        while nxt[x] != x:
            nxt[x] = nxt[nxt[x]]         # 路径减半
            x = nxt[x]
        return x
    dist = [0] * n
    nxt[0] = 1                           # 0 号已访问
    queue = deque([0])
    while queue:
        i = queue.popleft()
        j = i + jump[i]
        if j >= n:
            return dist[i] + 1
        targets = [j] if find(j) == j else []
        x = find(0)
        while x < i:                     # 只遍历 0..i-1 中还没访问的
            targets.append(x)
            x = find(x + 1)
        for t in targets:
            if find(t) == t:
                nxt[t] = t + 1           # 标记已访问：并到右边
                dist[t] = dist[i] + 1
                queue.append(t)
    return -1
```

运行：`[2,5,1,1,1,1]` → `3`，`10^6` 个 `1` → `1000000`。

**取舍。** 向左的边是前缀时，单个 `lo` 指针最简单，严格 `O(n)`；并查集版本对**任意区间** `[l, r]` 都适用（向左只能跳 `d` 格、LC 2612 这类「一次可到一段区间」的题），代价是多一个 `find`，均摊接近 `O(1)`。`n` 只有几千时，直接枚举 `range(i)` 的 `O(n^2)` BFS 也能过，最容易写对。
