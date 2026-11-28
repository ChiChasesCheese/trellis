---
id: lct-learn-greedy-2-1
node: greedy.2.1
type: qa
step: 1
---
## Q
**贪心算法 › 区间贪心 › 区间覆盖**｜学习卡

套路是什么？

## A
**一句话。** 区间覆盖的贪心是隐式 BFS 分层：边扫当前层边记下一层能伸到的最远位置，扫到层末就必须再选一个，计一跳。

下图：LC 45，每一层是同样跳数能到的范围，扫到层末必须再跳一次。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 145">
<rect x="30" y="40" width="56" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="58.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="86" y="40" width="56" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="114.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="142" y="40" width="56" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="198" y="40" width="56" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="226.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="254" y="40" width="56" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="282.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<text x="58.0" y="84" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<text x="114.0" y="84" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<text x="170.0" y="84" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<text x="226.0" y="84" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<text x="282.0" y="84" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<line x1="30" y1="94" x2="30" y2="100" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="86" y1="94" x2="86" y2="100" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="30" y1="94" x2="86" y2="94" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="58.0" y="110" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">第 0 跳</text>
<line x1="86" y1="94" x2="86" y2="100" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="198" y1="94" x2="198" y2="100" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="86" y1="94" x2="198" y2="94" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="142.0" y="110" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">第 1 层</text>
<line x1="198" y1="94" x2="198" y2="100" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="310" y1="94" x2="310" y2="100" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="198" y1="94" x2="310" y2="94" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="254.0" y="110" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">第 2 层</text>
<text x="170" y="30" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">扫本层时记下一层最远 far；i == end 时 jumps += 1，end = far</text>
<text x="170" y="138" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">每一层 = 再跳一次能到的格子（隐式 BFS）</text>
</svg>

```python
def jump(nums):                  # 跳到最后一格的最少次数
    jumps = end = far = 0        # end：当前层的右边界
    for i in range(len(nums) - 1):   # 最后一格不用再跳
        far = max(far, i + nums[i])  # 本层能伸到的最远
        if i == end:             # 本层走完，必须再跳一次
            jumps += 1
            end = far            # 下一层的右边界
    return jumps
```

**要点。**
- 为什么对？：到 `end` 时，所有起点在 `end` 之内的选择都已看过；多跳一次一定选伸得最远的，不会比别的选择差。
- LC 1326 怎么改？：先预处理 `reach[l]` = 左端点为 `l` 的龙头能到的最远右端（左端点截到 `0`），再套同一个循环；到 `end` 时若 `far <= i` 无解返回 `-1`。
- 不保证能到达怎么办？：层末若 `far` 没有超过 `i`，说明卡住了，直接判无解（LC 55 就是只做这个判断）。

**易错点。**
- 循环扫到最后一格：`i == end` 会多计一跳，`[2,3,1,1,4]` 得 `3`，应为 `2`。
- 每次跳到 `nums[j]` 最大的格子：该比的是 `j + nums[j]`，`[3,3,1,2,1,1]` 按值挑得 `3`，应为 `2`。
- LC 1326 左端点不截断：`i - r < 0` 时 `reach[-3]` 写到数组尾部。

**对应题目。** LC 45 跳跃游戏 II、LC 1326 灌溉花园的最少水龙头数目
