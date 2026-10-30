---
id: tlc-maximum-subarray-sum-with-one-deletion-2-code
node: p5.maximum-subarray-sum-with-one-deletion
type: qa
step: 2
---
## Q
**LC 1186 删除一次得到子数组最大和**｜写出 Python 实现

整数数组 `arr`（长度 `1..10^5`，元素 `-10^4..10^4`）。选一个非空连续子数组，可以从中删掉至多一个元素（删后仍非空），求能得到的最大元素和。要求 `O(n)`。

## A
**思路。** `keep` 是以当前位置结尾、没有删除过的最大子数组和（标准 Kadane）；`skip` 是以当前位置结尾、至多删除过一个元素的最大和。处理新元素 `x` 时，`skip` 取 `skip + x`（延续）、`keep`（删掉 `x` 本身，沿用上一格没删过的最优）、`x`（重新开始）三者最大；`keep` 取 `max(keep, 0) + x`。答案是所有位置的 `keep` 和 `skip` 的最大值。

```python
def maximum_sum(arr: list[int]) -> int:
    keep = skip = best = arr[0]    # keep：以 i 结尾、没删过；skip：以 i 结尾、至多删过一个
    for x in arr[1:]:
        # skip 三选一：延续（含已删过的）/ 删掉 x（保留到 i-1 为止的 keep）/ 从 x 重新开始
        skip, keep = max(skip + x, keep, x), max(keep, 0) + x
        best = max(best, keep, skip)
    return best
```

运行：`arr=[1,-2,0,3]` → `4`，`arr=[1,-2,-2,3]` → `3`，`arr=[-1,-1,-1,-1]` → `-1`，`arr=[1,-4,1]` → `2`，`arr=[5]` → `5`。

**复杂度。** 时间 `O(n)`，一遍扫描；空间 `O(1)`，只保留两个状态变量和答案。

**写法要点。** 元组同时赋值 `skip, keep = ..., ...`：右边先全部求值，保证 `skip` 用到的是上一格的 `keep`；`best = skip = keep = arr[0]` 把初始状态统一；`max(a, b, c)` 一次比较三项，比嵌套 `max` 清晰；`arr[1:]` 会复制一份数组（`O(n)` 空间），如果要严格 `O(1)` 空间，用 `itertools.islice(arr, 1, None)` 或下标循环。
