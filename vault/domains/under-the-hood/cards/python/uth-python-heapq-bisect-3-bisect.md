---
id: uth-python-heapq-bisect-3-bisect
node: python.heapq-bisect
type: qa
step: 3
---
## Q
**bisect_left 与 bisect_right 差在哪**｜Python · CPython 3.14

对 `[1, 2, 2, 2, 3]` 查 `2`，两个函数分别返回什么？`insort` 为什么不是 O(log n)？

## A
**背景。** 在有序列表里找位置，从头扫是 O(n)。二分（binary search）每次看中间一个元素，一次排除一半，只要 O(log n) 次比较。`bisect` 就是现成的二分。

**结构。** 在有序 `list` 上不断缩小查找区间 `[lo, hi)`，不额外分配内存（`bisect.py` 是纯 Python，另有 C 加速版）。有重复值时，「该插在哪」有两个答案：

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 170">
<rect x="45" y="70" width="50" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="70" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="95" y="70" width="50" height="32" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="120" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="145" y="70" width="50" height="32" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="170" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="195" y="70" width="50" height="32" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="220" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="245" y="70" width="50" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="270" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="45" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<line x1="45" y1="104" x2="45" y2="110" stroke-width="1" stroke="currentColor"/>
<text x="95" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<line x1="95" y1="104" x2="95" y2="110" stroke-width="1" stroke="currentColor"/>
<text x="145" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<line x1="145" y1="104" x2="145" y2="110" stroke-width="1" stroke="currentColor"/>
<text x="195" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<line x1="195" y1="104" x2="195" y2="110" stroke-width="1" stroke="currentColor"/>
<text x="245" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<line x1="245" y1="104" x2="245" y2="110" stroke-width="1" stroke="currentColor"/>
<text x="295" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<line x1="295" y1="104" x2="295" y2="110" stroke-width="1" stroke="currentColor"/>
<line x1="95" y1="52" x2="95" y2="70" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="95.0,70.0 92.0,64.0 98.0,64.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="95" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">bisect_left = 1</text>
<line x1="245" y1="52" x2="245" y2="70" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="245.0,70.0 242.0,64.0 248.0,64.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="245" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">bisect_right = 4</text>
<text x="170" y="150" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">线上的数字是插入位置</text>
</svg>
```

**细节。**

- 实测 `bisect_left` 返回 1（第一个 2 的位置），`bisect_right` 返回 4（最后一个 2 之后）。
- `bisect_left` 比较 `a[mid] < x`，`bisect_right` 比较 `x < a[mid]`，只用 `<`。
- `insort` 是二分加 `list.insert`，查找 O(log n)，但插入要搬动元素，整体 O(n)。

**为什么。** 3.10 起支持 `key=`，用法和 `sorted` 一致；键开销大时先预算一列键再二分。

**例题：** LC 34 在排序数组中查找元素的第一个和最后一个位置

给非递减的整数数组 `nums` 和 `target`，返回 `target` 出现的起止下标，不存在返回 `[-1, -1]`。要求时间复杂度 O(log n)。

```python
import bisect

def search_range(nums: list[int], target: int) -> list[int]:
    left = bisect.bisect_left(nums, target)
    if left == len(nums) or nums[left] != target:
        return [-1, -1]
    right = bisect.bisect_right(nums, target) - 1
    return [left, right]
```
