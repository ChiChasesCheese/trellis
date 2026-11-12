---
slug: longest-increasing-subsequence
---
## Q
**LC 300 最长递增子序列**｜Medium

求整数数组中最长严格递增子序列（不要求连续）的长度。

## A
**一句话。** 耐心排序（patience sorting）：`tails[k]` 记长度 `k+1` 的递增子序列的最小结尾，二分替换或追加。

```python
def length_of_lis(nums):
    tails = []                    # tails[k]：长度 k+1 的最小结尾
    for x in nums:
        i = bisect_left(tails, x)     # 第一个 >= x 的位置
        if i == len(tails):
            tails.append(x)       # 比所有结尾都大：长度加一
        else:
            tails[i] = x          # 让该长度的结尾更小
    return len(tails)
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 严格递增误用 `bisect_right`：`[7,7,7,7,7,7,7]` 得 `7`，应为 `1`。
- 把 `tails` 当真实子序列：`[4,5,1]` 得 `tails=[1,5]`，但 `1` 在 `5` 后面，只有长度可信。

**追问。**
- 允许相等（非严格递增）？：换成 `bisect_right`。
- 要还原序列？：记每个元素的前驱下标，从末尾回溯。
- 二维的套娃信封（LC 354）？：宽度升序、同宽高度降序，再对高度求严格 LIS。

**同模式。** LC 354 俄罗斯套娃信封问题、LC 673 最长递增子序列的个数、LC 646 最长数对链、LC 1143 最长公共子序列
