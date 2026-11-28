---
id: hi-fix-retry-key-10-unique-constraint
node: fix.retry-key
type: qa
step: 10
---
## Q
**通知系统 · 唯一约束就是幂等的答案**｜补强

面试官：「产品团队的请求超时了，他们重试。你怎么保证用户不会收到两张支付回执？两个一模一样的重试还可能同时到达。」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **结论：** notification_id 上建唯一约束，`INSERT … ON CONFLICT DO NOTHING`，数据库原子地只放一条进来；不用锁，也不用先查。
- **第二次调用：** 受影响 0 行即重复，服务读出已有行，返回与第一次相同的 202 和同一个 notification_id（状态用 GET 查），不再发送。同 id 内容不同（存请求内容的哈希比对）返回 422，是调用方 bug，不是重试。
- **为什么不用锁：** 第一次到达时那行还不存在，没东西可锁；锁服务多一次往返且锁会过期。唯一索引本身就是那把锁：第二个插入者等第一个提交，然后失败。
- **为什么不先查：** 两个同时到达的请求都查到「没有」都插入，用户收到两张回执；峰值 83,000 次/秒还多 83,000 次查询。唯一约束一条语句完成检查和占位。
- **放在哪一步：** 请求路径只校验、追加日志（acks=all）、返回 202；INSERT 在日志后的 worker 里，1 行才发送，0 行跳过并确认日志消息；20 片 ≈ 4,150 行/秒/片。
- **崩溃窗口：** INSERT 成功、没发出就崩：行是 pending，重试得 0 行被跳过；所以 pending 超过 1 分钟没变的行由扫描补发，发给供应商带 notification_id 做幂等键。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 233">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">三种做法，只有一种对</text>
<rect x="8" y="26" width="324" height="61" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">分布式锁 ✗</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一开始那一行还不存在，没有东西可锁</text>
<text x="18" y="75.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">多一次往返，锁还会过期</text>
<rect x="8" y="95" width="324" height="61" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="114.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">先查再插 ✗</text>
<text x="18" y="129.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">两个请求都查到「没有」，都插入</text>
<text x="18" y="144.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">峰值多 83,000 次查询/秒</text>
<rect x="8" y="164" width="324" height="61" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="183.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">唯一约束 + ON CONFLICT ✓</text>
<text x="18" y="198.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">一条语句检查并占位，数据库裁决</text>
<text x="18" y="213.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">第二次 0 行 = 重复</text>
</svg>
白板上：一条带 ON CONFLICT 的 INSERT；两个同时到达的请求，一个得 1 行、一个得 0 行；再画三种做法的对照。

**常见失分。**
- **一上来说分布式锁：** 那行根本还不存在。
- **请求路径里先查一次：** 先查再插，并发的两个都能通过。
- **只用 Redis SETNX：** 主从切换或过期都会丢；兜底必须是数据库唯一约束。
- **重复就报错：** 重试是正常流程，不该让调用方看到失败。
- **不处理崩在插入之后：** 行 pending 却没发出，要有扫描补发。

**面试官可能接着问。**
- 两请求在不同服务器，要分布式锁吗？ → 不要，竞争的是库里同一个键，唯一索引已让它们排队。
- 分片后唯一约束还成立吗？ → 只在单分片内成立，所以分片键用 notification_id。
- 第二次调用能返回 409 吗？ → 可以，但调用方只想知道「已经有了」，原样返回第一次结果更友好。
