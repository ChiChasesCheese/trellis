---
id: hi-sdx-repl-siblings
node: more.replication
type: qa
step: 7
---
## Q
**多主冲突：晚发现与兄弟版本**｜补充 · 复制 · 追问

面试官：「多主复制里两个 leader 同时写了同一个键。为什么这比单主的冲突难处理？副本怎么判断两个写是并发的，而不是后者覆盖前者？判出并发后怎么办？」

## A
**结论。** 多主里两个写都在本地立刻确认，冲突要到异步交换日志时才浮现，请求路径上已没有人可问，所以合并必须自动且确定，或把两个版本都留下。判定靠版本向量：新版本逐位不小于已存版本才算覆盖，有升有降就是并发。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 196">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">两个 leader A、B；已存版本 {A:2, B:1}</text>
<rect x="10" y="28" width="176" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="98.0" y="46.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">新写 {A:2, B:2}</text>
<text x="98.0" y="61.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">A 持平，B 更大</text>
<polyline points="186,50 207.0,50.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="214,50 207.0,53.2 207.0,46.8" style="fill:var(--accent,#3b6fd4)"/>
<rect x="214" y="28" width="116" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="272.0" y="46.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">每一位 ≥ 已存</text>
<text x="272.0" y="61.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">写者见过它：覆盖</text>
<rect x="10" y="92" width="176" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="98.0" y="110.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">新写 {A:1, B:2}</text>
<text x="98.0" y="125.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">A 更小，B 更大</text>
<polyline points="186,114 207.0,114.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="214,114 207.0,117.2 207.0,110.8" style="fill:var(--accent,#3b6fd4)"/>
<rect x="214" y="92" width="116" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="272.0" y="110.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">有升有降</text>
<text x="272.0" y="125.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">并发：留兄弟</text>
<text x="8" y="166" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">兄弟版本交给应用合并，</text>
<text x="8" y="182" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不要用时间戳悄悄丢掉一个。</text>
</svg>

**要点。**
- **发现得晚：** 单主里第二个写者当场被阻塞或报错，用户可重试；多主里没有这一步。
- **版本上下文：** 客户端读到值和版本，写时原样带回，副本据此比较。
- **兄弟版本：** 并发的两个版本都保留，交给应用合并：购物车取并集、计数取最大，或让用户挑，或用定义了合并的类型（CRDT）。
- **同步检测不可取：** 让一方等另一个 leader 确认，就失去多主「本地独立写」的意义，不如用单主。

**面试里这样说。** 「我用版本向量判断并发：不可比较的版本都留成兄弟，由应用合并，而不是用时间戳悄悄丢掉一个。合并函数必须在各副本上得出同一个结果。」

**易错。**
- **时间戳折叠兄弟：** 丢掉了系统明明知道是并发的写。
- **合并函数不确定：** 各副本合并结果不同，数据永远不收敛。
