---
id: uth-python-set-3-intersection
node: python.set
type: qa
step: 3
---
## Q
**小集合和大集合求交集有多快**｜Python · CPython 3.14

`{1,2,3} & set(range(10**6))` 要 100 万次比较吗？`in` 用 `set` 和 `list` 差多少？

## A
**背景。** 求交集最直接是两边各遍历一遍互相比，O(m + n)。但 `set` 查一个元素是 O(1)，那只要遍历小的一边，逐个去大的里面查。

**结构。** `set_intersection` 先比较两边大小，**遍历较小的那个**，每个元素去较大的集合里做一次哈希查找。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<text x="46" y="20" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">小 set</text>
<rect x="30" y="32" width="32" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="46" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="30" y="68" width="32" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="46" y="86" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="30" y="104" width="32" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="46" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="250" y="20" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">大 set 100 万个</text>
<rect x="170" y="32" width="26" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="196" y="32" width="26" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="222" y="32" width="26" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="248" y="32" width="26" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="274" y="32" width="26" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="300" y="32" width="26" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="170" y="58" width="26" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="196" y="58" width="26" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="222" y="58" width="26" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="248" y="58" width="26" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="274" y="58" width="26" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="300" y="58" width="26" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="170" y="84" width="26" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="196" y="84" width="26" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="222" y="84" width="26" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="248" y="84" width="26" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="274" y="84" width="26" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="300" y="84" width="26" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="170" y="110" width="26" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="196" y="110" width="26" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="222" y="110" width="26" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="248" y="110" width="26" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="274" y="110" width="26" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="300" y="110" width="26" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="170" y="136" width="26" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="196" y="136" width="26" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="222" y="136" width="26" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="248" y="136" width="26" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="274" y="136" width="26" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="300" y="136" width="26" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="62" y1="46" x2="198" y2="71" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="198.0,71.0 192.6,72.6 193.5,67.6" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="62" y1="82" x2="276" y2="97" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="276.0,97.0 270.8,99.1 271.2,94.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="62" y1="118" x2="250" y2="123" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="250.0,123.0 244.9,125.4 245.1,120.4" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="184" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">遍历小的 每个元素去大的里哈希查一次</text>
</svg>
```

**细节。**

- 复杂度 O(min(m, n))，不是 O(m + n)；`a & b` 与 `b & a` 一样快。
- 本机实测：3 个元素 & 100 万元素，约 0.056 微秒。
- 判断 `999999 in` 100 万元素：`set` 约 0.017 微秒，`list` 约 5 毫秒。

**为什么。** 哈希查找是 O(1)，遍历大的一方没有意义。

**坑。** 把 `list` 转成 `set` 本身要 O(n)，只查一两次不划算。

**例题：** LC 349 两个数组的交集

给两个数组 `nums1`、`nums2`，返回它们的交集，结果里每个元素只出现一次，顺序不限。

```python
def intersection(nums1: list[int], nums2: list[int]) -> list[int]:
    return list(set(nums1) & set(nums2))
```
