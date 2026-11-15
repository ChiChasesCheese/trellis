---
slug: k-radius-subarray-averages
---
## Q
**LC 2090 半径为 k 的子数组平均值**｜Medium

整数数组 `nums` 和 `k`。对每个下标 `i`，求以 `i` 为中心、半径 `k` 的子数组（共 `2k + 1` 个数）的平均值，向下取整；不足 `2k + 1` 个数时为 `-1`。

## A
**一句话。** 前缀和：窗口 `[i - k, i + k]` 之和 = `pre[i + k + 1] - pre[i - k]`，除以 `2k + 1` 向下取整；两端不足的位置保持 `-1`。

```python
def get_averages(nums, k):
    n, w = len(nums), 2 * k + 1
    pre = [0] * (n + 1)
    for i, x in enumerate(nums):
        pre[i + 1] = pre[i] + x
    ans = [-1] * n
    for i in range(k, n - k):
        ans[i] = (pre[i + k + 1] - pre[i - k]) // w
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 窗口范围写成 `range(k, n - k + 1)`：`i + k + 1` 会越界，应是 `range(k, n - k)`。
- `k = 0`：窗口只有自己，平均值就是 `nums[i]`，公式自然成立。

**追问。**
- 想省掉 `pre` 数组？：滑动窗口，每步加进右端、减去左端，`O(1)` 空间。

**同模式。** LC 1004 最大连续1的个数 III、LC 424 替换后的最长重复字符、LC 209 长度最小的子数组、LC 643 子数组最大平均数 I
