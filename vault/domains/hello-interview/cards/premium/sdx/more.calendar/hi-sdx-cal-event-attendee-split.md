---
id: hi-sdx-cal-event-attendee-split
node: more.calendar
type: qa
step: 2
---
## Q
**事件和参会人分成两张表**｜补充 · 日历与排期（Google Calendar） · 必会

面试官：「日历里的一个事件有时间、地点、重复规则，还有几十个参会人，各自有回复状态。参会人放在事件记录里的数组中，还是单独一张表？为什么？」

## A
**结论。** 拆成两张表。事件表（Event）只放组织者控制的字段：时间、地点、重复规则；参会表（Attendee）一行一个人，记录事件、用户和回复状态。两类写入落在不同的行上，互不争用。

**要点。**
- **写入的人不同：** 组织者改时间地点，低频、改整条；参会人回复，高频、各改各的一小块。
- **嵌入数组的问题：** 每次回复都要读改写整条事件，并和组织者的编辑抢同一行的锁。
- **拆表之后：** 回复只更新自己那一行；组织者改时间只写事件表一行，参会人通过事件编号读到新时间。
- **幂等的邀请：** (event_id, user_id) 唯一，邀请重试不会产生两行。
- **按用户列出日程：** 在参会表上以 user_id 开头建索引，就能列出某人参加的所有事件。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 226">
<rect x="10" y="8" width="150" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="85.0" y="26.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">事件表 Event</text>
<text x="85.0" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">时间 · 地点 · 规则</text>
<rect x="180" y="8" width="150" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="255.0" y="26.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">参会表 Attendee</text>
<text x="255.0" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">事件 · 用户 · 回复</text>
<polyline points="95,52 95.0,79.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="95,86 91.8,79.0 98.2,79.0" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="255,52 255.0,79.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="255,86 251.8,79.0 258.2,79.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="103" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">组织者改</text>
<text x="263" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">RSVP</text>
<rect x="10" y="90" width="150" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="85.0" y="108.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只写 1 行</text>
<text x="85.0" y="123.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">与回复互不争用</text>
<rect x="180" y="90" width="150" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="255.0" y="108.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只写自己 1 行</text>
<text x="255.0" y="123.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">与组织者互不争用</text>
<text x="8" y="160" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">嵌入数组：每次回复都要读改写整条事件，</text>
<text x="8" y="176" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">并与组织者的编辑抢同一行锁。</text>
<text x="8" y="200" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">(event_id, user_id) 唯一，邀请重试幂等。</text>
</svg>

**为什么。** 数据应该按「谁来写、写多频繁」来切分。同一条记录里混着两种写入节奏，锁和冲突就跟着混在一起；拆开以后各自独立扩展，也各自可以换存储。

**面试里这样说。** 「事件表只存组织者控制的字段，参会表一人一行，(event_id, user_id) 唯一。回复只改自己那一行，不和组织者的编辑争锁；列出我的日程就用参会表的 user_id 索引。」

**易错。**
- **把参会人嵌进事件：** 回复和编辑互相阻塞，热门的大会议尤其明显。
- **把回复状态放进事件表：** 一个人回复要改所有人共享的那一行。
- **为每位参会人复制整个事件：** 组织者改一次时间要改 N 份，容易不一致。
