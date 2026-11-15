---
slug: minimize-max-distance-to-gas-station
---
## Q
**LC 774 最小化去加油站的最大距离**｜Hard

`stations` 是升序排列的加油站位置。再新建 `k` 个加油站（位置可为任意实数），使相邻加油站的最大距离最小，返回这个最小值（误差 `1e-6` 内）。

## A
**一句话。** 对答案 `D` 实数二分：间隔 `g` 至少要新增 `⌈g/D⌉-1` 个站，总数 `≤ k` 就说明 `D` 可行，缩小 `D`。

```python
def min_max_gas_dist(stations, k):
    gaps = [b - a for a, b in pairwise(stations)]
    lo, hi = 0, max(gaps)
    for _ in range(60):             # 实数二分：固定轮数
        mid = (lo + hi) / 2
        # 间隔 g 需新增 ⌈g/mid⌉-1 个站，这里取 int(g/mid)
        need = sum(int(g / mid) for g in gaps)
        if need <= k:
            hi = mid                # 够用：试更小的最大距离
        else:
            lo = mid
    return hi
```

**复杂度。** 时间 `O(n log(W/ε))`，空间 `O(n)`。

**易错点。**
- 整数二分：答案是实数，用 `lo + 1 < hi` 会提前停止，应固定轮数或比较精度。
- 需要新增站数写成 `⌈g/D⌉`：区间 `g` 切成 `⌈g/D⌉` 段只需 `⌈g/D⌉-1` 个站。

**追问。**
- 为什么能二分？：`D` 越大需要的站越少，是单调的。
- 能不能用堆？：每次给当前最大的段加一个站，要 `O(k log n)`，`k` 很大时太慢。

**同模式。** LC 410 分割数组的最大值、LC 875 爱吃香蕉的珂珂、LC 1011 在 D 天内送达包裹的能力
