---
id: tlc-shu-zu-zhong-de-ni-xu-dui-lcof-2-code
node: b.shu-zu-zhong-de-ni-xu-dui-lcof
type: qa
step: 2
---
## Q
**剑指 Offer 51 数组中的逆序对**｜写出 Python 实现

数组 `record`，`0 <= record.length <= 50000`。逆序对是满足 `i < j` 且 `record[i] > record[j]` 的 `(i, j)`（严格大于）。返回逆序对总数，要求 `O(n log n)`。

## A
**思路。** 递归归并排序，递归函数返回「排好序的列表, 逆序对数」。合并两个有序的半边时，用双指针；取一个左边元素时，已经取走的右边元素（`j` 个）都严格小于它，给计数加 `j`；右半取完后左半剩余的元素比所有右边元素都大，加 `(len(left) - i) * len(right)`。

```python
def reverse_pairs(record: list[int]) -> int:
    def sort(a: list[int]) -> tuple[list[int], int]:
        if len(a) <= 1:
            return a, 0
        mid = len(a) // 2
        left, x = sort(a[:mid])
        right, y = sort(a[mid:])
        merged: list[int] = []
        count = x + y                              # 左半内部、右半内部的逆序对
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:                # 相等不算逆序：先取左边
                merged.append(left[i])
                count += j                         # 此时已取走的 j 个右边元素都严格小于 left[i]
                i += 1
            else:
                merged.append(right[j])
                j += 1
        count += (len(left) - i) * len(right)      # 右半取完后，剩下的左元素比全部右元素都大
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged, count

    return sort(record)[1]
```

运行：`[9,7,5,4,6]` → `8`，`[]` → `0`，`[1]` → `0`，`[2,2,2]` → `0`，`[3,2,1]` → `3`；`50000` 个随机数约 `0.04` 秒，`50000` 到 `1` 的降序数组 → `1249975000`。

**复杂度。** 时间 `O(n log n)`；空间 `O(n)`，每层合并的临时列表，递归深度 `O(log n)`。

**写法要点。** 内层函数 `sort` 返回元组 `(有序列表, 计数)`，调用方用元组解包同时接两个值；长度 `0` 或 `1` 直接返回，空数组自然得到 `0`；`left[i] <= right[j]` 里的 `<=` 决定相等不算逆序；最后用 `extend` 把剩余部分接上，两个剩余部分至多一个非空；切片 `a[:mid]` 会复制，换取代码短，`n = 5 * 10^4` 毫无压力。
