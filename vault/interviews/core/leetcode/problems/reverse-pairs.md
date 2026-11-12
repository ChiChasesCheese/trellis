---
slug: reverse-pairs
---
## Q
**LC 493 翻转对**｜Hard

数出满足 `i < j` 且 `nums[i] > 2 * nums[j]` 的数对个数。

## A
**一句话。** 归并排序：两半各自有序后，用单调右移的指针数出「左半 > 2×右半」的对数，再合并。

```python
def reverse_pairs(nums):
    def sort_count(a):    # 返回 (排好序的 a, 翻转对数)
        if len(a) <= 1:
            return a, 0
        mid = len(a) // 2
        left, cl = sort_count(a[:mid])
        right, cr = sort_count(a[mid:])
        cross = j = 0
        for x in left:    # x 变大，满足条件的 y 前缀只会变长
            while j < len(right) and x > 2 * right[j]:
                j += 1
            cross += j
        return sorted(left + right), cl + cr + cross

    return sort_count(nums)[1]
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 条件写成 `>=`：`[1,3,2,3,1]` 得 `3`，应为 `2`；写成 `x > y` 就是普通逆序对。
- 先合并再计数：合并后左右混在一起，指针不再单调。
- 其他语言里 `2 * nums[j]` 对 `-2^31` 会溢出：要先转 `long`。

**追问。**
- 能边合并边计数吗？：不能，合并比的是 `x` 与 `y`，计数比的是 `x` 与 `2y`，指针停点不同，要单独扫一遍。
- 数据流在线处理呢？：树状数组或动态开点线段树，每次插入 `O(log n)`。

**同模式。** LC 315 计算右侧小于当前元素的个数、LC 327 区间和的个数、LC 912 排序数组、LC 148 排序链表
