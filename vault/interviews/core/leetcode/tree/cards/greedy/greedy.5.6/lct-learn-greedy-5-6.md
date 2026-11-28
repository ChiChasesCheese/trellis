---
id: lct-learn-greedy-5-6
node: greedy.5.6
type: qa
step: 1
---
## Q
**贪心算法 › 思维题 › 两次扫描**｜学习卡

套路是什么？

## A
**一句话。** 两次扫描：约束分左、右两个方向时，各扫一遍处理一个方向，第二遍和第一遍的结果取 `max`。

下图：LC 135，两个方向的约束各扫一遍；第二遍与第一遍取 `max`，两边都满足。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 130">
<text x="14" y="32" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ratings</text>
<rect x="110" y="14" width="50" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="135.0" y="32.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="160" y="14" width="50" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="185.0" y="32.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="210" y="14" width="50" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="235.0" y="32.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<text x="14" y="66" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">左 → 右</text>
<rect x="110" y="48" width="50" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="135.0" y="66.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="160" y="48" width="50" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="185.0" y="66.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="210" y="48" width="50" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="235.0" y="66.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<text x="14" y="100" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">右 → 左</text>
<rect x="110" y="82" width="50" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="135.0" y="100.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<rect x="160" y="82" width="50" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="185.0" y="100.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="210" y="82" width="50" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="235.0" y="100.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<text x="270" y="100" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">max 取并</text>
<text x="170" y="124" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">左邻约束扫一遍，右邻约束反着扫一遍，再取 max</text>
</svg>

```python
def candy(ratings):
    n = len(ratings)
    give = [1] * n                   # 每人至少 1 颗
    for i in range(1, n):            # 左到右：比左邻居高就多一颗
        if ratings[i] > ratings[i - 1]:
            give[i] = give[i - 1] + 1
    for i in range(n - 2, -1, -1):   # 右到左：比右邻居高也要满足
        if ratings[i] > ratings[i + 1]:
            give[i] = max(give[i], give[i + 1] + 1)
    return sum(give)
```

**要点。**
- 为什么对？：两个方向的约束互相独立，各自的最小满足值是下界；第二遍取 `max` 同时满足两边，且没有比这更省的。
- `O(1)` 额外空间怎么做？：一遍扫上坡 / 下坡：记上坡长、下坡长、坡顶糖数，下坡比坡顶还长时给坡顶补一颗。
- 孩子站成环怎么办？：找评分最小的孩子（他只要 `1` 颗），从他把环切开成线性问题。

**易错点。**
- 只扫一遍：`[1,0,2]` 只左到右得 `4`，应为 `5`。
- 第二遍直接赋值不取 `max`：`[1,2,3,1]` 会把 `3` 的糖压低，破坏第一遍结果，应为 `7`。
- 评分相等也要求更多：条件必须严格大于，`[2,2,2]` 应为 `3`。

**对应题目。** LC 135 分发糖果
