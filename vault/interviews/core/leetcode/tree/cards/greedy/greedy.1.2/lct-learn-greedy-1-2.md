---
id: lct-learn-greedy-1-2
node: greedy.1.2
type: qa
step: 1
---
## Q
**贪心算法 › 贪心策略 › 单序列配对**｜学习卡

套路是什么？

## A
**一句话。** 排序后对撞双指针：最重的一定占一个位置，最轻的能搭上就一起走，搭不上则最重的单独走。

下图：LC 881，排序后对撞双指针，最重的每轮必上船。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 145">
<rect x="40" y="50" width="60" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="70.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<rect x="100" y="50" width="60" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="130.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="160" y="50" width="60" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="190.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="220" y="50" width="60" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="250.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<line x1="70.0" y1="34" x2="70.0" y2="48" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="70.0,48.0 67.0,41.7 73.0,41.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="70.0" y="30" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">lo 最轻</text>
<line x1="250.0" y1="34" x2="250.0" y2="48" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="250.0,48.0 247.0,41.7 253.0,41.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="250.0" y="30" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">hi 最重</text>
<text x="170" y="104" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">轻 + 重 ≤ limit：一起走，lo += 1</text>
<text x="170" y="122" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">不论搭没搭上：最重的上船，hi -= 1</text>
<text x="170" y="140" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">limit = 3：[3]、[1,2]、[2] → 3 条船</text>
</svg>

```python
def num_rescue_boats(people, limit):
    people.sort()
    lo, hi = 0, len(people) - 1
    boats = 0
    while lo <= hi:                  # lo == hi 时最后一人也要一船
        if people[lo] + people[hi] <= limit:
            lo += 1                  # 最轻的搭上最重的
        hi -= 1                      # 最重的一定上船
        boats += 1
    return boats
```

**要点。**
- 为什么对？：最重的人必占一艘船；最轻的都带不上，就没人能和他同船；带得上则带最轻的最划算，留下的人更重也不会更差。
- 要配对和恰为 `target`（LC 1679）怎么改？：排序对撞：和小则 `lo` 右移，和大则 `hi` 左移，相等则配成一对两边同移。

**易错点。**
- 没排序就双指针：`[3,2,2,1]`、`limit = 3` 得 `4`，应为 `3`。
- 循环写成 `lo < hi`：漏掉最后单独一人，`[5]` 得 `0`。
- 让最轻的两人配对：`[1,1,3,3]`、`limit = 4` 得 `3`，应为 `2`。

**对应题目。** LC 881 救生艇
