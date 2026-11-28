---
id: bagu-payment-system-2-state-machine
node: a.scenario.payment-system
type: qa
step: 2
---
## Q
**订单与支付单状态机 · 并发下谁能把状态改过去**｜必会

面试官：「订单和支付单的状态怎么设计？支付成功回调和超时关单任务同一秒到达，怎么保证不出错？」

## A
**基本回答。** 订单 `CREATED → PAID` 或 `CREATED → CLOSED`；支付单 `INIT → PROCESSING → SUCCESS / FAILED`，分开是因为一个订单可有多次支付尝试（第一次失败再换卡）。终态不回退，否则答不出「这笔钱怎么走到这一步」；每次转换在同一事务里写状态流水便于审计。不能先 SELECT 再 UPDATE：两个请求同毫秒都读到 CREATED，各写 PAID 和 CLOSED，后写覆盖先写。条件放进 `WHERE`，检查和修改成为一条原子语句，行锁让并发请求排队，后到的匹配 0 行；代码只看影响行数，1 是赢了继续后续动作（通知发货、入账），0 是别人先改了。只加行锁、不带条件没用，后拿锁的照样会把 PAID 改成 CLOSED。成功回调晚于关单时钱已到账而订单是 `CLOSED`，不能悄悄改回 `PAID`（座位或库存可能已放给别人），要走退款或人工恢复。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<rect x="4" y="6" width="160" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="84.0" y="27.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">回调：改成 PAID</text>
<rect x="176" y="6" width="160" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="256.0" y="27.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">关单：改成 CLOSED</text>
<rect x="70" y="84" width="200" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="100.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">订单 7 一行记录</text>
<text x="170.0" y="115.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">status = CREATED</text>
<line x1="84" y1="40" x2="125.6641488571138" y2="79.85266412419581" stroke-width="1.2" stroke="currentColor"/>
<polygon points="130.0,84.0 123.6,82.0 127.7,77.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="256" y1="40" x2="214.33585114288618" y2="79.85266412419581" stroke-width="1.2" stroke="currentColor"/>
<polygon points="210.0,84.0 212.3,77.7 216.4,82.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="70" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">抢同一行的锁</text>
<rect x="4" y="160" width="164" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="86.0" y="181.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">先拿到锁：影响 1 行</text>
<rect x="176" y="160" width="160" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="256.0" y="181.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">后到的：影响 0 行</text>
<line x1="130" y1="124" x2="90.64374379521993" y2="156.20057325845642" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="86.0,160.0 88.7,153.9 92.5,158.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="210" y1="124" x2="249.35625620478007" y2="156.20057325845642" stroke-width="1.2" stroke="currentColor"/>
<polygon points="254.0,160.0 247.5,158.5 251.3,153.9" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="224" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0 行 = 状态已被改走，什么都不做</text>
</svg>
两个动作同时改订单 7：先拿到行锁的生效，后到的发现状态不再是 CREATED，更新 0 行。
**举个例子。** 订单 7 在 15:00 创建，15:15 到期关单。15:14:59 付款回调与 15:15:00 关单任务抢同一行：回调先拿锁，CREATED 改成 PAID 影响 1 行并通知发货；关单随后拿锁，status 已是 PAID，影响 0 行，什么也不做。顺序反过来则关单赢、回调 0 行，转退款或人工恢复。
```sql
UPDATE pay_order SET status='PAID'   WHERE id=? AND status='CREATED';
UPDATE pay_order SET status='CLOSED' WHERE id=? AND status='CREATED';
```
**容易错。**
- **以为条件不满足会报错：** UPDATE 不报错，只是影响 0 行，必须检查。
