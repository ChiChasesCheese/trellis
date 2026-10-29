---
id: uth-cpp-sort-1-introsort
node: cpp.sort
type: qa
step: 1
---
## Q
**std::sort 为什么不会退化成 O(n²)**｜C++ · libstdc++ 16

`std::sort` 底下是快速排序吗？遇到构造好的最坏输入怎么办？

## A
**背景。** 快速排序（quicksort）：挑一个枢轴（pivot），比它小的放左边、比它大的放右边，两边各自再排。例：`[5,2,8,1,9,3]` 取 5 → `[2,1,3]`、5、`[8,9]`。平均 O(n log n)，但枢轴总是恰好最小或最大时，每轮只去掉一个元素，退化成 O(n²)。

**结构。** 内省排序（introsort）：快排为主，发现递归太深（说明被带偏了）就换成堆排序兜底，小区间留给插入排序收尾。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 245">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">例: 枢轴取 5</text>
<rect x="10" y="22" width="30" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="25" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="44" y="22" width="30" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="59" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="78" y="22" width="30" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="93" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<rect x="112" y="22" width="30" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="127" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="146" y="22" width="30" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="161" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9</text>
<rect x="180" y="22" width="30" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="195" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<line x1="110" y1="46" x2="110" y2="62" stroke="currentColor" stroke-width="1"/>
<polygon points="110,62 107.3,56.0 112.7,56.0" fill="currentColor"/>
<rect x="10" y="64" width="30" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="25" y="79.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="44" y="64" width="30" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="59" y="79.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="78" y="64" width="30" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="93" y="79.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="112" y="64" width="30" height="22" rx="3" fill="none" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="127" y="79.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="146" y="64" width="30" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="161" y="79.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<rect x="180" y="64" width="30" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="195" y="79.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9</text>
<text x="222" y="40" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">枢轴总最小或最大:</text>
<text x="222" y="55" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每轮去 1 个, O(n²)</text>
<text x="8" y="108" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">比 5 小的在左, 比 5 大的在右, 两边再各自排</text>
<rect x="10" y="128" width="150" height="46" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="85" y="148" text-anchor="middle" font-size="13" font-family="sans-serif" fill="currentColor">快速排序</text>
<text x="85" y="165" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">枢轴取首,中,尾中位数</text>
<line x1="160" y1="151" x2="230" y2="151" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="230,151 224.0,153.7 224.0,148.3" style="fill:var(--accent,#3b6fd4)"/>
<text x="195" y="144" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">深度超限</text>
<text x="195" y="168" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">&gt; 2·log₂n</text>
<rect x="230" y="128" width="100" height="46" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="280" y="148" text-anchor="middle" font-size="13" font-family="sans-serif" fill="currentColor">堆排序</text>
<text x="280" y="165" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">O(n log n) 兜底</text>
<line x1="85" y1="174" x2="85" y2="200" stroke="currentColor" stroke-width="1"/>
<polygon points="85,200 82.3,194.0 87.7,194.0" fill="currentColor"/>
<text x="96" y="192" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">区间 ≤ 16 就停手</text>
<rect x="10" y="200" width="150" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="85" y="217" text-anchor="middle" font-size="13" font-family="sans-serif" fill="currentColor">整体插入排序</text>
<text x="85" y="232" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">收尾, 数组已近乎有序</text>
</svg>
```

**细节。**

- 枢轴取首、中、尾三个数的中位数
- 递归深度超过 2·⌊log₂ n⌋，这一段改用堆排序（把数组当堆，反复取走最大的）
- 区间缩到 16 个元素以内就停手，最后整个数组跑一遍插入排序（把元素逐个插进前面已排好的部分，近乎有序时很快）
- libc++ 阈值不同：小于 24 个用插入排序

**为什么。** 快排常数小，但最坏 O(n²)；堆排序慢一点，却保证 O(n log n)，只在快排“走偏”时启用。

**例题：** LC 75 颜色分类（同类：LC 912 排序数组）

数组里只有 `0`、`1`、`2`，原地排好序，不用库函数，最好一趟扫描。例：`[2,0,2,1,1,0]` → `[0,0,1,1,2,2]`。三个指针把数组划成“小于、等于、大于”三段，就是快排的划分。

```python
def sort_colors(nums: list[int]) -> None:
    # 不变量：nums[:lo] 全是 0，nums[lo:i] 全是 1，nums[hi+1:] 全是 2，nums[i:hi+1] 未检查
    lo, i, hi = 0, 0, len(nums) - 1
    while i <= hi:
        if nums[i] == 0:
            nums[lo], nums[i] = nums[i], nums[lo]   # 换来的一定是 1（区间 [lo, i) 全是 1），i 可以前进
            lo += 1
            i += 1
        elif nums[i] == 2:
            nums[i], nums[hi] = nums[hi], nums[i]   # 换来的是未检查的数，i 不能动
            hi -= 1
        else:
            i += 1
```
