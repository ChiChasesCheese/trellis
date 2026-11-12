---
slug: minimum-size-subarray-sum
---
## Q
**LC 209 长度最小的子数组**｜Medium

给正整数数组 `nums` 和 `target`，求和 `>= target` 的最短连续子数组的长度，不存在返回 `0`。

## A
**一句话。** 可变长滑动窗口：和够了就一路缩左端，每缩一步都是候选答案；元素为正，两端只前进。

```python
def min_sub_array_len(target, nums):
    best = len(nums) + 1          # 哨兵：比任何合法长度都大
    left = total = 0
    for right, x in enumerate(nums):
        total += x
        while total >= target:    # 够了：缩左端
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1
    return best if best <= len(nums) else 0
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 缩左端写成 `if`：`target=9`、`[1,1,1,9]` 得 `4`，应为 `1`。
- 初值写 `0` 再取 `min`：永远是 `0`，要用哨兵。

**追问。**
- 含负数怎么办？：窗口和不再单调，用单调双端队列维护前缀和，见 LC 862。
- 要 `O(n log n)` 的解？：前缀和单调递增，对每个右端二分查找左端。

**同模式。** LC 3 无重复字符的最长子串、LC 76 最小覆盖子串、LC 713 乘积小于 K 的子数组、LC 862 和至少为 K 的最短子数组
