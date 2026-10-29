---
id: uth-cpp-sort-2-stable-nth
node: cpp.sort
type: qa
step: 2
---
## Q
**stable_sort 与 nth_element 各是什么算法**｜C++ · libstdc++ 16

标准库里“稳定排序”和“取第 k 小”分别是怎么实现的？

## A
**背景。** 两个常见需求：排序后相等的元素保持原来的先后顺序（稳定，stable）；只要第 k 小的数，不必把整个数组排好。

**结构。** `stable_sort` 是归并排序（merge sort：把两段各自排好的数据合并成一段）；`nth_element` 是快速选择（quickselect：像快排那样划分，但只往含第 n 位的一侧继续）。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 225">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">nth_element: 每轮只处理含第 n 位的一侧</text>
<rect x="10" y="28" width="300" height="20" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<line x1="160" y1="26" x2="160" y2="50" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<circle cx="250" cy="38" r="4" style="fill:var(--accent,#3b6fd4)" stroke="none"/>
<rect x="160" y="56" width="150" height="20" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<line x1="240" y1="54" x2="240" y2="78" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<circle cx="250" cy="66" r="4" style="fill:var(--accent,#3b6fd4)" stroke="none"/>
<rect x="240" y="84" width="70" height="20" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<circle cx="250" cy="94" r="4" style="fill:var(--accent,#3b6fd4)" stroke="none"/>
<text x="8" y="116" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">蓝竖线 = 枢轴, 圆点 = 第 n 位, 它总在某一侧</text>
<text x="8" y="144" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">stable_sort: 归并, 借 n/2 的临时缓冲</text>
<rect x="10" y="156" width="70" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="45" y="171.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">有序 A</text>
<rect x="90" y="156" width="70" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="125" y="171.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">有序 B</text>
<line x1="85" y1="178" x2="85" y2="194" stroke="currentColor" stroke-width="1"/>
<polygon points="85,194 82.3,188.0 87.7,188.0" fill="currentColor"/>
<rect x="10" y="194" width="150" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="85" y="209.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">缓冲里合并, 写回</text>
<text x="250" y="170" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">相等元素</text>
<text x="250" y="186" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">先来先走</text>
<text x="250" y="202" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">所以稳定</text>
</svg>
```

**细节。**

- `stable_sort` 申请一块 n/2 大小的临时缓冲来归并，O(n log n)
- 缓冲申请不到时退化成不用额外内存的原地归并，标准允许慢到 O(n log² n)
- `nth_element` 每轮划分后只处理含第 n 位的一侧，平均 O(n)
- 它同样有深度上限，超限改用堆选择（heap_select：用堆挑出最小的 n 个）

**为什么。** 稳定要求相等元素保持原顺序，快排做不到，归并天然稳定，代价是额外空间。

**例题：** LC 215 数组中的第 K 个最大元素（同类：LC 912 排序数组）

给整数数组 `nums` 和 `k`，返回排序后第 `k` 个最大的元素，要求平均 O(n)。例：`[3,2,1,5,6,4]`、`k = 2` → `5`。下面是快速选择：每轮随机取枢轴，只留下答案所在的一侧。

```python
import random

def find_kth_largest(nums: list[int], k: int) -> int:
    while True:
        pivot = random.choice(nums)
        bigger = [x for x in nums if x > pivot]
        equal = nums.count(pivot)
        if k <= len(bigger):                       # 答案在比 pivot 大的那一堆里
            nums = bigger
        elif k <= len(bigger) + equal:             # 落在 pivot 自己这一段
            return pivot
        else:                                      # 答案在比 pivot 小的那一堆里
            k -= len(bigger) + equal
            nums = [x for x in nums if x < pivot]
```
