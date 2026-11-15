---
slug: advantage-shuffle
---
## Q
**LC 870 优势洗牌**｜Medium

给两个等长数组 `nums1`、`nums2`。重排 `nums1`，使满足 `nums1[i] > nums2[i]` 的下标 `i` 尽量多，返回重排后的 `nums1`。

## A
**一句话。** 田忌赛马：对手从强到弱，我方最强能赢就上最强，赢不了就派最弱的去送。

```python
def advantage_count(nums1, nums2):
    a = sorted(nums1)
    ans = [None] * len(a)
    lo, hi = 0, len(a) - 1
    # nums2 的下标按值从大到小：先对付最强的对手
    for i in sorted(range(len(a)), key=lambda i: -nums2[i]):
        if a[hi] > nums2[i]:
            ans[i] = a[hi]       # 能赢就用最强的
            hi -= 1
        else:
            ans[i] = a[lo]       # 赢不了就送最弱的
            lo += 1
    return ans
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 把 `nums2` 本身排序：要按 `nums2` 的原下标放结果，所以排的是下标。
- 赢不了时随便放：必须放最小的，保留强牌去赢更弱的对手。

**追问。**
- 为什么最强对手先处理？：它最难赢，赢得了才值，赢不了就拿最弱牌送掉，损失最小。
- 另一种从小到大的写法？：双指针让每张我方牌去打能赢的最弱对手，不能赢的放到剩余位置。

**同模式。** LC 455 分发饼干、LC 826 安排工作以达到最大收益、LC 881 救生艇
