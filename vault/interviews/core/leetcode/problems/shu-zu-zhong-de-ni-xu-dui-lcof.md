---
slug: shu-zu-zhong-de-ni-xu-dui-lcof
---
## Q
**剑指 Offer 51 数组中的逆序对**｜Hard

数组 `record` 中满足 `i < j` 且 `record[i] > record[j]` 的 `(i, j)` 叫逆序对，求总数。

## A
**一句话。** 归并排序，合并时取左元素的那一刻，已取走的右元素个数 `j` 就是它的逆序数。

```python
def reverse_pairs(record):
    def sort(a):
        if len(a) <= 1:
            return a, 0
        mid = len(a) // 2
        left, x = sort(a[:mid])
        right, y = sort(a[mid:])
        merged, cnt = [], x + y
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:     # 相等不算逆序，先取左
                merged.append(left[i])
                cnt += j                # 已取走的右元素都更小
                i += 1
            else:
                merged.append(right[j])
                j += 1
        cnt += (len(left) - i) * len(right)   # 左剩余大于全部右
        return merged + left[i:] + right[j:], cnt

    return sort(record)[1]
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 相等时先取右（`<` 代替 `<=`）：相等对被算进去，`[5,5]` 得 `1`，应为 `0`。
- 漏了右半取完后左半的剩余：`[2,1]` 得 `0`，应为 `1`。
- 只返回计数不返回有序数组：上一层合并需要有序的两半。

**追问。**
- 每个元素右侧有多少个更小的（LC 315）？：归并时带原下标，取左元素时给它的计数加 `j`。
- 翻转对（LC 493，`nums[i] > 2 * nums[j]`）？：合并前先用双指针单独数一遍。
- 换成树状数组？：离散化后从右往左，查前缀和再更新，`O(n log n)`。

**同模式。** LC 315 计算右侧小于当前元素的个数、LC 493 翻转对、LC 327 区间和的个数、LC 912 排序数组
