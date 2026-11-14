---
slug: maximum-coins-from-k-consecutive-bags
---
## Q
**LC 3413 收集连续 K 个袋子可以获得的最多硬币数量**｜Medium

数轴上不相交区间 `[l, r, c]` 表示 `l..r` 每格 `c` 枚硬币，取连续 `k` 格，求最多硬币数。坐标、`k` 到 `10^9`。

## A
**一句话。** 窗口和是起点的分段线性函数，最优窗口一定有一端贴着某段端点；按段做滑窗算「右端对齐某段右端」，再把坐标镜像算一遍「左端对齐左端」。

```python
def maximum_coins(coins, k):
    def right_aligned(segs):    # 窗口右端对齐某段右端
        ans = cover = i = 0
        for l, r, c in segs:
            cover += (r - l + 1) * c
            while segs[i][1] < r - k + 1:   # 整段滑出
                sl, sr, sc = segs[i]
                cover -= (sr - sl + 1) * sc
                i += 1
            sl, _, sc = segs[i]             # 左端段可能露一截
            out = max(0, r - k + 1 - sl) * sc
            ans = max(ans, cover - out)
        return ans

    coins.sort()
    mirror = [(-r, -l, c) for l, r, c in reversed(coins)]
    return max(right_aligned(coins), right_aligned(mirror))
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 只做右端对齐：硬币密度不同，最优窗口可能是左端贴着某段左端，要镜像再做一遍。
- 露出的部分忘乘 `c`：这一截要按那一段的密度扣。

**追问。**
- 为什么端点一定对齐？：窗口平移一格，和的变化量只在端点跨过段边界时改变，线性函数的最大值在断点取到。
- 每格硬币都是 1（LC 2271）？：密度相同，只做一个方向即可。

**同模式。** LC 3 无重复字符的最长子串、LC 2271 毯子覆盖的最多白色砖块数
