---
id: hi-fix-airbnb-wallet-05-refresh-policy
node: fix.airbnb-wallet
type: qa
step: 5
---
## Q
**Airbnb Wallet · 刷新 pending 的策略**｜复盘

面试官：「getTransactionStatus 怎么实现？pending 的转账，什么时候只读本地，什么时候去问支付平台？」

你会怎么回答？

## A
**当时的回答。**
- **读本地：** 先读本地的钱包和交易表，这是对的。
- **然后设想同步调用：** pending 时在用户读请求里直接调支付平台。
**差在哪。**
- **没有策略：** 没有新鲜度窗口、没有限速、没有后台的刷新机制，三项都没说。
- **面试官没法判断「什么时候」：** 他问的就是条件；答案里只有一个动作，没有条件。
- **重复刷新没人管：** 同一笔交易被很多请求同时读到，会有很多个刷新同时出发。
**应该这样说。**
- **读的返回：** 「读本地行，返回 status 和 last_checked_at；用户能看到这个状态是多久前确认的。」
- **三种情况：** 「终态立刻返回；pending 且新，不调外部；pending 且旧，入队一个按 transaction_id 去重的刷新任务，返回 pending。」
- **一笔一个：** 「入队之前用一条条件 UPDATE 抢占，影响 1 行的那个请求才入队，其余直接返回。建 pending 行时就把 last_vendor_check_at 设成 now()，不留 NULL，否则「NULL < 时间」永远不成立，新行永远抢不到。」
- **限速：** 「worker 调支付平台受一个全局 QPS 上限约束，我假设额度 100 次/秒，自己取 50。」
- **写回：** 「worker 在一个数据库事务里，把 status 从 pending 改成终态，同时更新钱包的 ready_to_use 和 on_hold。」
**白板。**
```
def get_transaction_status(txn_id):
    t = db.get(txn_id)        # 主键读
    if t.status != "pending":
        return t              # 终态直接返回
    if claim_refresh(txn_id): # 1 行才入队
        queue.send(txn_id)
    return t                  # 仍是 pending

def claim_refresh(txn_id):
    # 建行时 last_vendor_check_at = now()
    return db.execute(
      "UPDATE transactions "
      "SET last_vendor_check_at = now() "
      "WHERE id = %s "
      "AND status = 'pending' "
      "AND last_vendor_check_at "
      "  < now() - interval '30 seconds'",
      txn_id).rowcount == 1
```

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 230">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">getTransactionStatus：读、抢占、排队、刷新</text>
<rect x="8" y="26" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">用户读</text>
<text x="170" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">读本地行：status + last_checked_at</text>
<polyline points="170,70 170,108" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,108 166.8,101 173.2,101" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="176" y="93" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">pending 且超过 30 秒</text>
<rect x="8" y="108" width="324" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="126.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">条件 UPDATE 抢占</text>
<text x="170" y="141.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">影响 1 行的那个请求入队</text>
<polyline points="170,152 170,182" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,182 166.8,175 173.2,175" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="176" y="171" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">transaction_id</text>
<rect x="8" y="182" width="324" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="200.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">worker · 全局上限 50 次/秒</text>
<text x="170" y="215.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">调支付平台，一个事务落状态和余额</text>
</svg>
白板上：读路径画到队列为止，worker 画在限速旁边。
**为什么这样说。** （约 1 分钟。）面试官问的是条件和上限。强的回答把「读本地、抢占、入队、限速、一个事务落库」每一步说出来，没有一步是「可能」；弱的回答停在「实时查一下」。
**面试官可能接着问。**
- 抢占时就写了 last_vendor_check_at，worker 查失败了呢？ → 它表示「最近一次尝试」；失败也要等下一个窗口再来，平台出问题时不会被重试风暴打；页面显示「最近一次检查」。
- 抢占之后、入队之前服务崩了呢？ → 这次刷新丢了；下一个窗口的读会再抢占，最多晚一个窗口，每日扫描也兜底。
- 队列里的消息放什么？ → 只放 transaction_id；worker 取出后重新读行，已是终态就丢弃，这样任务重复也无害。
- 全局上限怎么实现？ → 所有 worker 共用一个令牌桶，每秒 50 个令牌；拿不到就等下一秒。
**同类题。**
- **订单物流、股票报价：** 键换成运单号或股票代码，窗口和上限换成各自的数字。
- **GoFundMe 的结算任务：** 后台按固定频率处理 Pending，不由用户读驱动。
