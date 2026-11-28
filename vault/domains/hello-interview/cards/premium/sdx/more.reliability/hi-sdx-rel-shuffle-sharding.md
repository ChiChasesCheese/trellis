---
id: hi-sdx-rel-shuffle-sharding
node: more.reliability
type: qa
step: 8
---
## Q
**洗牌分片：把爆炸半径从 25% 降到 3.6%**｜补充 · 可靠性 · 追问

面试官：「8 个节点，一个客户端发来能打崩节点的请求（毒药请求）。固定分成 4 组，每组 2 个节点，会影响多少客户？换成给每个客户分配随机 2 个节点的组合呢？」

## A
**结论。** 固定分片：毒药客户打死自己那一组，同组客户全挂，占 1/4。洗牌分片（shuffle sharding）：每个客户一对随机节点，共 C(8,2)=28 种，只有恰好同一对的客户才全挂，约 1/28≈3.6%。

**要点。**
- **固定分片：** 4 组各 2 个节点，毒药客户拖垮整组，爆炸半径 25%，且是 100% 影响。
- **洗牌分片：** 每个客户一个随机的两节点组合，称为虚拟分片。
- **只重合一个节点：** 大多数重叠的客户只共享一个节点，请求在另一个节点上重试成功。
- **组合增长：** 节点数增加，组合数飞快增长，100 选 5 约 7500 万，隔离度接近单租户，硬件不变。
- **前提：** 客户端或路由层必须真的在组内节点间重试，否则部分重叠也得不到保护。

**为什么。** 隔离靠的是组合数学，不靠买更多机器。同样 8 台机器，被同一个毒药客户波及的比例从 1/4 缩到 1/28。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 268">
<text x="8" y="18" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">固定分片：4 组，每组 2 个节点</text>
<rect x="10" y="28" width="32" height="28" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="26" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="50" y="28" width="32" height="28" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="66" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="90" y="28" width="32" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="106" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="130" y="28" width="32" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="146" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="170" y="28" width="32" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="186" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="210" y="28" width="32" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="226" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<rect x="250" y="28" width="32" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="266" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="290" y="28" width="32" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="306" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<text x="8" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">毒药客户端打死节点 1、2：1/4 的客户全挂</text>
<text x="8" y="108" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">洗牌分片：每个客户一对随机节点</text>
<rect x="10" y="118" width="32" height="28" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="26" y="136" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="50" y="118" width="32" height="28" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="66" y="136" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="90" y="118" width="32" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="106" y="136" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="130" y="118" width="32" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="146" y="136" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="170" y="118" width="32" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="186" y="136" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="210" y="118" width="32" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="226" y="136" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<rect x="250" y="118" width="32" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="266" y="136" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="290" y="118" width="32" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="306" y="136" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<text x="8" y="170" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">客户 X 用 2、5：节点 2 坏，重试到 5 成功</text>
<text x="8" y="194" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">客户 Y 用 1、2：两个都坏，全挂</text>
<text x="8" y="222" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">C(8,2) = 28 种组合</text>
<text x="8" y="242" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只有恰好同一对的客户全挂：1/28 ≈ 3.6%</text>
</svg>

**面试里这样说。** 「我给每个租户分配一个随机的两节点组合，8 台里有 28 种。毒药客户只会让与它完全相同组合的租户全挂，约 3.6%，其余只丢一个节点，靠重试到另一个节点就能成功。」

**易错。**
- **客户端不会重试：** 重叠一个节点的客户也失败，隔离效果归零。
- **组合太小：** 节点或组合数太少，仍有大量客户完全重合。
- **把它当容量方案：** 它只限制故障波及面，不增加吞吐。
