---
id: hi-mock-airbnb-wallet-10-dive-bounded-refresh-sweep
node: fix.airbnb-wallet-mock
type: qa
step: 10
---
## Q
**Airbnb Wallet · 第 10 步 · 深入二（下）：有界刷新与每日扫描**｜模拟面试

面试官：「用户一直刷新一笔 pending 的转账。你要不要实时去问平台？如果回调一直没来呢？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **不实时问平台：** 用户的读只读本地行，刷新交给后台，三道上限：新鲜度窗口 30 秒（假设）；每笔每窗口最多一个刷新任务；对平台全局限速 20 次/秒。
- **读路径：** pending 就返回 pending 和 last_vendor_check_at；距今不足 30 秒什么都不做，为空或超过 30 秒才抢名额：条件 UPDATE 把 last_vendor_check_at 写成现在，1 行就把 transaction_id 入刷新队列，0 行说明别人刚抢过。无论哪种都立刻返回 pending。
- **worker：** 取到任务先重读（队列至少一次投递会有重复），仍 pending 才调 getTransfer，再 `settle()`；4 个 worker × 5 次/秒 = 20 次/秒。
- **数字：** 平均在途 120 秒（假设）：稳态 pending = 16.5 × 120 ≈ 2,000 笔；最坏每笔都被刷，2,000 ÷ 30 秒 = 67 次/秒 > 20，排不完但不放大成平台流量；任务 30 秒作废，队列最长约 2,000。预算：新建 50 + 刷新 20 + 扫描 20 = 90 次/秒，低于额度 100。
- **队列：** 把突发刷新变成平稳 20 次/秒；代价是多一个组件、至少一次投递；不用 Kafka，因为不需要回放也没有多消费者，托管队列就够。
- **回调一直没来：** 每日凌晨扫描兜底。选 `status='pending'` 且 created_at 早于 1 小时的（`(status, created_at)` 索引，每批 500）；有 vendor_transfer_id 就按 id 查，没有就用同一个键重发 createTransfer；结果都走 settle()。1 小时门槛是因为正常回调几分钟内到，更早的去查是浪费额度。
- **频率来自恢复窗口：** 恢复窗口一天，所以一天一次，最坏等 24 + 1 = 25 小时。假设 0.1% 回调丢：16.5 × 86,400 ≈ 143 万笔/天 × 0.1% ≈ 1,430 笔，按 20 次/秒约 72 秒扫完。
- **告警：** 最老 pending 超过 26 小时就叫人，另看 pending 超过 1 小时的笔数；扫描自己没跑也要告警。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 246">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">每日扫描：选谁 · 多快 · 怎么叫人</text>
<rect x="8" y="26" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">选谁：pending 且创建超过 1 小时</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">索引 (status, created_at)；每批 500 行</text>
<rect x="8" y="80" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="99.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">调谁：有 vendor id 按 id 查；无则同键重发</text>
<text x="18" y="114.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">限速 20 次/秒；结果走同一个事务</text>
<rect x="8" y="134" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="153.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">多快：1,430 笔/天 ÷ 20 次/秒 ≈ 72 秒</text>
<text x="18" y="168.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每天凌晨一次；最坏 24 + 1 = 25 小时</text>
<rect x="8" y="188" width="324" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="207.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">叫人：最老 pending 超过 26 小时就告警</text>
<text x="18" y="222.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">指标：pending &gt; 1 小时的笔数</text>
</svg>
白板上新增：读 pending 的流程图（窗口、抢名额、队列、限速 worker），和每日扫描的四件事。

**常见失分。**
- **读请求里同步问平台：** 用户刷新变成平台流量，平台慢读也慢。
- **刷新没有上限：** 无窗口、不去重、无全局限速，一次突发吃光额度。
- **只说「定期扫一下」：** 没有选择规则、频率、上限。
- **扫描另写一套更新逻辑：** 与 webhook 不一致，重复扫到可能改两次。
- **只有任务没有告警：** 扫描没跑没人知道。

**面试官可能接着问。**
- 平台说「还在处理」？ → 只更新 last_vendor_check_at，仍 pending。
- 为什么不每分钟扫？ → 恢复窗口是一天；每分钟扫会让同一笔卡住的转账从最多 1 次/天变成 1,440 次/天。
- 崩溃点 A 要等 25 小时才发出？ → 是；若业务要求提现 1 小时内发出，就给「vendor id 为空且超过 5 分钟」的行加每 5 分钟的小扫描，这种行只在崩溃时有，数量少；现在不加。
- 用户打开那笔转账呢？ → 有界刷新在 30 秒窗口内就会更新，不用等扫描。
