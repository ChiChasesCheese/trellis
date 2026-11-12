---
slug: tt-pythagorean-triple-in-array
---
## Q
**整数数组中的勾股三元组**｜Medium

整数数组 `nums`（可有负数、`0`、重复值），判断是否存在三个不同下标 `i`、`j`、`k` 使 `nums[i]^2 + nums[j]^2 == nums[k]^2`，要求 `O(n^2)`。例：`[-3,4,-5]` → `True`，`[3,3,5]` → `False`。

## A
**一句话。** 先平方并排序，再倒着枚举斜边 `sq[k]`，在左边用双指针找两数之和（3Sum 结构）。

```python
def has_pythagorean_triple(nums):
    sq = sorted(x * x for x in nums)   # 平方抹掉符号
    for k in range(len(sq) - 1, 1, -1):  # sq[k] 当斜边
        i, j = 0, k - 1
        while i < j:
            s = sq[i] + sq[j]
            if s == sq[k]:
                return True
            if s < sq[k]:
                i += 1
            else:
                j -= 1
    return False
```

**复杂度。** 时间 `O(n^2)`，空间 `O(n)`。

**易错点。**
- 没平方就排序：`[-5,3,4]` 最大的是 `4`，找不到，应为 `True`。
- 用集合去重：`[0,0,0]` 只剩一个 `0`，应为 `True`；值可以相同，只要下标不同。
- 指针范围写成 `j = k`：斜边被当成直角边，`[0,5,7]` 误判 `True`，必须 `i < j < k`。

**追问。**
- 要统计所有不重复的三元组？：命中后跳过相同的平方值，避免重复计数。
- 值域有上界 `M`、数组很长？：用勾股数公式 `(m²-n², 2mn, m²+n²)` 生成候选，再哈希查是否都在数组里。

**同模式。** LC 15 三数之和、LC 611 有效三角形的个数、LC 16 最接近的三数之和
