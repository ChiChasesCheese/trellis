---
id: uth-gaps-heuristics-4-spread-vs-pack
node: gaps.heuristics
type: qa
step: 4
---
## Q
**打分是价值观：摊开还是塞满**｜Kubernetes · 1.37

同样是「选分最高的机器」，调度器的默认打分把 Pod 摊开，换一条公式就能把 Pod 塞满。两者差在哪？

## A
**结构。** 打分插件 `NodeResourcesFit` 有三种策略，默认 `LeastAllocated`，另有 `MostAllocated`。两个公式只差一步：

- `LeastAllocated`：（容量 − 放入后已用）× 100 ÷ 容量，越空分越高，结果是摊开
- `MostAllocated`：放入后已用 × 100 ÷ 容量，越满分越高，结果是塞满（文档称之为装箱，bin packing）

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 180">
<text x="215" y="18" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">摊开</text>
<text x="295" y="18" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">塞满</text>
<text x="215" y="34" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">Least</text>
<text x="295" y="34" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">Most</text>
<text x="12" y="66" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">A</text>
<rect x="34" y="50" width="30" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="66" y="50" width="30" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="98" y="50" width="30" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="130" y="50" width="30" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="98" y="50" width="30" height="22" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="113" y="65" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">P</text>
<rect x="195" y="50" width="40" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="215" y="65" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">25</text>
<rect x="275" y="50" width="40" height="22" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="295" y="65" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">75</text>
<text x="12" y="106" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">B</text>
<rect x="34" y="90" width="30" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="66" y="90" width="30" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="98" y="90" width="30" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="130" y="90" width="30" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="34" y="90" width="30" height="22" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="49" y="105" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">P</text>
<rect x="195" y="90" width="40" height="22" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="215" y="105" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">75</text>
<rect x="275" y="90" width="40" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="295" y="105" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">25</text>
<text x="170" y="148" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">新 Pod 要 1 核  每台 4 核  A 已用 2 核</text>
<text x="170" y="170" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">摊开选 B (更空)  塞满选 A (更满)</text>
</svg>
```

**为什么。** 摊开让每台机器留有余量，负载突增时更从容；塞满让 Pod 集中，容易空出整台机器，方便缩容。两种都是贪心，差别只在你想优化什么。

**坑。** 策略要写进调度器配置才生效；不配置就一直是摊开。

**对应 LeetCode：** 无直接对应的题
