---
slug: zui-xiao-tiao-yue-ci-shu
---
## Q
**LCP 09 最小跳跃次数**｜Hard

`N` 个弹簧，小球从 `0` 号开始。按 `i` 号弹簧，小球可向右弹到 `i + jump[i]`（`>= N` 即弹出机器），或向左弹到 `0..i-1` 中任意一个。求弹出机器最少要按几次。例：`jump = [2,5,1,1,1,1]` → `3`。

## A
**一句话。** 无权图上按层 BFS，向左的边覆盖一段前缀，用只增不减的指针 `lo` 记录前缀扫到哪，每个下标只被向左扫到一次。

```python
def minimum_jump(jump):
    n = len(jump)
    seen = [False] * n
    seen[0] = True
    frontier, lo, steps = [0], 1, 0   # lo：下标 < lo 都已入队
    while frontier:
        steps += 1
        nxt = []
        for i in frontier:
            j = i + jump[i]
            if j >= n:          # 向右弹出机器
                return steps
            if not seen[j]:
                seen[j] = True
                nxt.append(j)
            while lo < i:       # 向左：只扫没扫过的一段
                if not seen[lo]:
                    seen[lo] = True
                    nxt.append(lo)
                lo += 1
        frontier = nxt
    return -1       # 一直向右弹总能出界，到不了这里
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 只往右跳：`[2,5,1,1,1,1]` 得 `5`，应为 `3`。
- 每个点把 `range(i)` 整段扫一遍：`10^6` 个 `1` 时要扫约 `5 × 10^11` 次，超时。
- 出队时才标记已访问：同一下标被多次加入下一层，重复工作成倍增加。

**追问。**
- 要输出路线？：入队时记 `parent[j] = i`，出界时沿 `parent` 回溯。
- 向左只能跳到 `[i - d, i - 1]`？：区间不再是前缀，单个 `lo` 不够，改用并查集「跳过已访问」。
- 向左免费、向右代价 1？：代价只有 0 和 1，用双端队列的 0-1 BFS。

**同模式。** LC 1345 跳跃游戏 IV、LC 1871 跳跃游戏 VII、LC 2612 最少翻转操作数、LC 45 跳跃游戏 II
