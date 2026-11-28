---
id: lct-learn-greedy-8
node: greedy.8
type: qa
step: 1
---
## Q
**贪心算法 › 其他**｜学习卡

套路是什么？

## A
**一句话。** 其他贪心：每题找一个「一旦违反就必须调整」的信号——油量变负就换起点，回答相同的兔子凑满一组就开新组，超过目标的三元组直接丢。

下图：LC 134，`d = gas - cost`；油量一变负就把起点换到下一站并清零。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 145">
<text x="10" y="38" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">d</text>
<rect x="60" y="20" width="50" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-2</text>
<rect x="110" y="20" width="50" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="135.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-2</text>
<rect x="160" y="20" width="50" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="185.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-2</text>
<rect x="210" y="20" width="50" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="235.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="260" y="20" width="50" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="285.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="10" y="82" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">tank</text>
<rect x="60" y="64" width="50" height="28" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2"/>
<text x="85.0" y="82.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">-2</text>
<rect x="110" y="64" width="50" height="28" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2"/>
<text x="135.0" y="82.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">-2</text>
<rect x="160" y="64" width="50" height="28" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2"/>
<text x="185.0" y="82.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">-2</text>
<rect x="210" y="64" width="50" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="235.0" y="82.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<rect x="260" y="64" width="50" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="285.0" y="82.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">6</text>
<text x="85" y="108" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">清零</text>
<text x="135" y="108" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">清零</text>
<text x="185" y="108" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">清零</text>
<line x1="235" y1="108" x2="235" y2="94" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="235.0,94.0 238.0,100.3 232.0,100.3" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="235" y="122" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">start = 3</text>
<text x="170" y="140" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">tank &lt; 0：start..i 都当不了起点，换到 i+1</text>
</svg>

```python
def can_complete_circuit(gas, cost):
    total = tank = start = 0
    for i in range(len(gas)):
        d = gas[i] - cost[i]
        total += d               # 总净油量：判断有没有解
        tank += d                # 从 start 出发的当前油量
        if tank < 0:             # start..i 都当不了起点
            start, tank = i + 1, 0
    return start if total >= 0 else -1
```

**要点。**
- 为什么对？：从 `start` 到 `i` 第一次油量为负，则这一段里任何站作起点，到 `i` 时都比 `start` 出发的剩油更少，也会失败，起点直接跳到 `i + 1`；总油量够，唯一没被排除的起点就能绕一圈。
- LC 781 怎么改？：回答 `x` 的兔子同色成组，每组 `x + 1` 只；回答相同的 `count` 只需要 `ceil(count / (x + 1))` 组，总数是组数乘 `x + 1`。
- LC 1899 怎么改？：取 max 只会变大：任一分量超过目标的三元组丢弃，剩下的三个分量各要有一个恰好等于目标。
- LC 1041 怎么改？：只模拟一轮：回到原点，或朝向不再是北（至多四轮转回），就会绕环。

**易错点。**
- 漏掉 `total >= 0`：`gas = [2,3,4]`、`cost = [3,4,3]` 总油不够，却返回 `2`，应为 `-1`。
- LC 781 向下取整：`[1,1,1]` 得 `2`，应为 `4`，第三只要另起一组。
- LC 1041 只判回到原点：`"GL"` 一轮后在 `(0,1)` 朝西，会错判 `false`，应为 `true`。

**对应题目。** LC 134 加油站、LC 781 森林中的兔子、LC 1899 合并若干三元组以形成目标三元组、LC 1041 困于环中的机器人
