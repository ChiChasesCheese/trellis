---
id: tlc-longest-increasing-subsequence-4-followup
node: p2.longest-increasing-subsequence
type: qa
step: 4
---
## Q
**LC 300 最长递增子序列**｜追问

面试官接着问：（1）输出一条最长的递增子序列本身？（2）允许相等（最长非递减子序列）怎么改？（3）二维的俄罗斯套娃信封（LC 354）怎么转化成 LIS？

## A
1. **输出序列**：除了 `tails` 的值，再记录每个位置当前对应的原数组下标 `tail_idx`，以及每个元素接在谁后面 `prev`。结束后从最后一个长度的下标沿 `prev` 回溯。

```python
from bisect import bisect_left


def lis_sequence(nums: list[int]) -> list[int]:
    tails: list[int] = []          # 结尾值
    tail_idx: list[int] = []       # 结尾对应的下标
    prev = [-1] * len(nums)        # prev[i] = 以 i 结尾的最长序列里 i 的前一个下标
    for i, x in enumerate(nums):
        k = bisect_left(tails, x)
        if k == len(tails):
            tails.append(x)
            tail_idx.append(i)
        else:
            tails[k] = x
            tail_idx[k] = i
        prev[i] = tail_idx[k - 1] if k else -1
    seq, i = [], tail_idx[-1]
    while i != -1:
        seq.append(nums[i])
        i = prev[i]
    return seq[::-1]
```

`lis_sequence([10,9,2,5,3,7,101,18])` → `[2, 3, 7, 18]`（长度 `4`，和 `[2,3,7,101]` 同样合法）。
2. **允许相等**：把 `bisect_left` 换成 `bisect_right`，等于在 `x` 后面插入，相等的数也能接上。`[7,7,7,7,7,7,7]` → `7`，`[0,1,0,3,2,3]` → `4`。
3. **信封嵌套**：先按宽度升序排序，宽度相同按高度**降序**，再对高度序列求严格 LIS。同宽的信封高度降序，就不会有两个同宽信封被串进同一条递增链。

```python
def max_envelopes(envelopes: list[list[int]]) -> int:
    envelopes.sort(key=lambda e: (e[0], -e[1]))
    tails: list[int] = []
    for _, h in envelopes:
        i = bisect_left(tails, h)
        if i == len(tails):
            tails.append(h)
        else:
            tails[i] = h
    return len(tails)
```

`max_envelopes([[5,4],[6,4],[6,7],[2,3]])` → `3`。

**Python 提醒**：`bisect` 系列函数不检查列表是否有序，对无序列表调用也不报错、只是结果无意义；`tails` 的有序性要靠算法本身保证。
