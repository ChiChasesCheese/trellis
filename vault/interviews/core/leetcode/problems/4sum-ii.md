---
slug: 4sum-ii
---
## Q
**LC 454 四数相加 II**｜Medium

四个等长数组 `nums1..nums4`，求有多少个下标四元组 `(i, j, k, l)` 满足 `nums1[i] + nums2[j] + nums3[k] + nums4[l] == 0`。

## A
**一句话。** 折半（meet in the middle）：前两个数组所有两数和进哈希表计数，再对后两个数组的每个两数和查它的相反数。

```python
def four_sum_count(nums1, nums2, nums3, nums4):
    ab = Counter(a + b for a in nums1 for b in nums2)
    ans = 0
    for c in nums3:
        for d in nums4:
            ans += ab[-c - d]      # 相反数出现的次数
    return ans
```

**复杂度。** 时间 `O(n^2)`，空间 `O(n^2)`。

**易错点。**
- 把哈希表值存成「是否出现」：要的是方案数，必须计次数。
- 先对四个数组各自去重：下标不同的相同值是不同的四元组，不能去重。

**追问。**
- 为什么不是 `O(n^4)` 也不是 `O(n^3)`？：折半后两边各只有 `n^2` 个和，哈希查询 `O(1)`。
- 想要具体的四元组而不仅是个数？：表里存下标列表，输出量本身可能是 `n^4`。

**同模式。** LC 18 四数之和、LC 1 两数之和、LC 1679 K 和数对的最大数目
