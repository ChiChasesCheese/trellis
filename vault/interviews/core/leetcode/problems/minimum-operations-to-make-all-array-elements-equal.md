---
slug: minimum-operations-to-make-all-array-elements-equal
---
## Q
**LC 2602 使数组元素全部相等的最少操作次数**｜Medium

给正整数数组 `nums` 和查询数组 `queries`。对每个 `queries[i]`，每次操作可把任意元素加 1 或减 1，求把 `nums` 所有元素变成 `queries[i]` 的最少操作数（各查询互相独立）。

## A
**一句话。** 排序加前缀和，每个查询值二分找到分界点，小于它的部分把差补上、大于它的部分把差减掉。

```python
def min_operations(nums, queries):
    nums.sort()
    pre = list(accumulate(nums, initial=0))
    n, res = len(nums), []
    for q in queries:
        i = bisect_left(nums, q)       # 前 i 个比 q 小
        low = q * i - pre[i]           # 小的要加到 q
        high = pre[n] - pre[i] - q * (n - i)  # 大的要减到 q
        res.append(low + high)
    return res
```

**复杂度。** 时间 `O((n + m) log n)`，空间 `O(n)`。

**易错点。**
- 每个查询都遍历整个数组：`O(nm)` 会超时，要排序加前缀和。
- 前缀和数组不带头部 0：`pre[i]` 表示前 `i` 个数之和，需要 `initial=0` 才对齐。
- 小的一段写成 `pre[i] - q * i`：小元素要加到 `q`，差为 `q * i - pre[i]`，写反得负数。

**追问。**
- 为什么最优是各自对齐到 `q`？：每个元素到 `q` 的最少步数就是 `|x - q|`，各元素互相独立。
- 若要所有元素变成同一个任意值呢？：最优值是中位数（LC 462）。

**同模式。** LC 1685 有序数组中差绝对值之和、LC 462 最小操作次数使数组元素相等 II、LC 1658 将 x 减到 0 的最小操作数
