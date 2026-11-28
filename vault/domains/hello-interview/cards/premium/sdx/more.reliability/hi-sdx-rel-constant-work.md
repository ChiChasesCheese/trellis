---
id: hi-sdx-rel-constant-work
node: more.reliability
type: qa
step: 12
---
## Q
**恒定工作：故障时工作量不变**｜补充 · 可靠性 · 加分

面试官：「恒定工作（constant work）模式说，可靠系统在平静和大规模故障时应做同样多的工作，比如健康检查结果每隔几秒整份推送，而不是变化时才推增量。这样做换来了什么？」

## A
**结论。** 换来的是故障模式等于正常模式：没有突发的工作洪峰，没有恢复时的积压，错过的更新被下一轮整份覆盖，容量按已知的恒定负载配置即可。代价是故意浪费，只适合小载荷、高风险的控制面。

**要点。**
- **增量系统的问题：** 平静时几乎不做事，大量变化同时发生时工作量暴涨，最忙的时刻恰好是最没测过的时刻。
- **单一模式：** 恒定工作只有一个模式，每隔几秒就演练一次。
- **没有恢复洪峰：** 分区或崩溃后没有要回放的积压，下一轮整份覆盖，恢复成本等于日常成本。
- **自愈：** 整份替换是幂等的，丢失或损坏的更新被下一轮纠正，不要求每个增量恰好一次、按序到达。
- **代价：** 总在做最大工作量，所以适用于健康检查、配置这类小载荷控制面，不适合数据面。

**为什么。** 系统最脆弱的时刻是负载突变的时刻。让负载永远不变，等于把这个脆弱时刻消除。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<text x="8" y="18" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">工作量随时间变化</text>
<text x="8" y="42" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">增量推送</text>
<rect x="20" y="94" width="30" height="6" rx="3" stroke-width="1" fill="currentColor" fill-opacity="0.18" stroke="currentColor"/>
<rect x="58" y="94" width="30" height="6" rx="3" stroke-width="1" fill="currentColor" fill-opacity="0.18" stroke="currentColor"/>
<rect x="96" y="94" width="30" height="6" rx="3" stroke-width="1" fill="currentColor" fill-opacity="0.18" stroke="currentColor"/>
<rect x="134" y="44" width="30" height="56" rx="3" stroke-width="1" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="172" y="50" width="30" height="50" rx="3" stroke-width="1" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="210" y="92" width="30" height="8" rx="3" stroke-width="1" fill="currentColor" fill-opacity="0.18" stroke="currentColor"/>
<rect x="248" y="94" width="30" height="6" rx="3" stroke-width="1" fill="currentColor" fill-opacity="0.18" stroke="currentColor"/>
<rect x="286" y="94" width="30" height="6" rx="3" stroke-width="1" fill="currentColor" fill-opacity="0.18" stroke="currentColor"/>
<line x1="14" y1="100" x2="330" y2="100" stroke-width="1.2" stroke="currentColor"/>
<text x="8" y="124" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">大面积故障时（第 4、5 格）工作量暴涨</text>
<text x="8" y="152" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">整份推送</text>
<rect x="20" y="174" width="30" height="22" rx="3" stroke-width="1" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="58" y="174" width="30" height="22" rx="3" stroke-width="1" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="96" y="174" width="30" height="22" rx="3" stroke-width="1" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="134" y="174" width="30" height="22" rx="3" stroke-width="1" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="172" y="174" width="30" height="22" rx="3" stroke-width="1" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="210" y="174" width="30" height="22" rx="3" stroke-width="1" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="248" y="174" width="30" height="22" rx="3" stroke-width="1" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="286" y="174" width="30" height="22" rx="3" stroke-width="1" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<line x1="14" y1="196" x2="330" y2="196" stroke-width="1.2" stroke="currentColor"/>
<text x="8" y="212" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">每格相同，没有洪峰也没有积压</text>
</svg>

**面试里这样说。** 「对健康检查和配置分发这类控制面，我选恒定工作：每隔几秒整份推送全部状态，而不是推增量。这样大面积故障时负载不变，恢复时也没有积压要追。」

**易错。**
- **用在数据面：** 总是推全量，带宽和算力浪费巨大。
- **全量文件太大：** 超过固定预算，恒定工作变成恒定过载。
- **仍保留增量路径：** 又回到双模式，紧急模式没人测。
