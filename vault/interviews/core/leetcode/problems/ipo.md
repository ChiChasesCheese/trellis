---
slug: ipo
---
## Q
**LC 502 IPO**｜Hard

初始资本 `w`，最多做 `k` 个项目，项目 `i` 需要资本 `capital[i]`、赚 `profits[i]`，求最终最大资本。

## A
**一句话。** 按资本排序，每轮把做得起的项目利润放进大根堆，取利润最大的做，重复 `k` 轮。

```python
def find_maximized_capital(k, w, profits, capital):
    projects = sorted(zip(capital, profits))
    afford = []     # 做得起的利润（取负，大根堆）
    i = 0
    for _ in range(k):
        while i < len(projects) and projects[i][0] <= w:
            heapq.heappush(afford, -projects[i][1])
            i += 1
        if not afford:      # 做不起，资本不会再涨
            break
        w -= heapq.heappop(afford)
    return w
```

**复杂度。** 时间 `O(n log n + k log n)`，空间 `O(n)`。

**易错点。**
- 选资本要求最低的项目而不是利润最大的：`k=2, w=0, [1,2,3], [0,1,1]` 得 `3`，应为 `4`。
- 堆为空不 `break`：`heappop` 空堆抛 `IndexError`。
- 只在循环前入堆一次：每做完一个项目资本变大，要重新推进指针，示例一得 `1`，应为 `4`。

**追问。**
- 为什么贪心成立？：做利润最大的项目资本涨得最多，解锁的项目只多不少。
- 为什么不能直接按利润排序？：利润大但做不起的项目要等资本够了才能选，所以要按资本分批入堆。

**同模式。** LC 215 数组中的第 K 个最大元素、LC 295 数据流的中位数、LC 373 查找和最小的 K 对数字、LC 871 最低加油次数
