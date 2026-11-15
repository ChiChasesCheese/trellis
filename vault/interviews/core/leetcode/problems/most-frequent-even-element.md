---
slug: most-frequent-even-element
---
## Q
**LC 2404 出现最频繁的偶数元素**｜Easy

整数数组 `nums`。返回出现次数最多的偶数元素；有多个并列时返回最小的；没有偶数返回 `-1`。

## A
**一句话。** 只统计偶数的出现次数，按（次数降序，值升序）取最优。

```python
def most_frequent_even(nums):
    cnt = Counter(x for x in nums if x % 2 == 0)
    if not cnt:
        return -1
    return min(cnt, key=lambda x: (-cnt[x], x))
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 用 `most_common(1)`：并列时它按首次出现顺序，不是取最小值。
- 没有偶数时直接 `min`：`Counter` 为空会报错，要先返回 `-1`。

**追问。**
- 想一遍扫描、`O(1)` 额外空间？：偶数个数不定，要计数就需要哈希表，除非先排序。

**同模式。** LC 169 多数元素、LC 229 多数元素 II、LC 347 前 K 个高频元素
