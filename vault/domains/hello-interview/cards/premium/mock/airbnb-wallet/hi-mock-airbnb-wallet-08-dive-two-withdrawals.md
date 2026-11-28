---
id: hi-mock-airbnb-wallet-08-dive-two-withdrawals
node: fix.airbnb-wallet-mock
type: qa
step: 8
---
## Q
**Airbnb Wallet · 第 8 步 · 深入一：两笔不同的提现**｜模拟面试

面试官：「钱包里有 500 美元。两个不同的提现请求，各 500 美元，同时到达两台不同的服务器。会发生什么？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先答被问的：** 这是两笔不同的提现，不是同一笔重试；让数据库只放其中一笔进来。
- **唯一的操作：** 一条条件 UPDATE，把 500 美元（50,000 分）从可用挪到冻结，条件 `ready_to_use >= 50000`，检查和占用在同一条语句里。
- **一行还是零行：** 事务里先插入 pending 行（`(wallet_id, attempt_id)` 唯一，挡重发），再跑这条 UPDATE。1 行：我赢了，提交、返回 202，平台调用在事务之后。0 行：钱不够，回滚整个事务（含刚插的 pending 行），返回 409 insufficient_funds，不调平台。0 行不是错误，数据库不报错，不检查就继续会得到一笔没冻结的 pending 提现。
- **为什么只有一个赢：** UPDATE 先拿钱包行的行锁，第二个等第一个提交；Postgres 默认 READ COMMITTED 会按最新的行重新检查 WHERE，此时 ready_to_use 已是 0，更新 0 行。
- **为什么不先 SELECT 再 UPDATE：** 两个请求都读到 500、都通过、都扣，余额变 −500；CHECK 会拦第二个，但那是报错不是正常流程。
- **钱最后去哪：** 平台完成：冻结减 500；失败：冻结减 500、可用加回 500，与改状态同事务，释放不会漏。
- **重试是另一回事：** 同一次点击重发靠 `(wallet_id, attempt_id)` 唯一约束，返回首次那笔；一个机制管两笔不同的提现，一个管同一笔重发，不混。

```sql
UPDATE wallets
SET ready_to_use = ready_to_use - 50000, on_hold = on_hold + 50000
WHERE wallet_id = $w AND ready_to_use >= 50000;
-- 1 行：COMMIT，202 pending；0 行：ROLLBACK，409
```

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 242">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">三种手段，各解一个问题</text>
<rect x="8" y="28" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="48" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">条件 UPDATE</text>
<text x="18" y="63" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">管：两笔不同提现抢同一笔钱</text>
<text x="18" y="78" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不管：同一笔被重发</text>
<rect x="8" y="98" width="324" height="62" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="118" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">attempt_id 唯一</text>
<text x="18" y="133" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">管：同一次点击被重发</text>
<text x="18" y="148" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不管：两笔不同提现</text>
<rect x="8" y="168" width="324" height="62" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="188" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">行锁 FOR UPDATE</text>
<text x="18" y="203" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">管：读后写要同时改多行</text>
<text x="18" y="218" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不管：单行条件更新用不着</text>
</svg>
白板上新增：条件 UPDATE、两个请求的时序，和三种手段各管什么的对照。

**常见失分。**
- **先讲 transaction_id 和 attempt_id：** 那是重发，问的是两笔不同的提现。
- **先 SELECT 再 UPDATE：** 并发请求都读到 500，透支。
- **0 行不处理：** 继续 INSERT，得到没冻结的 pending 提现。
- **为一行余额上分布式锁：** 行锁已经做了这件事，还多一个会过期的东西。

**面试官可能接着问。**
- 500 美元，提现 300 和 300？ → 第一个可用剩 200、冻结 300；第二个 200 >= 300 为假，0 行，409，同一条语句。
- 第一笔后来失败，用户再提？ → 失败的同一事务把 500 退回可用，条件成立；释放冻结必须与改状态同事务，漏掉就是资金被卡住。
- 为什么先插入再 UPDATE？ → 先 UPDATE 的话，重发会因余额已冻结而返回 409，而不是首次那笔；先插入，重发在唯一约束上就被识别，不碰余额。
- 订座和库存同样吗？ → `UPDATE seats SET status='held' WHERE seat_id=$s AND status='available'`、`UPDATE stock SET n = n - 1 WHERE sku=$k AND n > 0`，都是检查和占用合一。
- 为什么不用 SELECT FOR UPDATE 或 SERIALIZABLE？ → 也对，但多一次往返或要处理序列化失败重试；谓词只依赖被写的这一行时条件 UPDATE 最简单，先读多行再决定才用它们。
