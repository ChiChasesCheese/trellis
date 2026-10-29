---
id: uth-gaps-dp-join-order-3-geqo
node: gaps.dp-join-order
type: qa
step: 3
---
## Q
**表太多时放弃最优**｜PostgreSQL · 17

FROM 里有多少项时，PostgreSQL 不再逐层 DP？换成什么办法找连接顺序？

## A
**背景。** 逐层 DP 的运行时间随表数指数增长，手册说，穷举往往比「执行一个次优计划」损失的时间还长。

**结构。** `geqo_threshold` 默认 12：FROM 里有 12 项或更多，就改用基因算法（GEQO，genetic query optimization）。它把连接顺序当成旅行商问题，用整数串表示：`4-1-3-2` 是先连 4 和 1，再并入 3，再并入 2。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 206">
<rect x="40" y="12" width="240" height="28" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="160" y="30" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">随机造一批顺序  如 4-1-3-2</text>
<rect x="40" y="58" width="240" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="160" y="76" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">每个顺序交给标准规划器估成本</text>
<rect x="40" y="104" width="240" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="160" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">丢掉成本最高的</text>
<rect x="40" y="150" width="240" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="160" y="168" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">拿好顺序的片段拼出新顺序</text>
<line x1="160" y1="40" x2="160" y2="52" fill="none" stroke="currentColor" stroke-width="1.2"/>
<path d="M160,58 L157,52 L163,52 Z" fill="currentColor" stroke="none"/>
<line x1="160" y1="86" x2="160" y2="98" fill="none" stroke="currentColor" stroke-width="1.2"/>
<path d="M160,104 L157,98 L163,98 Z" fill="currentColor" stroke="none"/>
<line x1="160" y1="132" x2="160" y2="144" fill="none" stroke="currentColor" stroke-width="1.2"/>
<path d="M160,150 L157,144 L163,144 Z" fill="currentColor" stroke="none"/>
<line x1="280" y1="164" x2="316" y2="164" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="316" y1="164" x2="316" y2="26" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="316" y1="26" x2="290" y2="26" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M284,26 L290,23 L290,29 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<text x="160" y="198" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">重复到看过预设个数的顺序 取见过最好的</text>
</svg>
```

**细节。**

- 一个顺序的好坏，就是标准规划器估出的最低总成本
- 新顺序由成本低的顺序的片段拼成（交叉，crossover）
- `geqo_effort` 取 1 到 10，默认 5：越大搜得越久

**坑。** 不保证最优。算法随机，但每次规划都把随机数重置为 `geqo_seed`，同一条查询得到同一个计划；想换搜索路径，改 `geqo_seed`。

**对应 LeetCode：** 无直接对应的题
