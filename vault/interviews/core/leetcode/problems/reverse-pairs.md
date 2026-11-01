---
slug: reverse-pairs
---
## Q
**LC 493 翻转对（Reverse Pairs）**｜Hard

给定一个数组 `nums`，如果 `i < j` 且 `nums[i] > 2 * nums[j]`，我们就将 `(i, j)` 称作一个重要翻转对。返回给定数组中的重要翻转对的数量。数组长度不会超过 `50000`，输入数组中的所有数字都在 32 位整数的表示范围内。例：`nums = [1,3,2,3,1]` → `2`（`(1,4)` 和 `(3,4)`）；`nums = [2,4,3,5,1]` → `3`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 归并排序（merge sort）中统计跨左右两半的逆序类配对（counting inversions 的变形）。

**一句话。** 归并排序递归排好左右两半，因为两半各自有序，用一个单调右移的指针就能在线性时间里数出「左半元素 > 2 × 右半元素」的对数，再把两半合并。

**识别。** 「`i < j` 且 `nums[i]` 与 `nums[j]` 满足某个大小关系」是逆序对一族：归并排序（分治）、树状数组（BIT）+ 离散化都行。`n = 5 * 10^4`，`O(n^2)` 约 `1.25 * 10^9` 次比较，超时；需要 `O(n log n)`。

**推导。** 暴力双层循环 `O(n^2)`。分治：把配对分成三类——都在左半、都在右半、跨两半。跨两半的配对里，`i` 在左、`j` 在右，**顺序已经确定**，只关心数值，所以可以先把两半各自排序而不影响计数。排序后，对左半的每个 `x`（递增），右半满足 `x > 2y` 的 `y` 是一个前缀，`x` 变大时前缀只增不减，所以一个指针 `j` 只右移，整个跨半计数 `O(len)`。计数必须在合并之前做（合并后左右混在一起）。

```python
def reverse_pairs(nums: list[int]) -> int:
    def sort_count(a: list[int]) -> tuple[list[int], int]:     # 返回 (排好序的 a, a 内部的翻转对数)
        if len(a) <= 1:
            return a, 0
        mid = len(a) // 2
        left, cl = sort_count(a[:mid])
        right, cr = sort_count(a[mid:])
        cross = j = 0                                # 左段元素 x 在前、右段元素 y 在后的翻转对
        for x in left:                               # left 递增：x 变大，满足 x > 2y 的 y 前缀只会变长
            while j < len(right) and x > 2 * right[j]:
                j += 1
            cross += j
        return sorted(left + right), cl + cr + cross    # 两段各自有序，Timsort 线性时间归并
    return sort_count(nums)[1]
```

运行：`[1,3,2,3,1]` → `2`，`[2,4,3,5,1]` → `3`，`[2147483647, -2147483648]` → `1`，`[5]` → `0`。

**复杂度。** 时间 `O(n log n)`（`log n` 层，每层计数与合并都是线性）；空间 `O(n)`。递归深度 `log n`，不会触发递归限制。

**拓展优化。**
- 树状数组（Fenwick tree，BIT）+ 离散化：从左到右处理 `nums[j]`，查询「已处理元素里 `> 2 * nums[j]` 的个数」，再把 `nums[j]` 加入。

```python
from bisect import bisect_left, bisect_right


def reverse_pairs_bit(nums: list[int]) -> int:
    vals = sorted(set(nums))                  # 离散化：把数值压成 1..m 的名次
    tree = [0] * (len(vals) + 1)              # 树状数组：统计已见元素落在每个名次的个数

    def add(i: int) -> None:
        while i < len(tree):
            tree[i] += 1
            i += i & -i

    def query(i: int) -> int:                 # 名次 <= i 的已见元素个数
        s = 0
        while i:
            s += tree[i]
            i -= i & -i
        return s

    ans = 0
    for seen, y in enumerate(nums):           # seen = 已处理的元素个数
        ans += seen - query(bisect_right(vals, 2 * y))    # 已见元素里 > 2y 的个数
        add(bisect_left(vals, y) + 1)
    return ans
```

- 查询时 `2 * y` 不一定在 `vals` 里，所以用 `bisect_right` 求「`<= 2y` 的名次数」；离散化只放原数组的值。

**易错点。**
- 把条件写成 `>=`：`[1,3,2,3,1]` 得到 `3`，正确 `2`；写成 `x > y`（普通逆序对）得到 `4`。
- 先合并再计数：合并后左右元素混在一起，指针不再单调，结果错误。必须先数跨半的配对再合并。
- C++/Java 里 `2 * nums[j]` 对 `-2^31` 会溢出 32 位：要先转 `long`；Python 整数不会溢出，`[2147483647, -2147483648]` 的答案是 `1`。

**同模式。** LC 315 计算右侧小于当前元素的个数、LC 327 区间和的个数、LC 912 排序数组、LC 148 排序链表。
