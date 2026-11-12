---
slug: create-maximum-number
---
## Q
**LC 321 拼接最大数**｜Hard

从 `nums1`、`nums2` 共取 `k` 个数字拼成最大的数，同一数组内保持原顺序。

## A
**一句话。** 枚举从 `nums1` 取 `i` 个，每边用单调栈挑最大子序列，再按「剩余后缀字典序」归并，取所有 `i` 的最大值。

```python
def max_number(nums1, nums2, k):
    def pick(nums, t):               # 最大的长度为 t 的子序列
        drop, st = len(nums) - t, []
        for x in nums:
            while drop and st and st[-1] < x:
                st.pop()
                drop -= 1
            st.append(x)
        return st[:t]

    def merge(a, b):                 # 比较整个后缀
        out, i, j = [], 0, 0
        while i < len(a) or j < len(b):
            if a[i:] >= b[j:]:
                out.append(a[i])
                i += 1
            else:
                out.append(b[j])
                j += 1
        return out

    m, n = len(nums1), len(nums2)
    return max(merge(pick(nums1, i), pick(nums2, k - i))
               for i in range(max(0, k - n), min(k, m) + 1))
```

**复杂度。** 时间 `O(k·(m+n+k²))`，空间 `O(m+n)`。

**易错点。**
- 合并只比首位、相等时随便取：`[2,5]` 与 `[2,6]` 得 `[2,5,2,6]`，应为 `[2,6,2,5]`。
- 单调栈不限制丢弃次数：`pick([1,2,3],2)` 只剩 `[3]`，应为 `[2,3]`。
- `i` 的范围写错：应为 `max(0, k-n)` 到 `min(k, m)`。

**追问。**
- 单个数组求最小的数怎么做（LC 402）？：同样的单调栈，改成弹掉更大的，再去前导 `0`。
- 后缀比较太慢怎么办？：给数组建后缀数组或缓存比较结果，每步降到 `O(1)`。

**同模式。** LC 402 移掉 K 位数字、LC 316 去除重复字母、LC 1673 找出最具竞争力的子序列、LC 1754 构造字典序最大的合并字符串
