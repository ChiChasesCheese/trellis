---
slug: magnetic-force-between-two-balls
---
## Q
**LC 1552 两球之间的磁力**｜Medium

`n` 个篮子位置，放 `m` 个球，使任意两球最小间距最大，返回这个最大的最小间距。

## A
**一句话。** 最大化最小值，二分答案：间距 `d` 可行则更小的也可行；判定时排序后贪心，能放就放。

```python
def max_distance(position, m):
    position.sort()

    def ok(d):                  # 相邻间距都 >= d 能否放下 m 个
        cnt, last = 1, position[0]
        for p in position[1:]:
            if p - last >= d:
                cnt, last = cnt + 1, p
        return cnt >= m

    lo, hi = 1, position[-1] - position[0]
    while lo < hi:              # 找最后一个可行的 d
        mid = (lo + hi + 1) // 2
        if ok(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo
```

**复杂度。** 时间 `O(n log n + n log U)`，空间 `O(1)`，`U` 为坐标跨度。

**易错点。**
- `mid = (lo + hi) // 2` 配 `lo = mid`：`hi = lo + 1` 时死循环，求最大要上取整。
- 忘了排序：贪心判定要求从左到右放。

**追问。**
- 为什么贪心判定对？：第一个球放最左最优，之后每个球放在最早满足间距的位置，给后面留的空间最多。
- 最小化最大值的反向题？：同样二分，判定换成「最多几段」，如 LC 410。

**同模式。** LC 875 爱吃香蕉的珂珂、LC 1011 在 D 天内送达包裹的能力、LC 2517 礼盒的最大甜蜜度
