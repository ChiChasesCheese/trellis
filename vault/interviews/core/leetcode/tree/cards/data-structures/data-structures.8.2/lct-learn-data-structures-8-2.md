---
id: lct-learn-data-structures-8-2
node: data-structures.8.2
type: qa
step: 1
---
## Q
**常用数据结构 › 树状数组和线段树 › 逆序对**｜学习卡

套路是什么？

## A
**一句话。** 逆序对就是「对每个数，数它右边（或左边）有多少个更小的」：离散化后用树状数组做单点加一、前缀求和，从右往左一边查一边插，总共 `O(n log n)`。

下图：从右往左扫，先查树里比 `x` 小的个数（前缀和），再把 `x` 插进去（单点加一）。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<text x="18" y="30" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">a</text>
<rect x="40" y="14" width="36" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="58.0" y="32.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<rect x="76" y="14" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="94.0" y="32.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="112" y="14" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="130.0" y="32.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<line x1="190" y1="28" x2="155" y2="28" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="155.0,28.0 161.3,25.0 161.3,31.0" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<text x="196" y="32" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">从右往左扫</text>
<text x="60" y="70" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">x</text>
<text x="130" y="70" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">查：比 x 小的个数</text>
<text x="270" y="70" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">插入后各值计数</text>
<text x="60" y="98" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<text x="130" y="98" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="225" y="80" width="30" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="240.0" y="97.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="255" y="80" width="30" height="26" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="270.0" y="97.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="285" y="80" width="30" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="300.0" y="97.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="60" y="130" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="130" y="130" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="225" y="112" width="30" height="26" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="240.0" y="129.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="255" y="112" width="30" height="26" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="270.0" y="129.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="285" y="112" width="30" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="300.0" y="129.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="60" y="162" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="130" y="162" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<rect x="225" y="144" width="30" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="240.0" y="161.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="255" y="144" width="30" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="270.0" y="161.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="285" y="144" width="30" height="26" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="300.0" y="161.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="240.0" y="186" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">值1</text>
<text x="270.0" y="186" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">值2</text>
<text x="300.0" y="186" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">值3</text>
<text x="130" y="186" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ans = 2</text>
</svg>

```python
def count_inversions(a):
    vals = sorted(set(a))            # 离散化：值 -> 1..m
    m = len(vals)
    tree = [0] * (m + 1)             # 树状数组：出现次数
    ans = 0
    for x in reversed(a):            # 右边的数先入树
        r = bisect_left(vals, x)     # 严格小于 x 的个数
        i = r
        while i > 0:                 # 查询前缀和
            ans += tree[i]
            i &= i - 1
        i = r + 1                    # x 自己的排名
        while i <= m:                # 单点加一
            tree[i] += 1
            i += i & -i
    return ans
```

**要点。**
- 为什么对？：从右往左处理时，树里装的正是 `x` 右边的数，前缀和 `[1, rank(x) - 1]` 就是其中比 `x` 小的个数，逐个累加得到全部逆序对。
- LC 493 怎么改？：条件是 `x > 2 * y`：查询位置改成 `bisect_left(vals, (x + 1) // 2)`，即值严格小于 `x / 2` 的个数，插入仍按 `x` 自己的排名。
- 归并排序怎么做？：两半各自排好后，用单调指针在合并前数出跨两半的对数，`O(n log n)`，不用离散化；493 的条件和合并的比较不同，要单独扫一遍再合并。

**易错点。**
- 条件写成 `>=`：逆序对要求严格大于，`[2,2]` 应得 `0`。
- 先插入再查询：`x` 会数到自己，或者数到比自己靠左的数。
- 树状数组下标从 `0` 开始：`i & -i` 在 `0` 处死循环，下标必须从 `1` 起。

**对应题目。** LC 493 翻转对
