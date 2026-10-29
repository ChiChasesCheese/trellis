---
id: uth-go-rust-modern-sorts-1-pdqsort
node: go-rust.modern-sorts
type: qa
step: 1
---
## Q
**pdqsort 怎么躲开快排的最坏情况**｜Go · 1.19 起

`sort.Sort` 用的抗模式快排（pattern-defeating quicksort，pdqsort）比普通快排多做了什么？

## A
**背景。** 快速排序：挑一个枢轴，比它小的放左、大的放右，再各自排。平均很快，但碰上特殊输入就会变慢：枢轴总挑得很偏、已经有序、大量重复值。pdqsort 的办法是先识别这些常见模式，各个击破。例：数组全是同一个值时，普通划分每轮只去掉一个元素；pdqsort 发现枢轴等于祖先枢轴，一次就把所有相等元素归到一边。

**结构。** 快速排序加一套“情况不对就换招”的检查，另有堆排序兜底。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 215">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">pdqsort: 先看输入像什么模式</text>
<rect x="8" y="26" width="140" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="78" y="43.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">长度 ≤ 12</text>
<line x1="148" y1="40" x2="164" y2="40" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="164,40 158.0,42.7 158.0,37.3" style="fill:var(--accent,#3b6fd4)"/>
<rect x="164" y="26" width="166" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="247" y="43.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">插入排序</text>
<rect x="8" y="62" width="140" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="78" y="79.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">长度 ≥ 50</text>
<line x1="148" y1="76" x2="164" y2="76" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="164,76 158.0,78.7 158.0,73.3" style="fill:var(--accent,#3b6fd4)"/>
<rect x="164" y="62" width="166" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="247" y="79.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">九个数取中位数选枢轴</text>
<rect x="8" y="98" width="140" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="78" y="115.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">划分后短侧 &lt; 1/8</text>
<line x1="148" y1="112" x2="164" y2="112" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="164,112 158.0,114.7 158.0,109.3" style="fill:var(--accent,#3b6fd4)"/>
<rect x="164" y="98" width="166" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="247" y="115.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">随机交换几个元素打乱规律</text>
<rect x="8" y="134" width="140" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="78" y="151.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">枢轴等于祖先枢轴</text>
<line x1="148" y1="148" x2="164" y2="148" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="164,148 158.0,150.7 158.0,145.3" style="fill:var(--accent,#3b6fd4)"/>
<rect x="164" y="134" width="166" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="247" y="151.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">一次把相等元素归到一边</text>
<rect x="8" y="170" width="140" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="78" y="187.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">不平衡 &gt; bits.Len(n) 次</text>
<line x1="148" y1="184" x2="164" y2="184" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="164,184 158.0,186.7 158.0,181.3" style="fill:var(--accent,#3b6fd4)"/>
<rect x="164" y="170" width="166" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="247" y="187.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">改用堆排序</text>
</svg>
```

**细节。**

- 长度 ≤ 12 用插入排序；长度 ≥ 50 用 Tukey ninther（九个数取中位数）选枢轴
- 划分后较短一侧不足 1/8，就随机交换几个元素打乱规律
- 不平衡划分累计超过 `bits.Len(n)` 次，改用堆排序
- 枢轴等于祖先枢轴时，一次把相等元素归到一边，应对大量重复值

**为什么。** 它识别已排序、逆序、大量重复这些常见输入模式并专门处理。

**例题：** LC 75 颜色分类（同类：LC 912 排序数组）

数组里只有 `0`、`1`、`2`，原地排好序，不用库函数，最好一趟扫描。例：`[2,0,2,1,1,0]` → `[0,0,1,1,2,2]`。三个指针把数组划成“小于、等于、大于”三段，大量重复值时“等于”那段一次归好，和 pdqsort 处理相等元素同一个思路。

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
