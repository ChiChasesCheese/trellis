---
id: hi-sdx-arch-sync-chain
node: more.architecture
type: qa
step: 3
---
## Q
**同步调用链拖垮可用性**｜补充 · 服务架构：微服务、服务发现、Serverless · 必会

面试官：「一个请求要同步穿过 5 个服务，每个服务的可用性都是 99.9%。整条链的可用性和延迟会怎样？你有什么办法？」

## A
**结论。** 可用性相乘：0.999 的 5 次方约为 99.5%，每月不可用时间从约 43 分钟涨到约 3.6 小时（按 30 天算）；延迟逐跳累加。出路有三条：合并边界、改异步、把需要的数据放到本地，让这一跳离开请求路径。

**要点。**
- **串联的硬依赖：** 每一跳都是必经之路，任何一跳挂了，整个请求失败。
- **延迟累加：** 总耗时是各跳之和，整条链的慢取决于每个请求碰到的最慢那一跳；每一跳还要各自的超时和重试预算。
- **合并边界：** 两个服务总是同步互相调用，多半本来就该是一个服务。
- **改异步：** 调用方不需要立刻拿到答案的步骤（通知、审计），用队列或事件代替 RPC。
- **本地缓存或复制数据：** 通过事件把需要的数据复制到本地，这一跳就从请求路径上消失。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 196">
<rect x="8" y="10" width="60" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="38.0" y="29.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">服务A</text>
<text x="38.0" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">99.9%</text>
<polyline points="68,33 67.0,33.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="74,33 67.0,36.2 67.0,29.8" style="fill:var(--accent,#3b6fd4)"/>
<rect x="74" y="10" width="60" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="104.0" y="29.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">服务B</text>
<text x="104.0" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">99.9%</text>
<polyline points="134,33 133.0,33.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="140,33 133.0,36.2 133.0,29.8" style="fill:var(--accent,#3b6fd4)"/>
<rect x="140" y="10" width="60" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="29.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">服务C</text>
<text x="170.0" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">99.9%</text>
<polyline points="200,33 199.0,33.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="206,33 199.0,36.2 199.0,29.8" style="fill:var(--accent,#3b6fd4)"/>
<rect x="206" y="10" width="60" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="236.0" y="29.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">服务D</text>
<text x="236.0" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">99.9%</text>
<polyline points="266,33 265.0,33.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="272,33 265.0,36.2 265.0,29.8" style="fill:var(--accent,#3b6fd4)"/>
<rect x="272" y="10" width="60" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="302.0" y="29.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">服务E</text>
<text x="302.0" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">99.9%</text>
<text x="8" y="84" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">可用性相乘：0.999 的 5 次方 ≈ 99.5%</text>
<text x="8" y="104" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每月不可用：约 43 分钟 → 约 3.6 小时</text>
<text x="8" y="124" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">延迟逐跳累加，慢的取决于最慢那一跳</text>
<line x1="8" y1="138" x2="332" y2="138" stroke-width="1" stroke="currentColor" opacity="0.4" stroke-dasharray="3 3"/>
<text x="8" y="160" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">①合并边界  ②改异步（队列/事件）</text>
<text x="8" y="180" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">③本地缓存或复制数据，让这一跳消失</text>
</svg>

**面试里这样说。** 「五跳同步串联，每跳 99.9%，整体只剩 99.5%。我会先看哪几跳能合并，不需要即时答案的改成事件，剩下的靠本地缓存去掉。调用链深度应该是架构评审的一个指标。」

**易错。**
- **只加重试：** 重试给每一跳都叠加了负载，下游一慢就放大成重试风暴。
- **把依赖都画成同步箭头：** 先问「调用方现在就需要答案吗」，再决定同步还是异步。
