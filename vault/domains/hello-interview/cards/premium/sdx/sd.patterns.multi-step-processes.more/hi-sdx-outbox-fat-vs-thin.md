---
id: hi-sdx-outbox-fat-vs-thin
node: sd.patterns.multi-step-processes.more
type: qa
step: 4
---
## Q
**发件箱事件带多少数据**｜补充 · 多步骤流程 · 追问

面试官：「发件箱里的事件，是带上订单的全部内容，还是只带一个订单 ID 让消费者回头查？瘦事件会引出什么竞态？」

## A
**结论。** 默认带全部内容（胖事件，事件携带状态）。发件箱的行在事务提交时快照下全部所需状态，消费者自给自足；瘦事件只带 ID 和类型，消费者回头查时，实体可能已经改变甚至消失。

**要点。**
- **胖事件：** 提交时快照，如 `OrderPlaced` 带商品、金额、地址；消费者无需回查，下游账本和审计拿到的是提交那一刻的值。代价是行更大，事件格式成了对外契约，要做版本化。
- **瘦事件的竞态：** 消费者读取时，订单可能已被修改、取消或删除，读到比事件更新的版本；同一个状态也可能在不同事件下被重复读到。
- **其他代价：** 瘦事件让消费者重新依赖生产者的接口，并增加读压力。
- **金融场景：** 默认胖事件，因为提交时的快照正是审计和下游账本需要的。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">瘦事件：只带 ID，消费者回头查</text>
<rect x="8" y="26" width="100" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="58.0" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t1 提交订单</text>
<text x="58.0" y="54.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">写事件 id=7</text>
<rect x="120" y="26" width="100" height="34" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t2 订单被改</text>
<text x="170.0" y="54.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">金额变了</text>
<rect x="232" y="26" width="100" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="282.0" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t3 消费者</text>
<text x="282.0" y="54.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">按 id 回查</text>
<polyline points="108,43 113.0,43.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="120,43 113.0,46.2 113.0,39.8" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="220,43 225.0,43.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="232,43 225.0,46.2 225.0,39.8" style="fill:var(--accent,#3b6fd4)"/>
<text x="8" y="92" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">回查读到的是 t2 之后的状态，</text>
<text x="8" y="112" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">比事件描述的 t1 更新；订单被删时直接读空。</text>
<line x1="8" y1="130" x2="332" y2="130" stroke-width="1" stroke="currentColor" opacity="0.4" stroke-dasharray="3 3"/>
<text x="8" y="152" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">胖事件：事务提交时拍下快照一起写入</text>
<rect x="8" y="162" width="324" height="34" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="183.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">OrderPlaced：商品、金额、地址（提交时的值）</text>
<text x="8" y="222" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">消费者无需回查，审计和下游账本拿到的</text>
<text x="8" y="240" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">就是提交那一刻的事实</text>
</svg>

**面试里这样说。** 「发件箱事件我用胖事件：事务提交时把下游需要的字段一起快照进去，消费者不用回查，不会读到比事件更新的状态。事件格式作为契约做版本化。」

**易错。**
- **为了省存储用瘦事件：** 回查读到的状态和事件对不上，对账时没法解释。
- **胖事件不做版本管理：** 加减字段会弄坏不知名的消费者。
