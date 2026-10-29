---
id: uth-compose-spring-three-level-cache-4-why-three
node: compose.spring-three-level-cache
type: qa
step: 4
---
## Q
**为什么不是两层：第三层的工厂在等代理**｜Spring Framework · 7.0

只有“成品”和“半成品”两层缓存行不行？Spring 为什么还要多一层工厂？

## A
**背景。** 事务、`@Async`、切面靠代理（proxy，包住原对象、在调用前后加料的替身）实现，代理由后处理器在 Bean 初始化完成之后生成：A 的最终形态是代理。而 B 向 A 要对象时，A 还没走到那一步。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 192">
<text x="14" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">B 手里该拿哪个 A</text>
<rect x="12" y="70" width="50" height="30" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="37.0" y="89.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B</text>
<rect x="190" y="30" width="140" height="124" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="260" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A 代理 最终形态</text>
<rect x="210" y="64" width="100" height="40" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="260.0" y="88.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A 原对象</text>
<line x1="62" y1="82" x2="210" y2="82" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<polygon points="210.0,82.0 205.0,84.5 205.0,79.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="120" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">两层: 拿到原对象</text>
<polyline points="62,94 100,134 190,134" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="190.0,134.0 185.0,136.5 185.0,131.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="120" y="152" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">三层: 拿到代理</text>
<text x="170" y="182" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">拿到原对象 调用就绕过切面</text>
</svg>
```

| 方案 | 后果 |
|---|---|
| 实例化后立刻给每个 Bean 造代理 | 没有环的 Bean 也被提前代理，打乱“初始化后再代理” |
| 半成品表里放原对象 | B 拿到没有切面的原对象，调用绕过事务 |
| 只有工厂、没有二级表 | 每次来要都造一个新代理，邻居们拿到的不是同一个 |
| 三层 | 有环才造，只造一次，大家共用 |

**为什么。** 三级存的是工厂而不是对象：“要不要造代理”推迟到真有人来要的那一刻（`getEarlyBeanReference`）；二级把这次的结果记下来，保证大家拿到同一个。创建完成后，自动代理创建器发现这个 Bean 已经提前代理过，就不再造第二个。

**对应 LeetCode：** 无直接对应的题
