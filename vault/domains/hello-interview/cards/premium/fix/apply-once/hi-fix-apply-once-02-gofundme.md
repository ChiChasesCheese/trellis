---
id: hi-fix-apply-once-02-gofundme
node: fix.apply-once
type: qa
step: 2
---
## Q
**GoFundMe 募款总额 · 只应用一次**｜补强

面试官：「你说用 Redis 存活动的已筹金额。如果 worker 在处理消息时崩了，或者消息被重放，这个数会怎样？它又怎么保证每笔捐款只被算进去一次？而且还没付成功的捐款不该算进去。」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **触发点：** 只有状态转到 SUCCESS 的那次事务才发 `DonationCompleted(donation_id, campaign_id, amount)`；PENDING 和被拒绝的不发，所以创建时不加总额。
- **可靠发出：** 状态改成 SUCCESS 和 outbox 事件行同一事务写入，中继再发到队列：不会「成功了没事件」，代价是事件可能投递多次，所以 worker 自己防重复。
- **worker 一个事务：** 先 INSERT 已应用表 `ON CONFLICT (donation_id) DO NOTHING RETURNING amount`；返回了行才 `UPDATE campaign_totals SET amount = amount + :amt`，再提交。重放时 INSERT 冲突、返回 0 行、不加；崩在提交前则整个回滚、重投后重做。
- **Redis：** 提交之后 `SET campaign:{id}:total <刚提交的值>`，不用 INCRBY，重复执行结果一样；SET 前崩了，下一个事件或定时刷新补上。
- **热门活动：** 一行总额每事务更新一次太慢；按 campaign_id 分区，一批事件一个事务：多行 INSERT … RETURNING 求和，一次 UPDATE。
- **验证：** 定期 `SELECT SUM(amount) … status = 'SUCCESS'` 和 `campaign_totals` 对账，不一致就是 bug。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 218">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">worker 一个事务，三句话</text>
<rect x="8" y="26" width="324" height="136" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">INSERT INTO campaign_total_applied</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">  (donation_id, campaign_id, amount)</text>
<text x="18" y="75.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">  VALUES (…) ON CONFLICT (donation_id)</text>
<text x="18" y="90.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">  DO NOTHING RETURNING amount;</text>
<text x="18" y="105.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">-- 返回 0 行：重放，到此为止</text>
<text x="18" y="120.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">UPDATE campaign_totals</text>
<text x="18" y="135.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">  SET amount = amount + &lt;返回的和&gt;</text>
<text x="18" y="150.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">  WHERE campaign_id = :c;  COMMIT;</text>
<text x="8" y="184" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">提交之后：SET campaign:{id}:total &lt;amount&gt;</text>
<text x="8" y="202" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">批处理：多行 VALUES，一次 UPDATE</text>
</svg>
白板上：worker 的三句话，返回 0 行就是重放。

**常见失分。**
- **创建时就 INCR：** 没付成功的捐款也进了总额。
- **只说「队列加事务」：** 事务不知道上一次提交过什么；已应用表要和加法同一事务提交，否则崩在中间少加或多加。
- **Redis 用 INCRBY 更新：** 重放一次多算一次。

**面试官可能接着问。**
- 两个 worker 同时处理同一活动，Redis 会被旧值覆盖吗？ → 按 campaign_id 分区只有一个 worker；再保险就让总额行带 `version`，Lua 只在新 version 更大时 SET。
- 已应用表会无限增长吗？ → 按月分区，队列保留期之外的旧分区可归档删除。
- 为什么不每次 `SELECT SUM`？ → 热活动每秒几千次打主库，只适合对账。
