---
id: uth-java-sort-1-two-algorithms
node: java.sort
type: qa
step: 1
---
## Q
**Arrays.sort 为什么 int[] 和对象用不同算法**｜Java · OpenJDK 25

`Arrays.sort(int[])` 和 `Arrays.sort(Integer[])` 用的是同一个算法吗？为什么？

## A
**背景。** 排序有个性质叫稳定（stable）：值相等的元素，排完后仍保持原来的先后。例：学生先按报名顺序、再按分数排，同分的人应仍按报名顺序。基本类型里两个相等的 `int` 看不出谁是谁，稳不稳定无所谓；对象则不然。

**结构。** 基本类型数组用双轴快速排序（`DualPivotQuicksort`，原地、不稳定）；对象数组用 `TimSort`（有比较器）或 `ComparableTimSort`（稳定，要额外内存）。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<rect x="110" y="14" width="120" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Arrays.sort</text>
<line x1="150" y1="42" x2="90" y2="86" stroke-width="1.2" stroke="currentColor"/>
<polygon points="90.0,86.0 92.6,81.0 95.5,85.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="190" y1="42" x2="250" y2="86" stroke-width="1.2" stroke="currentColor"/>
<polygon points="250.0,86.0 244.5,85.1 247.4,81.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="14" y="86" width="150" height="70" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="176" y="86" width="150" height="70" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="89" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">int[]</text>
<text x="89" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">双轴快排</text>
<text x="89" y="142" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">原地 不稳定</text>
<text x="251" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Integer[]</text>
<text x="251" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">TimSort</text>
<text x="251" y="142" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">稳定 要额外内存</text>
<text x="170" y="180" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">对象要稳定 基本类型不需要</text>
</svg>
```

**细节。**

- 快排原地进行，不要额外内存；对象比较是方法调用，TimSort 比较次数更少。
- 本机实测 200 万个随机数：`int[]` 约 76 毫秒，`Integer[]` 约 228 毫秒（单次测量，非严格基准）。

**为什么。** 稳定性对基本类型没有意义，对对象却是语义要求。

**例题：** LC 215 数组中的第 K 个最大元素

给整数数组 `nums` 和整数 `k`，返回排序后的第 `k` 个最大元素（不是第 `k` 个不同的元素），期望 O(n)。例：`[3,2,1,5,6,4]`，`k = 2` 得 `5`。

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
