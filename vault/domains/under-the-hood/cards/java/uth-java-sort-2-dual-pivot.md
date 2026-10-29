---
id: uth-java-sort-2-dual-pivot
node: java.sort
type: qa
step: 2
---
## Q
**双轴快排怎么避免最坏 O(n²)**｜Java · OpenJDK 25

`Arrays.sort(int[])` 选两个轴点（pivot）把数组分成几段？构造恶意数据能让它退化吗？

## A
**背景。** 快排（quicksort）选一个轴点，比它小的放左边、大的放右边，再分别递归。如果轴点总选到最小或最大，每次只分出一个元素，退化成 O(n²)。

**结构。** 选两个轴点 `pivot1 ≤ pivot2`，一趟分成三段：小于 `pivot1`、介于两者之间、大于 `pivot2`，再递归。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 180">
<rect x="22" y="40" width="80" height="34" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="62" y="61" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">小于 p1</text>
<rect x="102" y="40" width="28" height="34" rx="3" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="116" y="61" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">p1</text>
<rect x="130" y="40" width="80" height="34" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="170" y="61" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">p1 到 p2</text>
<rect x="210" y="40" width="28" height="34" rx="3" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="224" y="61" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">p2</text>
<rect x="238" y="40" width="80" height="34" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="278" y="61" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">大于 p2</text>
<text x="170" y="24" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一趟 分成三段</text>
<line x1="62" y1="80" x2="62" y2="100" stroke-width="1.2" stroke="currentColor"/>
<polygon points="62.0,100.0 60.0,96.0 64.0,96.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="170" y1="80" x2="170" y2="100" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,100.0 168.0,96.0 172.0,96.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="278" y1="80" x2="278" y2="100" stroke-width="1.2" stroke="currentColor"/>
<polygon points="278.0,100.0 276.0,96.0 280.0,96.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="120" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">三段各自递归</text>
<text x="170" y="150" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">递归超过 384 层 切到堆排序</text>
</svg>
```

**细节。**

- 轴点取自五个样本，间隔近似黄金比例，有序输入也不会选到边缘。
- 递归超过 `MAX_RECURSION_DEPTH`（384）就切到堆排序，保证 O(n log n)。
- 近乎有序的数据直接合并已有的有序段。
- `byte` 数组 64 个以上、`short` 与 `char` 数组 1750 个以上，改用计数排序。

**为什么。** 有堆排序兜底，不再有数据能让它退化。JDK 11 文档只写「许多会让其他快排退化的数据」，现在写「所有数据」。

**例题：** LC 75 颜色分类

数组 `nums` 只含 `0`、`1`、`2`，原地排序成 `0`、`1`、`2` 的顺序，不能调用库自带的排序函数。

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
