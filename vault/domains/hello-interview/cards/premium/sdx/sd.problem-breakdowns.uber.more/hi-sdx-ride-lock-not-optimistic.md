---
id: hi-sdx-ride-lock-not-optimistic
node: sd.problem-breakdowns.uber.more
type: qa
step: 1
---
## Q
**派单为何先加锁而非乐观并发**｜补充 · 网约车（Uber） · 追问

面试官：「两个乘客在同一块稀疏区域，同时把同一个司机排在候选第一位。为什么给司机发邀请之前要先加一个短 TTL 的排他锁，而不是用乐观并发：两边都匹配，发现冲突再让输的那个重试？」

## A
**结论。** 乐观并发假设冲突少、重试便宜。但这里的冲突出现在副作用之后：邀请一旦推到司机手机上就收不回，司机会同时看到两个互相矛盾的订单，用户直接感知为故障。所以在推送之前，先以 driver_id 加带 TTL 的锁，加锁失败就立刻换下一个候选。

**要点。**
- **代价不对称：** 内部重试对用户不可见；推送给司机的邀请不可撤回。
- **锁的形态：** 键为 `driver:{id}`，`SET NX` 加 TTL，TTL 略大于司机的响应窗口（如 10 秒）。
- **失败就跳过：** 加锁失败说明另一个匹配流程占着这个司机，直接取下一个候选，不阻塞等待。
- **TTL 兜底：** 司机不响应或匹配服务崩溃，锁自动过期，不依赖一次可能永远不来的显式释放。
- **最终正确性：** 锁只保证大多数时候互斥。接单时仍要条件更新（带订单号，`status='requested'` 才可改），挡住锁刚过期后的迟到点击。

**为什么。** 并发控制的选择取决于冲突发生时能否无声地回滚。能，用乐观并发；不能（已经对外发出了消息），就要在发出之前先占住资源。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 286">
<rect x="8" y="8" width="72" height="38" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="44" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">匹配 A</text>
<rect x="92" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="128" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">匹配 B</text>
<rect x="176" y="8" width="72" height="38" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="212" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis</text>
<rect x="262" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="298" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">司机端</text>
<text x="48" y="72" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">SET NX 10 秒</text>
<polyline points="44,84 212,84" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,84 205.0,87.2 205.0,80.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="48" y="106" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">成功</text>
<polyline points="212,118 44,118" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="44,118 51.0,114.8 51.0,121.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="140" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">SET NX 10 秒</text>
<polyline points="128,152 212,152" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="212,152 205.0,155.2 205.0,148.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="132" y="174" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">失败</text>
<polyline points="212,186 128,186" fill="none" stroke-width="1.3" stroke-dasharray="4 3" stroke="currentColor"/>
<polygon points="128,186 135.0,182.8 135.0,189.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="82.12" y="200" width="91.76" height="20" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="128" y="214" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">换下一个候选</text>
<text x="48" y="236" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">推送邀请</text>
<polyline points="44,248 298,248" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="298,248 291.0,251.2 291.0,244.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="8" y="274" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">冲突在发出邀请之前就已解决</text>
<line x1="44" y1="48" x2="44" y2="263" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="44" y1="278" x2="44" y2="282" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="48" x2="128" y2="61" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="76" x2="128" y2="198" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="222" x2="128" y2="263" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="278" x2="128" y2="282" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="48" x2="212" y2="129" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="144" x2="212" y2="282" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="48" x2="298" y2="282" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>

**面试里这样说。** 「发邀请之前我先给司机加 `driver:{id}` 的锁，`SET NX`，TTL 10 秒。加锁失败就换下一个候选，不等待。我不用乐观并发，因为冲突发现时邀请已经推到司机手机上，收不回来。接单时再用条件更新兜底。」

**易错。**
- **先发邀请再检测冲突：** 司机会收到两个订单，没法撤销。
- **加锁失败就等待：** 被占的司机马上就不空闲了，等待只会增加延迟。
- **TTL 短于司机响应时间：** 司机还在看订单，锁就过期了，又被别的订单拿走。
