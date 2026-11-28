---
id: hi-sdx-cap-quorum-not-linearizable
node: sd.core-concepts.cap-theorem.more
type: qa
step: 3
---
## Q
**R+W>N 为什么仍不线性一致**｜补充 · CAP 定理 · 追问

面试官：「Dynamo 风格存储，副本数 N=3，写确认数 W=2，读确认数 R=2，严格多数派、没有宽松法定人数。为什么读仍然不是线性一致？举一个具体的交错。」

## A
**结论。** R+W>N 只保证「读集合与写集合相交」，从而能读到已确认的写；它不保证读与读之间的先后。写是逐个副本落下去的，一个读者可能先读到新值，随后另一个读者读到旧值，这违反线性一致。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">N=3，W=2，R=2；写 x=1 正在进行，尚未 2 个确认</text>
<rect x="10" y="28" width="96" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="58.0" y="46.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">副本 r1</text>
<text x="58.0" y="61.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">x = 1（新）</text>
<rect x="122" y="28" width="96" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="46.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">副本 r2</text>
<text x="170.0" y="61.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">x = 0（旧）</text>
<rect x="234" y="28" width="96" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="282.0" y="46.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">副本 r3</text>
<text x="282.0" y="61.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">x = 0（旧）</text>
<polyline points="58,76 58,90 160,90 160,76" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<text x="10" y="108" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">① 读者 A 读 {r1, r2}</text>
<text x="10" y="124" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">取版本较新的 → 返回 1</text>
<polyline points="180,76 180,162 282,162 282,76" fill="none" stroke-width="1.3" stroke="currentColor"/>
<text x="231" y="180" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">② 之后读者 B 读 {r2, r3}</text>
<text x="231" y="196" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">两个都是旧的 → 返回 0</text>
<text x="8" y="222" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">A 已经读到 1，B 随后却读到 0：新值之后又见旧值，</text>
<text x="8" y="238" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每次读都满足 R=2，整体仍不是线性一致。</text>
</svg>

**要点。**
- **写不是瞬间完成：** 协调者把写发给三个副本，要等 2 个确认才算完成；之前副本陆续生效，读可以撞上半完成的状态。
- **每次读都合法：** B 的读集合 {r2, r3} 在写还没确认时也满足 R=2。
- **线性一致的要求：** 一旦有读返回了新值，之后开始的所有读都不能返回旧值。
- **修法很贵：** 读者返回前先同步做读修复（read repair），把新值写到一个写集合；写者也要先读到最新版本。每次多一轮往返。
- **同一客户端读两次也会倒退：** 这叫单调读（monotonic reads）被破坏。把会话固定到某个副本的办法在这里行不通，因为每次请求的协调者都可能挑不同的副本子集；改让客户端带上已见过的最高版本，读到更旧的结果就重试。

**为什么。** 法定人数给的是「读得到已确认的写」；要线性一致读，用共识（Raft 领导者读）。

**面试里这样说。** 「N=3、W=2、R=2 时，写落到 r1 还没到 r2、r3，读者 A 读 r1、r2 拿到新值，随后读者 B 读 r2、r3 拿到旧值，新值之后又见旧值，所以不是线性一致。需要线性一致我会走 Raft 领导者读。」

**易错。**
- **把法定人数说成强一致：** 它只在没有并发写、没有宽松法定人数、没有时钟问题时才像强一致。
- **靠调参数硬修：** R=N 能避开，但任一副本宕机读就失败。
