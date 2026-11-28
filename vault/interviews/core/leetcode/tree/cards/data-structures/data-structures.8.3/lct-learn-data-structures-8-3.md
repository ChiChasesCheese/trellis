---
id: lct-learn-data-structures-8-3
node: data-structures.8.3
type: qa
step: 1
---
## Q
**常用数据结构 › 树状数组和线段树 › 线段树（无区间更新）**｜学习卡

套路是什么？

## A
**一句话。** 线段树每个节点存一段区间的聚合值（这里是最大值）：单点修改自底向上重算 `O(log n)` 个祖先，区间查询拆成 `O(log n)` 个整节点。

下图：`size = 8`，叶子在 `tree[8:16]`，`i` 的孩子是 `2i`、`2i+1`；区间查询从两端往上拼出几个整节点。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 222">
<line x1="95.0" y1="61" x2="170.0" y2="37" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="245.0" y1="61" x2="170.0" y2="37" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="57.5" y1="109" x2="95.0" y2="85" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="132.5" y1="109" x2="95.0" y2="85" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="207.5" y1="109" x2="245.0" y2="85" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="282.5" y1="109" x2="245.0" y2="85" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="38.75" y1="157" x2="57.5" y2="133" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="76.25" y1="157" x2="57.5" y2="133" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="113.75" y1="157" x2="132.5" y2="133" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="151.25" y1="157" x2="132.5" y2="133" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="188.75" y1="157" x2="207.5" y2="133" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="226.25" y1="157" x2="207.5" y2="133" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="263.75" y1="157" x2="282.5" y2="133" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="301.25" y1="157" x2="282.5" y2="133" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<circle cx="170.0" cy="25" r="12" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="29" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<circle cx="95.0" cy="73" r="12" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="95.0" y="77" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">2</text>
<circle cx="245.0" cy="73" r="12" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="245.0" y="77" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">3</text>
<circle cx="57.5" cy="121" r="12" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="57.5" y="125" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">4</text>
<circle cx="132.5" cy="121" r="12" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="132.5" y="125" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">5</text>
<circle cx="207.5" cy="121" r="12" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="207.5" y="125" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">6</text>
<circle cx="282.5" cy="121" r="12" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="282.5" y="125" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">7</text>
<rect x="23.75" y="157" width="30" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="38.75" y="173" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">8</text>
<text x="38.75" y="195" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">[0]</text>
<rect x="61.25" y="157" width="30" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="76.25" y="173" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">9</text>
<text x="76.25" y="195" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">[1]</text>
<rect x="98.75" y="157" width="30" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="113.75" y="173" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">10</text>
<text x="113.75" y="195" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">[2]</text>
<rect x="136.25" y="157" width="30" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="151.25" y="173" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">11</text>
<text x="151.25" y="195" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">[3]</text>
<rect x="173.75" y="157" width="30" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="188.75" y="173" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">12</text>
<text x="188.75" y="195" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">[4]</text>
<rect x="211.25" y="157" width="30" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="226.25" y="173" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">13</text>
<text x="226.25" y="195" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">[5]</text>
<rect x="248.75" y="157" width="30" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="263.75" y="173" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">14</text>
<text x="263.75" y="195" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">[6]</text>
<rect x="286.25" y="157" width="30" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="301.25" y="173" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">15</text>
<text x="301.25" y="195" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">[7]</text>
<text x="170" y="216" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">query [2, 7) 取走 5、6、14 三个整节点</text>
</svg>

```python
size = n                         # 叶子在 tree[size : 2*size]
tree = [0] * (2 * size)

def update(i, v):                # 单点改，再向上重算
    i += size
    tree[i] = v
    while i > 1:
        i >>= 1
        tree[i] = max(tree[2 * i], tree[2 * i + 1])

def query(l, r):                 # 半开区间 [l, r) 的最大值
    res = 0                      # 最大值的单位元
    l, r = l + size, r + size
    while l < r:
        if l & 1:                # l 是右孩子：整节点取走
            res = max(res, tree[l]); l += 1
        if r & 1:                # r 是右孩子：取走 r-1
            r -= 1; res = max(res, tree[r])
        l, r = l >> 1, r >> 1
    return res
```

**要点。**
- 为什么对？：内部节点 = 两个孩子的聚合；改一个叶子只影响它到根的一条链。查询区间从两端向上收拢，落在右孩子的端点就取走，其余交给父节点。
- LC 3161 怎么改？：叶子 `x` 存「以障碍物 `x` 结尾的空隙长度」；放障碍物 `x` 时更新 `x` 自己，并把后继障碍物的空隙截短；查询 `[0, x]` 取最大空隙，再和最后一段 `x - 前驱` 比，`>= sz` 即可。
- 求和或最小怎么改？：把 `max` 换成 `+` 或 `min`，单位元换成 `0` 或 `inf`；区间更新要改用懒标记（下一张卡）。

**易错点。**
- 半开区间写成闭区间：查 `[0, x]` 要写 `query(0, x + 1)`，否则漏掉 `x`。
- 放障碍物只更新自己：后继障碍物的空隙被截短了，也要重写。
- 没放原点哨兵：第一块障碍物找不到前驱，用 `obs = [0]` 当哨兵再 `bisect`。

**对应题目。** LC 3161 物块放置查询
