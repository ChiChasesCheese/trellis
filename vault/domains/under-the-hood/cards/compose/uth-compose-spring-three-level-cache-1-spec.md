---
id: uth-compose-spring-three-level-cache-1-spec
node: compose.spring-three-level-cache
type: qa
step: 1
---
## Q
**单例 Bean 互相依赖：为什么一张表不够**｜Spring Framework · 7.0

Spring 创建单例 Bean（容器里只保留一份的对象）A 时要先有 B，创建 B 时又要先有 A。怎么避免无限递归？只用一张“名字 → 对象”的表行吗？

## A
**背景。** 创建一个 Bean 分三步：实例化（`new` 出对象）、注入依赖（给字段赋值，要去“拿”别的 Bean）、初始化。A 的字段要 B，B 的字段要 A，就成了循环依赖。

| 操作 | 要求 |
|---|---|
| 取成品 | 每次取 Bean 都走这里，要快，尽量不加锁 |
| 判断某个名字是否正在创建 | O(1) |
| 把造到一半的对象借给环上的邻居 | 只在真有环时才做 |
| 创建完成 | 所有人最终拿到同一个对象 |

**难点。** 只有一张成品表：创建 A → 要 B → 创建 B → 要 A，表里还没有 A，于是又去创建 A，无限递归。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 178">
<text x="14" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只有一张成品表时</text>
<rect x="12" y="30" width="64" height="30" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="44.0" y="49.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">造 A</text>
<rect x="96" y="30" width="64" height="30" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="128.0" y="49.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">要 B</text>
<rect x="180" y="30" width="64" height="30" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="212.0" y="49.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">造 B</text>
<rect x="264" y="30" width="64" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="296.0" y="49.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">要 A</text>
<line x1="76" y1="45" x2="96" y2="45" stroke-width="1.2" stroke="currentColor"/>
<polygon points="96.0,45.0 91.0,47.5 91.0,42.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="160" y1="45" x2="180" y2="45" stroke-width="1.2" stroke="currentColor"/>
<polygon points="180.0,45.0 175.0,47.5 175.0,42.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="244" y1="45" x2="264" y2="45" stroke-width="1.2" stroke="currentColor"/>
<polygon points="264.0,45.0 259.0,47.5 259.0,42.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="296,60 296,92 44,92 44,62" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)" stroke-dasharray="4 3"/>
<polygon points="44.0,62.0 46.5,67.0 41.5,67.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">表里还没有 A 又去造 A 无限递归</text>
<text x="170" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">加个集合只能发现环 解决不了</text>
<text x="170" y="160" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">B 此刻就要 A 这个对象</text>
</svg>
```

加一个“正在创建”的集合只能发现环并报错；B 此刻要的就是 A 这个对象，必须把造到一半的 A 先借出去。成品表要快读、不加锁，不能混进半成品，所以半成品另开一张表。

**对应 LeetCode：** 无直接对应的题
