---
id: tlc-create-maximum-number-5-alt
node: b.create-maximum-number
type: qa
step: 5
---
## Q
**LC 321 拼接最大数**｜另一种解法

挑最大子序列不用单调栈、合并时也不手写双指针，还能怎么写？和单调栈版怎么选？

## A
**思路。** 挑子序列用「窗口取最大」的贪心：还要挑 `need` 个时，下一位只能落在 `nums[start : len - need + 1]` 里（要给后面留 `need - 1` 个），取其中**最左**的最大值。合并用 `max(a, b).pop(0)`：两个列表按字典序比较，大的那个弹出首位。

```python
def max_number_window(nums1: list[int], nums2: list[int], k: int) -> list[int]:
    def pick(nums: list[int], t: int) -> list[int]:
        out: list[int] = []
        start = 0
        for need in range(t, 0, -1):                   # 还要挑 need 个
            window = nums[start : len(nums) - need + 1]
            best = max(window)
            start += window.index(best) + 1            # 取最左的最大值，后面选择更多
            out.append(best)
        return out

    def merge(a: list[int], b: list[int]) -> list[int]:
        a, b = a[:], b[:]                              # 复制一份，不改动原列表
        return [max(a, b).pop(0) for _ in range(len(a) + len(b))]

    m, n = len(nums1), len(nums2)
    return max(
        merge(pick(nums1, i), pick(nums2, k - i))
        for i in range(max(0, k - n), min(k, m) + 1)
    )
```

运行：`[3,4,6,5]`, `[9,1,2,5,8,3]`, `5` → `[9,8,6,5,3]`；`[2,5]`, `[2,6]`, `4` → `[2,6,2,5]`。

**取舍。** 窗口贪心每挑一位要扫一遍窗口，`pick` 是 `O(t · len)`，比单调栈的 `O(len)` 慢，但「每一位取能取到的最大值」最直观，适合先说出来再优化。`max(a, b).pop(0)` 是同一个后缀比较规则的简写，`pop(0)` 每次移动整个列表，复杂度与切片比较同级。面试正式答案写单调栈 + 显式合并，复杂度更好、每一步也好解释。
