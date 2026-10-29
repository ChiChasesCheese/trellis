---
id: uth-gaps-union-find-4-join-domain
node: gaps.union-find
type: qa
step: 4
---
## Q
**等价类什么时候不能乱推**｜PostgreSQL · 17

`a LEFT JOIN b ON a.x = b.y AND a.x = 42`：规划器可以在扫描 `b` 时就过滤 `b.y = 42`，却不能在扫描 `a` 时过滤 `a.x = 42`。为什么？

## A
**背景。** LEFT JOIN 要保留 `a` 的每一行，右边配不上就补 NULL。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 204">
<text x="60" y="20" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">表 a</text>
<text x="280" y="20" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">表 b</text>
<rect x="30" y="34" width="60" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="60" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">x = 7</text>
<rect x="30" y="76" width="60" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="60" y="92" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">x = 42</text>
<rect x="30" y="118" width="60" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="60" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">x = 9</text>
<rect x="250" y="58" width="60" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="280" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">y = 42</text>
<rect x="250" y="100" width="60" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="280" y="116" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">y = 5</text>
<line x1="90" y1="88" x2="250" y2="70" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<text x="100" y="50" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">右边补 NULL</text>
<text x="100" y="134" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">右边补 NULL</text>
<text x="14" y="170" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">错 扫描 a 时就丢掉 7 和 9 结果会少两行</text>
<text x="14" y="192" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">对 扫描 b 时丢掉 y = 5 它配不上任何行</text>
</svg>
```

**细节。**

- `b` 里 `y` 不等于 42 的行，本来就配不上任何满足 `a.x = 42` 的行，提前丢掉不影响结果
- `a` 里 `x` 不等于 42 的行，结果里本该以「右边全是 NULL」的样子出现，提前丢掉就少了行

**结构。** 所以等价类只在连接域（join domain）内成立：彼此内连接的一组表是一个域，每个外连接再给它可为空的那一侧另开一个域。

**坑。** `a LEFT JOIN (SELECT * FROM b WHERE b.z = 1) b ON a.x = b.y WHERE a.x = 1`：两处都是「等于 1」，却不能把 `a.x`、`b.z` 并进同一个类，否则会错误地得出 `a.x = b.z`。

**对应 LeetCode：** 无直接对应的题
