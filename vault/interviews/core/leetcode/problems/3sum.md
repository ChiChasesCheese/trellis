---
slug: 3sum
---
## Q
**LC 15 三数之和**｜Medium

给整数数组 `nums`，返回所有和为 `0` 且不重复的三元组。

## A
**一句话。** 先排序，固定第一个数，在其右边用对撞双指针找两数之和，三处跳过重复值。

```python
def three_sum(nums):
    nums = sorted(nums)
    n = len(nums)
    res = []
    for i in range(n - 2):
        if nums[i] > 0:              # 最小数都 > 0，不可能为 0
            break
        if i > 0 and nums[i] == nums[i - 1]:
            continue                 # 第一个数去重
        lo, hi = i + 1, n - 1
        while lo < hi:
            s = nums[i] + nums[lo] + nums[hi]
            if s < 0:
                lo += 1
            elif s > 0:
                hi -= 1
            else:
                res.append([nums[i], nums[lo], nums[hi]])
                lo += 1
                hi -= 1
                while lo < hi and nums[lo] == nums[lo - 1]:
                    lo += 1          # 第二个数去重
    return res
```

**复杂度。** 时间 `O(n^2)`，空间 `O(1)`。

**易错点。**
- 和后一个比较去重（`nums[i] == nums[i+1]`）：`[-1,0,1,2,-1,-4]` 丢掉 `[-1,-1,2]`。
- 找到解后只移一个指针：会死循环或重复输出。

**追问。**
- 最接近目标的三数之和？：同样排序加双指针，记录差的绝对值最小的和（LC 16）。
- 四数之和、`k` 数之和？：递归固定前 `k-2` 个数，最后两个用双指针，`O(n^(k-1))`。

**同模式。** LC 1 两数之和、LC 16 最接近的三数之和、LC 18 四数之和、LC 167 两数之和 II
