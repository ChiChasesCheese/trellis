---
slug: shortest-subarray-to-be-removed-to-make-array-sorted
---
## Q
**LC 1574 删除最短的子数组使剩余数组有序**｜Medium

删除 `arr` 的一个连续子数组（可为空），使剩下的元素非递减，求最短删除长度。

## A
**一句话。** 保留非递减的前缀和后缀，前缀末尾不超过后缀开头；双指针枚举前缀，后缀起点单调右移。

```python
def find_length_of_shortest_subarray(arr):
    n = len(arr)
    r = n - 1
    while r > 0 and arr[r - 1] <= arr[r]:   # 最长非降后缀的起点
        r -= 1
    if r == 0:
        return 0
    ans = r                                 # 只留后缀
    for l in range(n):
        if l > 0 and arr[l - 1] > arr[l]:
            break                           # 前缀不再有序
        while r < n and arr[r] < arr[l]:
            r += 1
        ans = min(ans, r - l - 1)           # 删 arr[l+1:r]
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 只考虑删前缀或删后缀：`[1,2,3,10,4,2,3,5]` 的最优解夹在中间。
- 前缀乱序后不 `break`：`[5,0,0,5,2]` 会返回 `0`，应为 `4`。
- 把 `r` 限制在 `n - 1`：`r = n`（后缀为空）也合法，对应删到末尾。

**追问。**
- 要返回具体区间？：记录取得最小值时的 `l + 1` 与 `r`。
- 删除的元素可以不连续呢？：求最长非递减子序列，答案 `n - LIS`。

**同模式。** LC 209 长度最小的子数组、LC 845 数组中的最长山脉、LC 581 最短无序连续子数组、LC 300 最长递增子序列
