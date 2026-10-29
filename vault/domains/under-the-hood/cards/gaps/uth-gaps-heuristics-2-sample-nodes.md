---
id: uth-gaps-heuristics-2-sample-nodes
node: gaps.heuristics
type: qa
step: 2
---
## Q
**5000 台机器不全看**｜Kubernetes · 1.37

集群有 5000 台机器，调度器给每个 Pod 打分时，真的要把 5000 台都检查一遍吗？

## A
**背景。** 过滤要对每台机器逐个检查（资源、污点、亲和性……），节点越多，每个 Pod 等得越久；而其中很多台的分数通常差别不大。

**结构。** 调度器不检查全部：并行检查，一找到足够多台「可行」的机器就停，只给这些打分。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 138">
<text x="170" y="18" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">按顺序检查 找够 N 个可行节点就停</text>
<rect x="16" y="40" width="20" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<rect x="38" y="40" width="20" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<rect x="60" y="40" width="20" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<rect x="82" y="40" width="20" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<rect x="104" y="40" width="20" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="126" y="40" width="20" height="20" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="148" y="40" width="20" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="170" y="40" width="20" height="20" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="192" y="40" width="20" height="20" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="214" y="40" width="20" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="236" y="40" width="20" height="20" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="258" y="40" width="20" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<rect x="280" y="40" width="20" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<rect x="302" y="40" width="20" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<line x1="114" y1="82" x2="114" y2="70" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M114,64 L117,70 L111,70 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<text x="114" y="98" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">本次从这开始</text>
<line x1="268" y1="82" x2="268" y2="70" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M268,64 L271,70 L265,70 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<text x="268" y="98" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">下次从这开始</text>
<text x="170" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">蓝框 = 可行  黑框 = 不可行  虚线 = 没检查</text>
</svg>
```

**细节。**

- `percentageOfNodesToScore` 默认 0，表示自适应：百分比 = 50 − 节点数 ÷ 125，不低于 5%，至少 100 台；不足 100 台就全看
- 下一个 Pod 从上次停下的位置接着查，让每台都有机会被查到

| 节点数 | 百分比 | 检查到几台可行就停 |
|---|---|---|
| 1000 | 42% | 420 |
| 5000 | 10% | 500 |
| 10000 | 5% | 500 |

**为什么。** 用「可能错过更优的机器」换调度速度。

**对应 LeetCode：** 无直接对应的题
