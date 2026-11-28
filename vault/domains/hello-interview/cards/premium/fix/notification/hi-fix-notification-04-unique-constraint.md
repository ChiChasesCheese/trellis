---
id: hi-fix-notification-04-unique-constraint
node: fix.notification
type: qa
step: 4
---
## Q
**通知系统 · 不发两封回执**｜复盘

面试官：「产品团队的请求超时，他们重试了。你怎么保证用户不收到两封支付回执？」

你会怎么回答？

## A
**当时的回答。** 先说「只插入一次」（23:31），这是目标不是机制；然后发现行还不存在锁不住（25:05），却没换方案，改成在服务里先查（25:27）；面试官 25:32 提示「the database enforces uniqueness」才说出「returns 0 rows」，从提问算起约 4 分钟。

**应该这样说。**
- **先说决定：** `notification_id` 做主键，`INSERT … ON CONFLICT DO NOTHING`；影响 1 行是第一次，去发送；0 行是重复，丢掉。
- **为什么不要锁和先查：** 行不存在没东西可锁；先查后插，同时到的两个重试都查不到、都插入，用户收到两封（面试官 23:36 已点出）；尖峰 83,000 次/秒再加一次库查询，会把刚用日志保护的库又打满。唯一约束在写入那一刻原子裁决，一个成功一个失败，查和写是同一条语句。
- **第二次调用：** 返回同样的 202 和同一个 notification_id，不是 409；调用方不需要分辨重试成没成功。
- **键是业务事件：** 调用方用 `receipt:` 加支付单号，重试永远是同一个键；他们坚持随机 id 时，再加 `UNIQUE (payment_order_id, kind)`。
- **放在 worker 里：** 请求路径只往日志追加；worker 取到消息做这一条 INSERT，日志里有两条重复消息，库里只有一行。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 187">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">产品团队超时重试：两次 POST，一条记录</text>
<rect x="8" y="26" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">第一次 POST pay_881</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">202，notification_id = receipt:pay_881</text>
<rect x="8" y="78" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="96.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">重试 POST pay_881</text>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">202，同一个 notification_id</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">日志里有两条，库里一行，用户一封</text>
<text x="8" y="165" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">去重键 = 业务事件（支付单号 + 种类）</text>
<text x="8" y="181" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不是每次请求新生成的随机 id</text>
</svg>
白板上：产品团队超时重试，两次 POST，一条记录。

**常见失分。**
- **锁：** 行都不存在，锁不住；分布式锁还多一个会过期的东西。
- **先查后插：** 并发的两个重试都查不到。
- **键由服务端生成：** 超时重试时调用方拿不到，等于没有键。

**面试官可能接着问。**
- 发送前崩溃？ → INSERT 成功后崩，这行一直是 queued；定时扫描把超过 1 分钟还是 queued 的行重发。
- 发出了但没记状态就崩？ → 可能再发一次，到供应商是至少一次；供应商支持去重键就带上 notification_id 再兜一层。
- 唯一索引一直长大？ → 去重键只需保留重试窗口：单独去重表，7 天约 3,500,000,000 个键，按天分区，到期整分区丢弃。
- 同一个键请求体不一样？ → 422，调用方的 bug，不发送。
