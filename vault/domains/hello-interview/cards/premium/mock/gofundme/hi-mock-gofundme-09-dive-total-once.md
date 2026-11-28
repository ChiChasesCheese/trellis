---
id: hi-mock-gofundme-09-dive-total-once
node: fix.gofundme-mock
type: qa
step: 9
---
## Q
**GoFundMe · 第 9 步 · 深入二：已募金额，只算成功，只算一次**｜模拟面试

面试官：「活动页上的已募金额，你打算怎么保证它只算成功的捐款？如果服务崩了或者消息重放了，会不会多算？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **定义：** 已募金额 = 所有 Success 捐款之和，Pending 和 Failed 不算；每次活动页 SUM 太贵，所以维护派生值。创建时不加，因为 Pending 之后可能失败。
- **触发：** 只有 Pending → Success 那一次条件更新产生 `DonationCompleted(donation_id, campaign_id, amount)`，和状态更新同事务写进 outbox（否则状态改了事件没发，或反过来），再经队列送给 worker。队列至少投递一次，所以要已应用表。
- **两张表：** `campaign_totals` 存持久总额，`campaign_total_applied` 以 donation_id 为主键记录哪些已加过。
- **worker 事务：** `INSERT INTO campaign_total_applied … ON CONFLICT DO NOTHING`；真的插入了才 `UPDATE campaign_totals SET amount = amount + 金额`；提交。重放时 INSERT 冲突，跳过加总，总额不变。
- **Redis：** 让活动页不读库；它可能落后或丢，所以不用 INCR（不记录哪笔加过，重放加两次），提交后只把 `campaign:{id}:total` SET 成持久值，重放时仍 SET 同值。
- **崩溃验证：** 崩在提交前，事务回滚、消息重投、正常加一次；崩在提交后、SET 前，持久值是对的、Redis 暂旧，重投时跳过加总再 SET 就对了。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 478">
<rect x="8" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="44" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">队列</text>
<rect x="92" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="128" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">worker</text>
<rect x="176" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="212" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<rect x="262" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="298" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis</text>
<text x="8" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只有 Pending → Success 才写 outbox 事件</text>
<rect x="116.92" y="84" width="190.16" height="20" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="212" y="98" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Success + outbox（同事务）</text>
<text x="48" y="120" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">DonationCompleted(D1)</text>
<polyline points="212,132 44,132" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="44,132 51.0,128.8 51.0,135.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="48" y="154" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">取消息</text>
<polyline points="128,166 44,166" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="44,166 51.0,162.8 51.0,169.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="188" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">INSERT applied(D1)</text>
<polyline points="128,200 212,200" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,200 205.0,203.2 205.0,196.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="222" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">插入成功</text>
<polyline points="212,234 128,234" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,234 135.0,230.8 135.0,237.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="256" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">totals += 金额</text>
<polyline points="128,268 212,268" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,268 205.0,271.2 205.0,264.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="121.96" y="282" width="180.08" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="212" y="296" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">COMMIT：applied + totals</text>
<text x="132" y="318" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">SET total = 持久值</text>
<polyline points="128,330 298,330" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="298,330 291.0,333.2 291.0,326.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="358" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">重放：队列把 D1 再投一次</text>
<text x="132" y="380" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">INSERT applied(D1)</text>
<polyline points="128,392 212,392" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,392 205.0,395.2 205.0,388.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="414" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">已存在：跳过加总</text>
<polyline points="212,426 128,426" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,426 135.0,422.8 135.0,429.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="448" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">SET total = 持久值（不变）</text>
<polyline points="128,460 298,460" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="298,460 291.0,463.2 291.0,456.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="44" y1="48" x2="44" y2="65" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="44" y1="80" x2="44" y2="474" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="48" x2="128" y2="65" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="80" x2="128" y2="82" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="106" x2="128" y2="109" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="124" x2="128" y2="280" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="304" x2="128" y2="347" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="362" x2="128" y2="474" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="48" x2="212" y2="65" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="80" x2="212" y2="82" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="106" x2="212" y2="177" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="192" x2="212" y2="245" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="260" x2="212" y2="280" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="304" x2="212" y2="307" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="322" x2="212" y2="347" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="362" x2="212" y2="369" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="384" x2="212" y2="403" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="418" x2="212" y2="437" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="452" x2="212" y2="474" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="48" x2="298" y2="82" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="106" x2="298" y2="280" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="304" x2="298" y2="437" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="452" x2="298" y2="474" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="8" y1="354" x2="85.28" y2="354" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="254.72" y1="354" x2="332" y2="354" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>
白板上新增：outbox、campaign_totals、campaign_total_applied 三张表，队列、计数 worker 和 Redis 的总额键。

**常见失分。**
- **只说工具名：** 说了 Redis、队列、事务，没说哪个记录「哪一笔已加过」。
- **创建时就加：** Pending 和之后失败的捐款也被算进去。
- **Redis 当账本：** 它是服务副本，真相在 campaign_totals 和 donations。
- **重放时再加一次：** 没有已应用表，重放就是多算。

**面试官可能接着问。**
- 两个 worker 乱序提交，Redis 会被旧值覆盖吗？ → 会；队列按 campaign_id 分区，一个活动由一个 worker 顺序处理，再用「新值比当前大才 SET」（无退款时总额只增）；支持退款改带版本号，版本更大才写。
- Redis 整个丢了？ → 从 campaign_totals 回填；campaign_totals 每天用 donations 的 Success 求和对账，有偏差就重算。
- 为什么不在 Success 的事务里直接加总？ → 每笔在线请求都抢活动行，热点进了写路径；放 worker 里可批量。
