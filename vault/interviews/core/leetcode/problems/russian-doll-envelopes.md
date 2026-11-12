---
slug: russian-doll-envelopes
---
## Q
**LC 354 俄罗斯套娃信封问题**｜Hard

信封 `[w, h]` 宽和高都严格小于另一个才能放进去（不许旋转）。求最多能套几层。

## A
**一句话。** 宽升序、同宽高降序排序，再对高度求严格最长递增子序列（LIS）。

```python
def max_envelopes(envelopes):
    # 同宽高降序：同宽的不可能同时进严格递增序列
    envelopes.sort(key=lambda e: (e[0], -e[1]))
    tails = []           # tails[k]：长 k+1 的 LIS 的最小结尾
    for _, h in envelopes:
        k = bisect_left(tails, h)    # 严格递增：相等要替换
        if k == len(tails):
            tails.append(h)
        else:
            tails[k] = h
    return len(tails)
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 同宽时高度升序：`[[1,3],[1,4],[1,5]]` 得 `3`，应为 `1`。
- `bisect_right` 代替 `bisect_left`：`[[1,1],[2,1]]` 得 `2`，应为 `1`。

**追问。**
- 允许旋转？：先把每个信封规范成 `w <= h`，其余不变。
- 为什么 `tails` 里不是真实的链？：它只记每种长度的最小结尾，长度对，内容不一定是一条合法链。

**同模式。** LC 300 最长递增子序列、LC 646 最长数对链、LC 673 最长递增子序列的个数、LC 1626 无矛盾的最佳球队
