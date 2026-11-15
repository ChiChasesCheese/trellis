---
slug: find-smallest-letter-greater-than-target
---
## Q
**LC 744 寻找比目标字母大的最小字母**｜Easy

非递减的小写字母数组 `letters` 和目标字母 `target`。返回 `letters` 中严格大于 `target` 的最小字母；若没有，则绕回返回第一个字母。

## A
**一句话。** 二分找第一个严格大于 `target` 的位置，越界就对长度取模绕回开头。

```python
def next_greatest_letter(letters, target):
    lo, hi = 0, len(letters)
    while lo < hi:
        mid = (lo + hi) // 2
        if letters[mid] > target:
            hi = mid             # mid 可能就是答案
        else:
            lo = mid + 1
    return letters[lo % len(letters)]   # 全部 <= target 时绕回
```

**复杂度。** 时间 `O(log n)`，空间 `O(1)`。

**易错点。**
- 用 `>=` 判断：等于 `target` 的字母不算，必须严格大于。
- 忘了取模：`lo == len(letters)` 时越界。

**追问。**
- 能直接用库函数吗？：`bisect_right(letters, target)` 就是第一个严格大于的位置。
- 不要求绕回呢？：越界时返回「无解」即可，其余相同。

**同模式。** LC 35 搜索插入位置、LC 34 在排序数组中查找元素的第一个和最后一个位置、LC 704 二分查找、LC 69 x 的平方根
