---
id: hi-fix-apply-once-01-mechanism
node: fix.apply-once
type: qa
step: 1
---
## Q
**只应用一次 (Apply Once)｜补强 · 机制**

总额、余额、库存、计数这类派生值，是由事件或后台任务一步步更新出来的。事件会被重放，任务会被重跑。为什么「Redis 原子 INCR」或者「放进一个事务」都保证不了每件事只加一次？怎样才算做对了？

## A
**要防的失败。** worker 处理一个事件有两步：把金额加进总额，再向队列确认（ack）。崩在两步之间，队列就会把同一个事件再投一次，worker 又加一遍。
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 288">
<rect x="18" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="54" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">队列</text>
<rect x="134" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Worker</text>
<rect x="250" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="286" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis</text>
<text x="58" y="72" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">完成事件 d17 · 25</text>
<polyline points="54,84 170,84" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="170,84 163.0,87.2 163.0,80.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="174" y="106" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">INCRBY total 25</text>
<polyline points="170,118 286,118" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="286,118 279.0,121.2 279.0,114.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="110.2" y="132" width="119.6" height="20" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="146" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">崩溃，来不及 ack</text>
<text x="170" y="174" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">队列重投</text>
<text x="58" y="196" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">完成事件 d17 · 25</text>
<polyline points="54,208 170,208" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="170,208 163.0,211.2 163.0,204.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="174" y="230" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">INCRBY total 25</text>
<polyline points="170,242 286,242" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="286,242 279.0,245.2 279.0,238.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="203.44" y="256" width="132.56" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="269.72" y="270" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">总额 +50：多算一次</text>
<line x1="54" y1="48" x2="54" y2="284" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="48" x2="170" y2="61" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="76" x2="170" y2="130" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="154" x2="170" y2="163" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="178" x2="170" y2="185" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="200" x2="170" y2="284" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="286" y1="48" x2="286" y2="254" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="286" y1="278" x2="286" y2="284" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="8" y1="170" x2="138.08" y2="170" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="201.92" y1="170" x2="332" y2="170" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>
白板上：加法做了、确认没来得及，重投之后同一笔被加了两次。

**为什么原子和事务都救不了。**
- **原子只管一次操作：** `INCR` 是原子的，但它不知道这个事件是不是上一次已经加过了。
- **事务只管一半不出现：** 事务保证「加和写」不会只成功一半，重投会开一个全新的事务，照样提交。
- **复制和队列也一样：** 它们让数据不丢，不让数据不重。至少一次投递，天然带着重复。

**机制。** 把「这个事件我已经加过」也写成数据，放进和加法同一个事务里。
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 390">
<rect x="8" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="44" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">队列</text>
<rect x="92" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="128" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Worker</text>
<rect x="176" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="212" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<rect x="262" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="298" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis</text>
<text x="48" y="72" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">d17 · 25</text>
<polyline points="44,84 128,84" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="128,84 121.0,87.2 121.0,80.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="132" y="106" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">INSERT applied(d17)</text>
<polyline points="128,118 212,118" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,118 205.0,121.2 205.0,114.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="175.12" y="132" width="73.76" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="212" y="146" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">插入 1 行</text>
<text x="132" y="168" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">total += 25；COMMIT</text>
<polyline points="128,180 212,180" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,180 205.0,183.2 205.0,176.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="202" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">SET total &lt;已提交值&gt;</text>
<polyline points="128,214 298,214" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="298,214 291.0,217.2 291.0,210.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="242" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">队列重投</text>
<text x="48" y="264" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">d17 · 25</text>
<polyline points="44,276 128,276" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="128,276 121.0,279.2 121.0,272.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="132" y="298" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">INSERT applied(d17)</text>
<polyline points="128,310 212,310" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,310 205.0,313.2 205.0,306.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="155.68" y="324" width="112.64" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="212" y="338" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">冲突 0 行：不加</text>
<text x="132" y="360" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">SET total（同一个值）</text>
<polyline points="128,372 298,372" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="298,372 291.0,375.2 291.0,368.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="44" y1="48" x2="44" y2="386" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="48" x2="128" y2="386" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="48" x2="212" y2="95" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="110" x2="212" y2="130" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="154" x2="212" y2="157" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="172" x2="212" y2="191" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="206" x2="212" y2="287" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="302" x2="212" y2="322" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="346" x2="212" y2="349" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="364" x2="212" y2="386" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="48" x2="298" y2="386" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="8" y1="238" x2="138.08" y2="238" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="201.92" y1="238" x2="332" y2="238" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>
白板上：worker 先往唯一约束的已应用表里插入事件 id；插进去了才加，冲突了就跳过。Redis 只被「设成」已提交的值。
- **已处理是一行数据：** 已应用表 `campaign_total_applied(donation_id 主键, campaign_id, amount)`。
- **同一个事务：** 插入已应用表和给总额做加法一起提交，要么都发生，要么都没发生。
- **插入的结果就是判决：** 插进 1 行就加，冲突就是重放，什么也不做。
- **缓存只做 SET：** 提交之后把 Redis 设成数据库里的值。重复一百次也是同一个值；崩在这一步，下一次也会补上。
- **只由终态触发：** 只有转到 SUCCESS 的那次事务才发事件。创建时不发，所以 PENDING 和后来被拒绝的不会被算进去。

**两种做法。** 要让重放无害，有两条路：
- **记录式：** 增量更新（`+=`），靠已应用的记录挡重复。适合总额、余额、库存。
- **绝对式：** 每次写的就是完整的值（窗口累计、`SELECT SUM` 的结果），重放写同一个数。适合聚合表、缓存。

**在面试里说这一句。** 「消费者可能重放，所以我不赌事件只来一次：worker 在一个事务里先把 `donation_id` 插进有唯一约束的 `campaign_total_applied`，插入成功才给总额加上这笔金额；重放时插入冲突，直接跳过。Redis 只 `SET` 成已提交的值。」

**怎么认出这类题。**
- **有派生值：** 总额、余额、库存、点击数、已成交数量，是由别的数据算出来的。
- **来源至少投递一次：** 队列、变更日志（CDC）、webhook、定时任务重跑、消费者重启。
- **更新是增量：** `+=`、`INCR`、追加、发邮件。你说出「加一」的时候，面试官会问「加了两次怎么办」。

**常见失分。**
- **只说「队列保证」：** 队列保证至少一次，不是恰好一次。
- **用 Redis INCR 当真相：** 重放多算、崩溃少算，没有任何记录能纠正。
- **创建时就计入：** 还没付成功的、后来被拒绝的，也进了总额。
