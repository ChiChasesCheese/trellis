---
slug: minimum-score-by-changing-two-elements
---
## Q
**LC 2567 修改两个元素的最小分数**｜Medium

整数数组 `nums`（长度 ≥ 3），分数 = 任意两数差的最大值 + 最小值。最多改两个元素的值，求最小分数。

## A
**一句话。** 改的数可以抄成别的数，最小差总能变 0；只剩最大差，排序后从两端共删两个，枚举三种删法。

**图解。** 排序后灰格是被改掉的数，蓝格是留下的连续一段，它的极差就是分数。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 130">
<rect x="14" y="12" width="30" height="28" rx="1" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="29" y="30" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">a0</text>
<rect x="44" y="12" width="30" height="28" rx="1" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="59" y="30" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">a1</text>
<rect x="74" y="12" width="30" height="28" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.35" stroke="currentColor" stroke-width="1.2"/>
<text x="89" y="30" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">a2</text>
<rect x="104" y="12" width="30" height="28" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.35" stroke="currentColor" stroke-width="1.2"/>
<text x="119" y="30" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">a3</text>
<rect x="134" y="12" width="30" height="28" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.35" stroke="currentColor" stroke-width="1.2"/>
<text x="149" y="30" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">a4</text>
<rect x="164" y="12" width="30" height="28" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.35" stroke="currentColor" stroke-width="1.2"/>
<text x="179" y="30" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">a5</text>
<text x="204" y="30" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">改最小两个</text>
<rect x="14" y="50" width="30" height="28" rx="1" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="29" y="68" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">a0</text>
<rect x="44" y="50" width="30" height="28" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.35" stroke="currentColor" stroke-width="1.2"/>
<text x="59" y="68" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">a1</text>
<rect x="74" y="50" width="30" height="28" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.35" stroke="currentColor" stroke-width="1.2"/>
<text x="89" y="68" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">a2</text>
<rect x="104" y="50" width="30" height="28" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.35" stroke="currentColor" stroke-width="1.2"/>
<text x="119" y="68" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">a3</text>
<rect x="134" y="50" width="30" height="28" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.35" stroke="currentColor" stroke-width="1.2"/>
<text x="149" y="68" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">a4</text>
<rect x="164" y="50" width="30" height="28" rx="1" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="179" y="68" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">a5</text>
<text x="204" y="68" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">两头各改一个</text>
<rect x="14" y="88" width="30" height="28" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.35" stroke="currentColor" stroke-width="1.2"/>
<text x="29" y="106" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">a0</text>
<rect x="44" y="88" width="30" height="28" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.35" stroke="currentColor" stroke-width="1.2"/>
<text x="59" y="106" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">a1</text>
<rect x="74" y="88" width="30" height="28" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.35" stroke="currentColor" stroke-width="1.2"/>
<text x="89" y="106" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">a2</text>
<rect x="104" y="88" width="30" height="28" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.35" stroke="currentColor" stroke-width="1.2"/>
<text x="119" y="106" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">a3</text>
<rect x="134" y="88" width="30" height="28" rx="1" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="149" y="106" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">a4</text>
<rect x="164" y="88" width="30" height="28" rx="1" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="179" y="106" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">a5</text>
<text x="204" y="106" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">改最大两个</text>
<text x="14" y="126" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">答案 = 三段蓝色里 最右 − 最左 的最小值</text>
</svg>

```python
def minimize_sum(nums):
    a = sorted(nums)
    # 删两头共两个：左删 2 / 各删 1 / 右删 2
    return min(a[-3] - a[0],
               a[-2] - a[1],
               a[-1] - a[2])
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 想分开优化最小差：改成与留下的某数相等，最小差就是 0，不用另花修改次数。
- 只试「删最大两个」或「删最小两个」：两头各删一个也可能最优，三种都要比。

**追问。**
- 不排序能做吗？：只需最小三个和最大三个数，一次遍历维护，时间 `O(n)`。
- 改成最多改 `k` 个？：枚举左边删 `i` 个、右边删 `k - i` 个，取 `a[n-1-(k-i)] - a[i]` 最小。

**同模式。** LC 1509 三次操作后最大值与最小值的最小差、LC 1984 学生分数的最小差值、LC 908 最小差值 I、LC 910 最小差值 II
