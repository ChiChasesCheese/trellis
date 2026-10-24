---
id: tlc-python-bisect-sorted-5-lis
node: python.bisect-sorted
type: qa
step: 5
---
## Q
**Python 工具箱｜用 `bisect_left` 写 `O(n log n)` 的最长递增子序列**

LC 300 最长递增子序列的 `tails` 数组里存什么？为什么用 `bisect_left`？如果题目是「非严格递增」应该换成什么？

## A
`tails[i]` = 长度为 `i+1` 的所有递增子序列里，**结尾元素的最小值**。`tails` 一定严格递增，所以能二分。

```python
from bisect import bisect_left
def length_of_lis(nums: list[int]) -> int:
    tails: list[int] = []
    for x in nums:
        i = bisect_left(tails, x)      # 第一个 >= x 的位置
        if i == len(tails):
            tails.append(x)            # x 比所有结尾都大：序列变长
        else:
            tails[i] = x               # 用更小的结尾替换，之后更容易接上
    return len(tails)
print(length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]))   # 4
print(length_of_lis([0, 1, 0, 3, 2, 3]))             # 4
print(length_of_lis([7, 7, 7, 7]))                   # 1
```

- 用 `bisect_left` 是因为**严格**递增：遇到相等的结尾就替换它，不延长。若写成 `bisect_right`，`[7,7,7,7]` 会得到 `4`，那是「非严格递增」的答案。
- `tails` 本身不是某个真实子序列，只有长度是对的；要还原序列需额外记录每个元素的前驱下标。
- 时间 `O(n log n)`，空间 `O(n)`；朴素 DP 是 `O(n^2)`。

非严格递增版本只需把 `bisect_left` 换成 `bisect_right`：`[7,7,7,7]` → `4`，`[1,3,2,2,5]` → `4`。

相关题：LC 354 俄罗斯套娃信封（先按宽升序、宽相同时高降序，再对高求 LIS）、LC 673 最长递增子序列的个数。
