---
slug: find-score-of-an-array-after-marking-all-elements
---
## Q
**LC 2593 标记所有元素后数组的分数**｜Medium

反复选未标记的最小元素（相同取下标小的），把它加进分数，并标记它和左右相邻的元素，直到全部被标记。返回分数。

## A
**一句话。** 按（值，下标）排序后依次处理，跳过已标记的，选中就加分并标记左右邻居；排序顺序就是题目的选取顺序。

**图解。** 按（值，下标）顺序处理，圈号是被选中的次序，浅色格是被邻居标记后跳过的。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 150">
<rect x="40" y="34" width="36" height="26" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="58.0" y="51.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="76" y="34" width="36" height="26" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="94.0" y="51.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="112" y="34" width="36" height="26" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="130.0" y="51.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="148" y="34" width="36" height="26" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="166.0" y="51.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="184" y="34" width="36" height="26" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="202.0" y="51.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="220" y="34" width="36" height="26" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="238.0" y="51.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<text x="58.0" y="74" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<text x="94.0" y="74" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<text x="130.0" y="74" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<text x="166.0" y="74" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<text x="202.0" y="74" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<text x="238.0" y="74" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<text x="94.0" y="26" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">①</text>
<text x="238.0" y="26" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">②</text>
<text x="166.0" y="26" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">③</text>
<text x="40" y="102" text-anchor="start" font-size="10" font-family="sans-serif" fill="currentColor">按 (值, 下标) 依次看：1 选 → 2 已标记跳过</text>
<text x="40" y="120" text-anchor="start" font-size="10" font-family="sans-serif" fill="currentColor">→ 2 选 → 3 跳过 → 4 选 → 5 跳过</text>
<text x="40" y="142" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">分数 = 1 + 2 + 4 = 7</text>
</svg>

```python
def find_score(nums):
    n = len(nums)
    marked = [False] * (n + 1)  # 多一格，i+1 越界不用判
    score = 0
    order = sorted(range(n), key=lambda i: (nums[i], i))
    for i in order:
        if marked[i]:
            continue
        score += nums[i]
        marked[i] = marked[i - 1] = marked[i + 1] = True
    return score
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 只按值排序：相同值要按下标从小到大，否则选中的元素不同。
- `i = 0` 时 `marked[i - 1]` 是 `marked[-1]`：正好是多开的那一格，不会误标真实元素。

**追问。**
- 为什么排序后不用每次重新找最小？：标记只会让元素失效，不会改变剩余元素的相对顺序，所以按排好的顺序跳过失效的即可。
- 能做到 `O(n)` 吗？：可以按「严格递减段」切分，每段从末尾隔一个取一个；思路更巧，面试先给排序解。

**同模式。** LC 1046 最后一块石头的重量、LC 2558 从数量最多的堆取走礼物、LC 2530 执行 K 次操作后的最大分数
