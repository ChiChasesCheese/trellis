---
slug: minimum-moves-to-pick-k-ones
---
## Q
**LC 3086 拾起 K 个 1 需要的最少行动次数**｜Hard

Alice 站在任选的下标上拾 `1`，每次行动可把某个 `0` 造成 `1`（至多 `maxChanges` 次），或把相邻的 `1` 与 `0` 交换。求恰好拾起 `k` 个 `1` 的最少行动次数。

## A
**一句话。** 先吃脚下及紧挨着的 `1`，再用造 `1` 换位（每个 `2` 步），不够的部分用中位数窗口挪已有的 `1`。

```python
def minimum_moves(nums, k, max_changes):
    # c：不用造 1 就能拿的连续 1（至多 3 个）
    runs = (len(list(g)) for v, g in groupby(nums) if v)
    c = min(max(runs, default=0), 3, k)
    if max_changes >= k - c:      # 剩下的全靠造 1，每个 2 步
        return max(c - 1, 0) + 2 * (k - c)

    need = k - max_changes        # 造 1 用满，其余挪已有的 1
    pos = [i for i, x in enumerate(nums) if x]
    pre = list(accumulate(pos, initial=0))

    def cost(l):                  # 窗口 pos[l:l+need] 向中位数靠拢
        r, m = l + need, l + need // 2
        left = pos[m] * (m - l) - (pre[m] - pre[l])
        right = pre[r] - pre[m+1] - pos[m] * (r - m - 1)
        return left + right

    best = min(map(cost, range(len(pos) - need + 1)))
    return 2 * max_changes + best
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- `c` 当成三格内 `1` 的个数：它必须是连续 `1` 的长度（封顶 3），`[1,0,1]`、`k=2`、`maxChanges=1` 得 `1`，应为 `2`。
- 不管 `maxChanges` 一律用窗口：例 1 得 `4`，应为 `3`，造 `1` 要先用满。
- `c` 不对 `k` 取最小：`k=1` 时答案应为 `0`。

**追问。**
- 为什么窗口站在中位数？：到一组点的距离和在中位数处最小。
- 同一数组查询很多个 `k`？：`pos`、`pre` 只建一次，每次重跑窗口。

**同模式。** LC 462 最少移动次数使数组元素相等 II、LC 1703 得到连续 K 个 1 的最少相邻交换次数、LC 296 最佳的碰头地点、LC 2448 使数组相等的最小开销
