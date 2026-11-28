---
id: bagu-outbox-1-why-outbox
node: a.idem.outbox
type: qa
step: 1
---
## Q
**本地消息表（Outbox）· 怎么保证业务和消息一致**｜必会

面试官：「支付成功后，订单服务要把状态改成已支付，还要发一条消息通知发货。你先改库再发消息队列（MQ），进程恰好在两步之间崩了，会怎样？怎么保证状态改了消息就一定会发？」

## A
**基本回答。** 数据库和 MQ 是两个独立系统，没有事务能同时管住它们，先写库后发消息崩在中间则下游永远不知道，先发后写库回滚则消息无中生有，这是双写问题（dual write）。办法是把「要发的消息」当成数据库里的一行：业务表更新和 outbox（发件箱）表插入放进同一个本地事务，要么都提交要么都回滚。提交之后，再由别的进程（中继）把 outbox 里的消息发到消息队列（MQ）。崩溃只会让消息晚发，不会丢。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 246">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">直接双写：两个系统，没有共同事务</text>
<rect x="8" y="26" width="110" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="63" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">改订单库</text>
<line x1="118" y1="41" x2="193" y2="41" stroke-width="1.2" stroke="currentColor"/>
<polygon points="200.0,41.0 193.0,44.2 193.0,37.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="200" y="26" width="110" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="255" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">发 MQ</text>
<text x="159" y="36" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">崩</text>
<text x="8" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">崩在两步之间：库变了，消息没发</text>
<rect x="8" y="92" width="324" height="76" rx="4" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="14" y="106" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同一个本地事务：要么都提交，要么都回滚</text>
<rect x="18" y="124" width="138" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="87" y="137.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">orders</text>
<text x="87" y="152.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">状态改成已支付</text>
<rect x="176" y="124" width="146" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="249" y="137.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">outbox</text>
<text x="249" y="152.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">插一行待发消息</text>
<line x1="249" y1="168" x2="249" y2="179" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="249.0,186.0 245.8,179.0 252.2,179.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="257" y="182" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">提交之后</text>
<rect x="150" y="190" width="100" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="200" y="209" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">中继进程</text>
<line x1="250" y1="205" x2="265" y2="205" stroke-width="1.2" stroke="currentColor"/>
<polygon points="272.0,205.0 265.0,208.2 265.0,201.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="272" y="190" width="60" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="302" y="209" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">MQ</text>
<text x="8" y="238" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">崩溃只会让消息晚发，不会丢</text>
</svg>
上半是直接双写：两步之间崩了就一边变了一边没变。下半是 outbox：改状态和写消息被框在同一个本地事务里，框外的中继只管把已经落库的消息送走。
**代码。** 业务更新和消息写入在同一个事务里：
```sql
START TRANSACTION;
UPDATE orders SET status = 'PAID' WHERE id = 1;       -- 业务变更
INSERT INTO outbox(msg_id, biz_key, payload)           -- 待发消息，同一事务
VALUES ('M0001', 1, '{"e":"paid"}');
COMMIT;
```
**容易错。**
- **以为 outbox 能做到恰好一次：** 它保证的是「不丢」（至少一次）；消息可能重发，消费端要自己去重。
- **把发 MQ 写进事务里：** 看起来也是「一起」，但 MQ 不会跟着回滚，而且拖长事务。
- **以为发完就不用管：** 未发送的行数和最老一行的年龄要监控，积压了要报警。
- **以为这样就强一致：** 下游看到消息有延迟，这是最终一致。

**业务场景。** 订单服务处理支付成功回调时，在一个事务里把订单改成已支付并写入 outbox；写完后进程被重启，中继起来照样把「已支付」发给发货服务，没有出现「钱收了不发货」。
