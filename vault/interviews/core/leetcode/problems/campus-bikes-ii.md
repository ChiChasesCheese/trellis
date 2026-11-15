---
slug: campus-bikes-ii
---
## Q
**LC 1066 校园自行车分配 II**｜Medium

`n` 个工人、`m` 辆自行车（`n ≤ m ≤ 10`）在二维网格上。给每个工人分一辆不同的车，使工人与分到的车的曼哈顿距离之和最小，返回最小和。

## A
**一句话。** 状态压缩 DP：`f[mask]` 是用掉车集合 `mask` 时的最小总距离，已分配的工人数就是 `mask` 的位数，依次给下一个工人选车。

```python
def assign_bikes(workers, bikes):
    n, m = len(workers), len(bikes)
    f = [inf] * (1 << m)             # f[mask]：已用车集合为 mask
    f[0] = 0
    for mask in range(1 << m):
        i = mask.bit_count()         # 前 i 个工人已分配
        if i >= n or f[mask] == inf:
            continue
        for j in range(m):
            if mask >> j & 1:
                continue
            d = (abs(workers[i][0] - bikes[j][0])
                 + abs(workers[i][1] - bikes[j][1]))
            nm = mask | 1 << j
            f[nm] = min(f[nm], f[mask] + d)
    return min(f[mask] for mask in range(1 << m)
               if mask.bit_count() == n)
```

**复杂度。** 时间 `O(2^m · m)`，空间 `O(2^m)`。

**易错点。**
- 贪心每个工人选最近的车：先到先得会让后面的工人更差，必须全局最优。
- 答案取 `f[(1<<m)-1]`：车比工人多，答案是所有恰有 `n` 位的 `mask` 里的最小值。
- 额外维护工人下标：位数 `popcount(mask)` 已经给出下一个工人，不需要再多一维。

**追问。**
- 为什么能省掉工人这一维？：工人按固定顺序分配，已用车数就是已分配工人数。
- 还有别的解法吗？：最小费用二分图匹配（匈牙利算法 / 费用流），`n`、`m` 大时才需要。

**同模式。** LC 1879 两个数组最小的异或值之和、LC 2172 数组的最大与和、LC 1349 参加考试的最大学生数
