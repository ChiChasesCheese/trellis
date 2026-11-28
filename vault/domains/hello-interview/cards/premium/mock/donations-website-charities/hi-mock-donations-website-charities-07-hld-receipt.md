---
id: hi-mock-donations-website-charities-07-hld-receipt
node: qb.sd.donations-website-charities.mock
type: qa
step: 7
---
## Q
**限时捐款网站 · 第 7 步 · 高层设计（二）：机构列表、状态与收据**｜模拟面试

面试官：「提交这条流程通了。成功之后的收据，还有机构列表、状态查询，怎么加进来？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **新增三块：** 「发件箱表（outbox）和消息队列，加上回执服务和邮件服务。」
- **机构列表：** 「`GET /charities` 读一张几行的小表，可以缓存，不碰 PSP。」
- **状态查询：** 「浏览器每 2 秒轮询 `GET /donations/:id`，读的就是同一行。PROCESSING 和 UNKNOWN 显示『处理中』，终态就停止轮询。」
- **收据，先说坑：** 「如果 API 改完状态再直接发队列，两步之间崩溃，状态成功了，邮件永远不发；反过来先发邮件再改状态，邮件发了状态却没改。」
- **发件箱：** 「所以 SUCCEEDED 的状态更新和一条 outbox 行写在同一个数据库事务里，要么都成功，要么都不成功。」
- **投递器：** 「一个小进程（relay）扫 outbox 里没投递的行，推到消息队列，成功后标记已投递。这是至少一次投递，可能重发。」
- **回执服务：** 「消费队列，按 donationId 去重，再给邮箱发邮件。失败就退避重试，多次失败进死信队列。邮件失败不影响支付状态，用户在状态页照样能看到成功。」
- **总额：** 「您说不需要展示总额，所以我不画计数器。如果要，我不会在一行上累加，那样 5 家机构就是 5 个热点行；我会用分片计数器，或者消费成功事件批量累加到 Redis，展示允许延迟几秒，账目真相仍是 donations 表。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 500">
<rect x="12" y="8" width="140" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="82" y="26.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">浏览器 · 捐款页</text>
<text x="82" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">donationId (UUID)</text>
<rect x="188" y="8" width="140" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="258" y="26.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">PSP 前端组件</text>
<text x="258" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">收卡号 · 换令牌</text>
<polyline points="152,22 188,22" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="188,22 181.0,25.2 181.0,18.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="188,40 152,40" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="152,40 159.0,36.8 159.0,43.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="17" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">卡号</text>
<text x="170" y="55" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">令牌</text>
<rect x="12" y="108" width="316" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="126.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">捐款 API</text>
<text x="170" y="141.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">无状态 · 多实例</text>
<polyline points="24,52 24,108" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="24,108 20.8,101.0 27.2,101.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="24,52 27.2,59.0 20.8,59.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="34" y="70" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">POST /donations</text>
<text x="34" y="84" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">GET /charities</text>
<text x="34" y="98" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">GET /donations/:id</text>
<path d="M12,198 a70,6 0 0 1 140,0 v136 a70,6 0 0 1 -140,0 z" stroke-width="1.2" fill="none" stroke="currentColor"/>
<path d="M12,198 a70,6 0 0 0 140,0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<text x="82" y="216" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库 Postgres</text>
<rect x="20" y="232" width="124" height="22" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="82" y="247" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">donations 表</text>
<rect x="20" y="258" width="124" height="22" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="82" y="273" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">outbox 表</text>
<rect x="20" y="284" width="124" height="22" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="82" y="299" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">charities 表</text>
<polyline points="60,152 60,192" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="60,192 56.8,185.0 63.2,185.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="60,152 63.2,159.0 56.8,159.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="66" y="176" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">INSERT / UPDATE</text>
<rect x="188" y="240" width="68" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="222" y="266" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">主 PSP</text>
<polyline points="220,152 220,240" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="220,240 216.8,233.0 223.2,233.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="226" y="200" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">扣款 + 幂等键</text>
<rect x="12" y="380" width="140" height="36" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="20" y="403" width="21.8" height="7" fill="none" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<rect x="44.8" y="403" width="21.8" height="7" fill="none" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<rect x="69.6" y="403" width="21.8" height="7" fill="none" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<rect x="94.4" y="403" width="21.8" height="7" fill="none" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<rect x="119.2" y="403" width="21.8" height="7" fill="none" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<text x="82" y="395" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">消息队列</text>
<polyline points="82,340 82,380" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="82,380 78.8,373.0 85.2,373.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="88" y="366" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">投递器</text>
<rect x="12" y="440" width="140" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="82" y="456.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">回执服务</text>
<text x="82" y="471.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">去重 · 重试</text>
<polyline points="82,416 82,440" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="82,440 78.8,433.0 85.2,433.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="188" y="440" width="140" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="258" y="456.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">邮件服务</text>
<text x="258" y="471.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">发收据</text>
<polyline points="152,460 188,460" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="188,460 181.0,463.2 181.0,456.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
</svg>
白板上新增：outbox 表、charities 表、投递器到消息队列、回执服务、邮件服务，以及浏览器的两条新读请求。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 336">
<rect x="8" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="44" y="23.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">投递器</text>
<text x="44" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">relay</text>
<rect x="92" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="128" y="23.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<text x="128" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">outbox 表</text>
<rect x="176" y="8" width="72" height="38" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="212" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">队列</text>
<rect x="262" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="298" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">回执服务</text>
<rect x="28.96" y="64" width="198.08" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="128" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">事务：SUCCEEDED + outbox 行</text>
<text x="48" y="100" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">扫未投递的行</text>
<polyline points="44,112 128,112" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,112 121.0,115.2 121.0,108.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="48" y="134" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">donationId</text>
<polyline points="128,146 44,146" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="44,146 51.0,142.8 51.0,149.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="48" y="168" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">发布 receipt 事件</text>
<polyline points="44,180 212,180" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,180 205.0,183.2 205.0,176.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="48" y="202" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">标记已投递</text>
<polyline points="44,214 128,214" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,214 121.0,217.2 121.0,210.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="216" y="236" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">消费事件</text>
<polyline points="298,248 212,248" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,248 219.0,244.8 219.0,251.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<polyline points="298,266 324,266 324,280 298,280" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="298,280 305.0,276.8 305.0,283.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="292" y="277" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">去重 + 发邮件</text>
<text x="8" y="304" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">崩在「发布」与「标记」之间：事件重发一次，</text>
<text x="8" y="324" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">回执服务按 donationId 去重，邮件不会发两封</text>
<line x1="44" y1="48" x2="44" y2="62" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="44" y1="86" x2="44" y2="293" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="44" y1="308" x2="44" y2="313" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="44" y1="328" x2="44" y2="332" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="48" x2="128" y2="62" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="86" x2="128" y2="89" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="104" x2="128" y2="157" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="172" x2="128" y2="293" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="308" x2="128" y2="313" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="328" x2="128" y2="332" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="48" x2="212" y2="62" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="86" x2="212" y2="266" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="281" x2="212" y2="293" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="308" x2="212" y2="313" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="328" x2="212" y2="332" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="48" x2="298" y2="332" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>
白板上新增：发件箱从事务到收据的时序，以及崩溃在中间时的补救方式。
**为什么这样说。** （约 5 分钟，累计第 23 分钟。）面试官看你对「状态变更加通知」这类双写问题有没有标准答案：发件箱。强的回答先说不用发件箱会出什么错，再讲投递器和去重。弱的回答是在 API 里同步发邮件，或者「改完状态顺手发一条消息」。这一步高级候选人要加快，把时间留给深入问题。
**面试官可能接着问。**
- 为什么不在 API 里同步发邮件？ → 邮件服务慢或失败，会拖慢甚至拖垮支付响应；而且邮件失败不该让已成功的支付回滚。
- 发件箱用轮询还是 CDC？ → 先用轮询，实现简单，2,000 笔/秒完全够；要更低延迟再换变更数据捕获（CDC）。
- 邮件会不会发两封？ → 投递是至少一次，所以回执服务按 donationId 去重：先写一条已发送记录再发，崩溃重来时发现已有就跳过。邮件服务若支持幂等键也一起用。
- 如果面试官改主意，要展示各机构总额？ → 就是前面说的两种做法，数据库行计数要分片，Redis 事件喂入更省事；展示允许几秒延迟，不影响对账。
**常见失分。**
- **双写：** 先改状态再发消息，中间崩溃就丢收据，面试官一定会追。
- **邮件失败回滚支付：** 把通知和支付绑成一件事，方向反了。
- **不去重：** 至少一次投递会重复，不说去重，是高级候选人常被抓到的地方。
- **时间太长：** 高层设计超过 15 分钟，深入问题就讲不完。
