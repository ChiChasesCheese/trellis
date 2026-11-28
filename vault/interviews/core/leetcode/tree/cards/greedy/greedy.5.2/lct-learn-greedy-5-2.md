---
id: lct-learn-greedy-5-2
node: greedy.5.2
type: qa
step: 1
---
## Q
**贪心算法 › 思维题 › 脑筋急转弯**｜学习卡

套路是什么？

## A
**一句话。** 脑筋急转弯：不模拟最优过程，先想清楚答案的下界在哪里，再想怎么排顺序取到它。本题总耗时按预订时的快照记下，最小耗时就是座位数。

下图：先找答案下界，再找一种顺序取到它。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 140">
<rect x="60" y="30" width="44" height="36" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="82" y="53" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">A</text>
<rect x="110" y="30" width="44" height="36" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="132" y="53" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B</text>
<rect x="180" y="30" width="44" height="36" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="202" y="53" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C</text>
<rect x="230" y="30" width="44" height="36" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="252" y="53" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">D</text>
<text x="170" y="20" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">靠窗　　　　　　　　　　　靠窗</text>
<text x="170" y="92" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">下界：每个座位至少 1 秒 → 总耗时 ≥ 座位数</text>
<text x="170" y="110" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">先订靠窗 A、D 再订 B、C：每个都 1 秒，取到下界</text>
<text x="170" y="128" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">实际耗时按预订那一刻的快照记，退座就减掉</text>
</svg>

```python
class BusBooking:
    def __init__(self, n):
        self.cost = {}               # 座位 -> 预订时定下的耗时
        self.total = 0
    def toggle(self, seat):
        if seat in self.cost:        # 退座：减去当初存下的耗时
            self.total -= self.cost.pop(seat)
            return
        c = 1
        if seat[0] in "AD":          # 靠窗：邻座已订则 3 秒
            mid = "BC"["AD".index(seat[0])] + seat[1:]
            c = 3 if mid in self.cost else 1
        self.cost[seat] = c
        self.total += c
    def getTotalTime(self):
        return self.total
    def getMinTime(self):
        return len(self.cost)        # 靠窗先订，每个 1 秒
```

**要点。**
- 为什么最小耗时就是座位数？：把靠窗座位全排在中间座位之前订，没有座位会遇到已订的邻座，每个都只要 `1` 秒。
- 为什么不能重算总耗时？：耗时是预订瞬间的快照，退座只影响之后的预订，所以要把当时的耗时存下来。

**易错点。**
- 退座后按当前座位重算总耗时：`B3`、`A3`、退 `B3`，重算得 `1`，应为 `3`（`A3` 当初已付 `3` 秒）。
- 相邻关系记错（`A` 邻 `C`）：`C3`、`A3` 误得 `4`，应为 `2`。

**对应题目。** LC 4080 设计公交车座位预订系统
