---
id: hi-fix-ack-point-02-write-and-publish
node: fix.ack-point
type: qa
step: 2
---
## Q
**先说清 200 在哪一步返回 · 库写和发布是一个整体**｜补强

面试官：「你既要把请求记进库，又要发到日志。这两件事怎么做到要么都发生、要么都不发生？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先说问题：** 「库和日志是两个系统，没有一个事务能包住两者，这叫双写（dual write）。先写库再发日志，崩在中间：库里有 queued 行，日志里没有消息，永远没人发，状态永远是 queued。反过来先发日志再写库：日志里有消息，库里没有行，查状态查不到。」
- **修法一，事务发件箱（transactional outbox）：** 「通知行和一条 outbox 行在同一个库事务里写，提交之后才返回 202。relay 读 outbox，发到日志，发完才删。至少一次：relay 可能发两次，worker 靠唯一约束去重。」
- **修法二，日志是真相：** 「请求路径只往日志追加一次，提交成功就返回 202。库不在请求路径上，由 worker 从日志读出来写，库是派生数据，丢了可以从日志重建。」
- **选哪个：** 「通知的接受路径选二。尖峰 83,000 条/秒，outbox 每条要写两行（通知行和 outbox 行），就是 166,000 行写/秒，把我前面放日志要躲开的压力又放回了库上；日志只追加一次。」
- **什么时候用一：** 「活动扇出：任务的游标和这一块的通知行本来就在库里，通知行就是 outbox。产品团队自己的服务要在改订单的同时发事件，也用一。」
- **两种都要消重：** 「都是至少一次，重复由唯一约束吸收。」
**白板。**
```
BEGIN;
INSERT INTO notification
  (notification_id, status)
VALUES ($id, 'queued')
ON CONFLICT DO NOTHING;
-- 0 行：重复请求，回滚，返回首次 202
INSERT INTO outbox (notification_id, body)
VALUES ($id, $body);
COMMIT;  -- 提交之后才返回 202
-- relay：每 100 毫秒读 outbox 500 行，
-- 发到日志，成功后删这 500 行
```

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 186">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">双写：库和日志是两个系统</text>
<rect x="8" y="34" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="44" y="57" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">服务</text>
<rect x="134" y="34" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="57" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">库</text>
<rect x="260" y="34" width="72" height="38" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="296" y="57" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">日志</text>
<text x="48" y="98" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">INSERT queued，提交</text>
<polyline points="44,110 170,110" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,110 163,113.2 163,106.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="132" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">崩溃</text>
<line x1="8" y1="128" x2="152" y2="128" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="188" y1="128" x2="332" y2="128" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="44" y1="74" x2="44" y2="156" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="74" x2="170" y2="87" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="101" x2="170" y2="121" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="135" x2="170" y2="156" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="296" y1="74" x2="296" y2="156" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<text x="8" y="164" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">库里有 queued 行，日志里没有</text>
<text x="8" y="180" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">永远没人发，状态永远 queued</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 194">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">两种修法，各自适合哪里</text>
<rect x="8" y="26" width="324" height="74" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">事务发件箱（outbox）</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">通知行 + outbox 行，一个事务</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">relay 读 outbox 发日志，发完再删</text>
<text x="18" y="89.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">适合：活动扇出、产品方自己的服务</text>
<rect x="8" y="108" width="324" height="74" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">日志是真相，库由日志喂</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">请求路径只追加日志一次</text>
<text x="18" y="156.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">worker 写库，库是派生的、可重建</text>
<text x="18" y="171.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">适合：通知的接受路径</text>
</svg>
白板上：左边是双写崩在中间的样子，右边是两种修法各管哪一类。
**为什么这样说。** （约 90 秒。）面试官要确认你知道这条缝，并且能说出两种修法的差别和适用条件。强的回答先说崩在哪里造成什么，再给两个修法，并用一个数字（166,000 行写/秒）说明为什么选二；弱的回答只说「用事务」，而库事务根本包不住日志。
**面试官可能接着问。**
- Kafka 事务能把库也包进去吗？ → 不能：Kafka 事务的原子范围在 Kafka 内部（读、写、提交位移）；库加日志只能用发件箱或让日志当真相。
- relay 用轮询还是 CDC？ → 轮询最简单，每 100 毫秒一次，延迟约 100 毫秒；量大时读库的变更日志（CDC）延迟更低、不压库。
- relay 发了但没删就崩了？ → 重启后再发一次；这是至少一次，worker 去重。
**常见失分。**
- **「用一个事务」：** 日志不在库里。
- **先写库，再发日志，中间不处理：** 一条缝，就是永远 queued 的行。
- **把 outbox 放到尖峰路径上：** 写放大一倍。
