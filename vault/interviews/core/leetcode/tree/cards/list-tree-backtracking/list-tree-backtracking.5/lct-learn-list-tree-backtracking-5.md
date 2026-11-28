---
id: lct-learn-list-tree-backtracking-5
node: list-tree-backtracking.5
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 其他递归/分治**｜学习卡

套路是什么？

## A
**一句话。** 三路划分分治：随机选主元，数组分成小于、等于、大于三堆；排序两侧都递归，选第 `k` 个只钻进答案所在的那一堆。

下图：随机主元 `p = 3` 把数组分成三堆；排序两侧都递归，选第 `k` 个只进一侧。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 160">
<rect x="20" y="40" width="33" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="36.5" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="53" y="40" width="33" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="69.5" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="86" y="40" width="33" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="102.5" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="119" y="40" width="33" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="135.5" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<rect x="152" y="40" width="33" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="168.5" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<rect x="185" y="40" width="33" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="201.5" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<rect x="218" y="40" width="33" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="234.5" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="251" y="40" width="33" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="267.5" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="284" y="40" width="33" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="300.5" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<line x1="20" y1="34" x2="20" y2="28" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="119" y1="34" x2="119" y2="28" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="20" y1="34" x2="119" y2="34" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="69.5" y="28" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">lo：&lt; p</text>
<line x1="119" y1="34" x2="119" y2="28" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="218" y1="34" x2="218" y2="28" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="119" y1="34" x2="218" y2="34" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="168.5" y="28" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">eq：= p（已就位）</text>
<line x1="218" y1="34" x2="218" y2="28" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="317" y1="34" x2="317" y2="28" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="218" y1="34" x2="317" y2="34" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="267.5" y="28" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">hi：&gt; p</text>
<text x="170" y="96" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">排序：lo、hi 都递归</text>
<text x="170" y="118" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">第 k 大：k ≤ |hi| → 钻进 hi</text>
<text x="170" y="134" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">k ≤ |hi| + |eq| → 答案就是 p</text>
<text x="170" y="150" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">否则钻进 lo，k 减去 |hi| + |eq|</text>
</svg>

```python
def quick_sort(a):
    if len(a) <= 1:
        return a
    p = random.choice(a)         # 随机主元，防有序输入退化
    lo = [x for x in a if x < p]
    eq = [x for x in a if x == p]    # 等于主元的已就位
    hi = [x for x in a if x > p]
    return quick_sort(lo) + eq + quick_sort(hi)

def kth_largest(a, k):           # 只递归答案所在的一侧
    p = random.choice(a)
    hi = [x for x in a if x > p]
    eq = a.count(p)
    if k <= len(hi):
        return kth_largest(hi, k)
    if k <= len(hi) + eq:
        return p
    lo = [x for x in a if x < p]
    return kth_largest(lo, k - len(hi) - eq)
```

**要点。**
- 为什么对？：等于主元的一堆位置已定，不用再排；选择只递归一侧，规模期望减半，总期望 `O(n)`；随机主元让期望成立。
- 要稳定或最坏 `O(n log n)` 怎么改？：归并排序（左右各排好再合并，稳定，额外 `O(n)`）或堆排序（原地）。
- 第 `k` 小怎么改？：第 `k` 小就是第 `n - k + 1` 大，或把比较方向对调。数据流里持续要第 `k` 大，用大小为 `k` 的小根堆。

**易错点。**
- 相等的值不单独成堆：全相同的数组每轮只排除一个，退化成 `O(n^2)`。
- 进小堆时忘了减 `k`：`[3,2,1]`、`k = 3`、主元 `2`，小堆里的 `k` 应是 `1`。
- 主元固定取第一个：已排序输入每轮只砍一个。

**对应题目。** LC 215 数组中的第 K 个最大元素、LC 912 排序数组
