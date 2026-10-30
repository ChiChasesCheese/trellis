---
id: tlc-longest-increasing-subsequence-2-code
node: p2.longest-increasing-subsequence
type: qa
step: 2
---
## Q
**LC 300 最长递增子序列**｜写出 Python 实现

`nums` 是整数数组，`1 <= nums.length <= 2500`，`-10^4 <= nums[i] <= 10^4`。返回最长严格递增子序列的长度（子序列不要求连续）。要求 `O(n log n)`。

## A
**思路。** `tails[k]` 存长度为 `k+1` 的递增子序列的最小结尾，数组严格递增。对每个数 `x` 用 `bisect_left` 找第一个 `>= x` 的位置：位置在末尾就追加，否则替换，让该长度的结尾更小。最后 `tails` 的长度就是答案。

```python
from bisect import bisect_left


def length_of_lis(nums: list[int]) -> int:
    tails: list[int] = []                          # tails[k] = 长度为 k+1 的递增子序列的最小结尾
    for x in nums:
        i = bisect_left(tails, x)                  # 严格递增：第一个 >= x 的位置
        if i == len(tails):
            tails.append(x)                        # x 比所有结尾都大：最长长度 +1
        else:
            tails[i] = x                           # 让长度 i+1 的结尾变得更小，对后面更有利
    return len(tails)
```

运行：`[10,9,2,5,3,7,101,18]` → `4`；`[0,1,0,3,2,3]` → `4`；`[7,7,7,7,7,7,7]` → `1`；`[5]` → `1`；`[1,2,3,4]` → `4`；`[4,3,2,1]` → `1`。

**复杂度。** 时间 `O(n log n)`：`n` 次二分，每次 `O(log n)`；空间 `O(n)`（`tails` 最长为 `n`）。

**写法要点。** `bisect_left` 在有序列表上做二分，返回插入位置，不要自己手写二分；`i == len(tails)` 同时覆盖了空列表和"比所有结尾都大"；赋值 `tails[i] = x` 不会破坏有序性，因为 `tails[i-1] < x <= tails[i]`；写成 `from bisect import bisect_left` 比 `import bisect` 少一层属性查找。
