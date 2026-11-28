---
id: lct-learn-dp-3-1
node: dp.3.1
type: qa
step: 1
---
## Q
**动态规划 › 背包 › 0-1 背包**｜学习卡

套路是什么？

## A
**一句话。** 0-1 背包：每个物品选或不选，`f[i+1][j]` 只读上一行 `f[i]`，所以每个物品至多用一次；可行性、方案数、最优值只差合并方式。

下图：`f[i+1][j]` 只读上一行的「不选」和「选」两格。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<rect x="20" y="30" width="46" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="66" y="30" width="46" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="112" y="30" width="46" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="158" y="30" width="46" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="204" y="30" width="46" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="250" y="30" width="46" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="20" y="60" width="46" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="66" y="60" width="46" height="30" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="89.0" y="79.0" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor">f[i][j-x]</text>
<rect x="112" y="60" width="46" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="158" y="60" width="46" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="204" y="60" width="46" height="30" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="227.0" y="79.0" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor">f[i][j]</text>
<rect x="250" y="60" width="46" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="20" y="90" width="46" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="66" y="90" width="46" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="112" y="90" width="46" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="158" y="90" width="46" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="204" y="90" width="46" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="227.0" y="109.0" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">f[i+1][j]</text>
<rect x="250" y="90" width="46" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="14" y="24" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">j →</text>
<line x1="227.0" y1="84.0" x2="227.0" y2="93.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="227.0,93.0 224.0,86.7 230.0,86.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="99.0" y1="87.0" x2="209.0" y2="95.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="209.0,95.0 202.5,97.5 202.9,91.6" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="136" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">两个来源都在上一行：每个物品至多用一次</text>
<text x="4" y="66" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">i</text>
<text x="4" y="96" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">i+1</text>
<text x="120" y="100" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">选 x</text>
<text x="260" y="70" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">不选</text>
</svg>

```python
def knapsack(nums, target):      # 和恰为 target 的方案数
    n = len(nums)
    # f[i][j]：前 i 个数里选若干个、和恰为 j 的方案数
    f = [[0] * (target + 1) for _ in range(n + 1)]
    f[0][0] = 1                  # 一个都不选，和为 0
    for i, x in enumerate(nums):
        for j in range(target + 1):
            f[i + 1][j] = f[i][j]            # 不选 x
            if j >= x:
                f[i + 1][j] += f[i][j - x]   # 选 x，只读上一行
    return f[n][target]
```

**要点。**
- 为什么对？：第 `i` 个数选或不选，选了就从 `j - x` 转来；只读上一行意味着同一个数不会被重复用，读本行就变成完全背包。
- LC 416 怎么改？：总和为奇数直接失败，否则 `target = 总和 // 2`，看 `f[n][target] > 0`。
- LC 494 怎么改？：设取 `+` 的子集和为 `P = (总和 + target) / 2`，奇偶不对或 `P < 0` 返回 `0`，再用本模板数 `P`。
- LC 1049 怎么改？：分成两堆使差最小：`target = 总和 // 2`，取不超过它的最大可达和 `s`，答案 `总和 - 2s`。

**易错点。**
- 转移读本行 `f[i + 1][j - x]`：同一个数被重复用，`[1,1,1,1,1]`、`target = 3` 得 `70`，应为 `5`。
- LC 494 不判奇偶和 `P < 0`：`[1,1]`、`target = -3` 时 `P = -1`，建表后 `IndexError`。
- LC 494 过滤掉 `0`：每个 `0` 前 `+` 和 `-` 是两种表达式，方案数翻倍。

**对应题目。** LC 416 分割等和子集、LC 494 目标和、LC 1049 最后一块石头的重量 II
