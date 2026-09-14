---
id: leetcode-q-remove-duplicates-from-sorted-array-pattern
node: two-pointers-window.two-pointers
type: qa
anki: 1787613692436
tags: [lc::26, leetcode, pattern, recall]
---
## Q
有序数组原地去重（LeetCode 26），双指针怎么设计？

## A
慢指针 uid 指向「已确认去重区间」的最后一个元素，快指针 cur 向前扫描。因为数组已排序，重复元素必然相邻，所以只需比较 nums[uid] 和 nums[cur]：相等则跳过（cur+=1）；不相等则 uid 先自增，再把 nums[cur] 写入 nums[uid]。最后返回 uid+1 即为去重后长度。核心是利用「有序」这一性质，把判重简化为单点比较，而不是维护集合。

**Evidence**

```
uid = 0
cur = 0
while cur < len(nums):
    if nums[uid] == nums[cur]:
        cur += 1
    else:
        uid += 1
        nums[uid] = nums[cur]
        cur += 1
return uid + 1
```

[原文 ↗](obsidian://open?vault=lc&file=questions%2F26%20-%20Remove%20Duplicates%20from%20Sorted%20Array)
