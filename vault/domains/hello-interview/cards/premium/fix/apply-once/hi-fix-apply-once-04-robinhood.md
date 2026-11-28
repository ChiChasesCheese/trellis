---
id: hi-fix-apply-once-04-robinhood
node: fix.apply-once
type: qa
step: 4
---
## Q
**Robinhood 成交回报 · 只应用一次**｜补强

面试官：「交易所通过成交推送告诉你订单成交了，断线重连之后会把最近的成交再推一遍。你怎么更新订单的已成交数量和用户持仓，保证每笔成交只算一次？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先说职责：** 「成交处理器的职责，是把交易所的成交变成我们订单和持仓上的变化。它面对的新问题是重复推送：重连后回放、处理器重启后重新消费。」
- **每笔成交有自己的 id：** 「交易所的成交回报带一个执行编号（exec id）。我建一张 `fills` 表，`exec_id` 主键。这个主键就是已应用记录。」
- **一个事务：** 「`INSERT INTO fills … ON CONFLICT (exec_id) DO NOTHING RETURNING order_id, qty`；返回了行，才 `UPDATE orders SET filled_qty = filled_qty + :qty`，状态按累计数量算：够了是 FILLED，不够是 PARTIAL；再 `UPDATE positions SET shares = shares + :qty`；提交。」
- **重放：** 「同一个 exec_id 再来，INSERT 返回 0 行，订单和持仓都不动。」
- **乱序和部分成交：** 「每笔成交的加法是可交换的，所以去重之后到达顺序不影响累计数量；状态要靠累计数量推出来，不靠最后一条消息。」
- **怎么找到订单：** 「用交易所给的订单号，经过键值库映射回我们的订单，再按 user_id 路由到分片；整个事务发生在这一个分片里。」
- **对账：** 「`filled_qty` 应当等于该订单下 `fills.qty` 之和；每天和交易所的成交报告比对。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 384">
<rect x="18" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="54" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">交易所</text>
<rect x="134" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">成交处理</text>
<rect x="250" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="286" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<text x="58" y="72" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">成交 E1 · 60 股</text>
<polyline points="54,84 170,84" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="170,84 163.0,87.2 163.0,80.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="174" y="106" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">INSERT fills(E1) → 1 行</text>
<polyline points="170,118 286,118" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="286,118 279.0,121.2 279.0,114.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="184.72" y="132" width="151.28" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="260.36" y="146" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">filled 60 · 持仓 +60</text>
<text x="170" y="174" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">断线重连，重推 E1</text>
<text x="58" y="196" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">成交 E1 · 60 股</text>
<polyline points="54,208 170,208" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="170,208 163.0,211.2 163.0,204.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="174" y="230" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">INSERT fills(E1) → 0 行</text>
<polyline points="170,242 286,242" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="286,242 279.0,245.2 279.0,238.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="236.16" y="256" width="99.68" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="286" y="270" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不变：仍是 60</text>
<text x="58" y="292" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">成交 E2 · 40 股</text>
<polyline points="54,304 170,304" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="170,304 163.0,307.2 163.0,300.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="174" y="326" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">INSERT fills(E2) → 1 行</text>
<polyline points="170,338 286,338" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="286,338 279.0,341.2 279.0,334.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="189.76" y="352" width="146.24" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="262.88" y="366" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">filled 100 · FILLED</text>
<line x1="54" y1="48" x2="54" y2="380" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="48" x2="170" y2="163" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="178" x2="170" y2="380" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="286" y1="48" x2="286" y2="95" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="286" y1="110" x2="286" y2="130" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="286" y1="154" x2="286" y2="219" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="286" y1="234" x2="286" y2="254" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="286" y1="278" x2="286" y2="315" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="286" y1="330" x2="286" y2="350" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="286" y1="374" x2="286" y2="380" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="8" y1="170" x2="108.2" y2="170" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="231.8" y1="170" x2="332" y2="170" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>
白板上：重连后重推 E1，插入返回 0 行，订单和持仓都不变。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 215">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">一条语句，三张表一起动</text>
<rect x="8" y="26" width="324" height="151" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">WITH f AS (INSERT INTO fills</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">  VALUES (:exec_id, :order, :qty, :px)</text>
<text x="18" y="75.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">  ON CONFLICT (exec_id) DO NOTHING</text>
<text x="18" y="90.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">  RETURNING order_id, qty),</text>
<text x="18" y="105.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">o AS (UPDATE orders SET</text>
<text x="18" y="120.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">  filled_qty = filled_qty + f.qty … FROM f</text>
<text x="18" y="135.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">  WHERE id = f.order_id)</text>
<text x="18" y="150.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">UPDATE positions SET shares = shares +</text>
<text x="18" y="165.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">  (SELECT coalesce(sum(qty),0) FROM f) …;</text>
<text x="8" y="199" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">f 没有返回行：o 和 positions 都不动</text>
</svg>
白板上：一条语句里，插入没返回行，其余两个更新都不动。

**为什么这样说。** 面试官在检查：重复推送到达时，你的数据里有没有一个地方记着哪笔成交已经算过。弱的回答只说「处理器要幂等」；强的回答说出成交的唯一编号、唯一约束，以及只在插入成功时才去加数量。
**面试官可能接着问。**
- 交易所不给 exec id 怎么办？ → 用 (外部订单号, 成交序号) 或成交的完整内容（时间、价格、数量）派生一个确定的 id；我会先确认交易所接口提供哪些字段。
- 成交和撤单同时到呢？ → 订单状态走状态机，终态不可回退；成交仍然记录并累计，撤单只影响未成交部分。
- 持仓要不要实时？ → 持仓是派生的，实时更新在同一个事务里；展示可以缓存，缓存 SET 成已提交的值。
- 处理器崩在提交之前？ → 事务回滚，消息没确认，重投之后重新做。
**常见失分。**
- **先 `filled_qty += qty` 再记录：** 崩在中间就多算或者少算。
- **用最后一条消息决定状态：** 乱序到达时状态被旧消息覆盖。
- **只防订单、不防持仓：** 订单对了，持仓被加了两次。
- **成交内容当作键但字段不全：** 两笔相同价格数量的合法成交被当成重复。
