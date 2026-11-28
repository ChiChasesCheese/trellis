---
id: bagu-payment-idempotency-2-same-txn
node: a.idem.payment-idempotency
type: qa
step: 2
---
## Q
**支付幂等 · 幂等记录为什么与业务同事务**｜必会

面试官：「幂等记录和业务写入为什么必须放在同一个事务里？流程是什么？」

## A
**基本回答。** 在同一个数据库事务里，先 `INSERT` 一条幂等记录（状态 `PROCESSING`，处理中），接着执行业务写入；业务做完，把记录更新成 `DONE` 并保存响应，一起提交。第二个请求带着同一个键进来，插入时会撞主键，这时就去读已有的记录，决定回放还是等待。MySQL 8.0.46 实测：余额 1000 扣 100，第二次插入 `K1` 报 1062，余额只减一次（900）。并发的相同 key 会在数据库里等第一个事务：它提交了第二个撞键，回滚了第二个就能继续做。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 290">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">第一次请求：同一个数据库事务里做三件事</text>
<rect x="8" y="24" width="324" height="142" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="20" y="34" width="300" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="52.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① 插幂等记录 K1：PROCESSING</text>
<line x1="170" y1="62" x2="170" y2="72" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,72.0 166.8,65.0 173.2,65.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="20" y="72" width="300" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="90.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② 业务写入：扣余额</text>
<line x1="170" y1="100" x2="170" y2="110" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,110.0 166.8,103.0 173.2,103.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="20" y="110" width="300" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="128.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ 改成 DONE，存下响应</text>
<text x="170" y="160" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">一起 COMMIT，要么都成功要么都回滚</text>
<text x="8" y="190" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">第二次请求：同一个 K1 又来了</text>
<rect x="8" y="198" width="90" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="53.0" y="216.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">K1 又来</text>
<line x1="98" y1="212" x2="118" y2="212" stroke-width="1.2" stroke="currentColor"/>
<polygon points="118.0,212.0 111.0,215.2 111.0,208.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="118" y="198" width="214" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="225.0" y="216.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">撞主键（错误 1062），读已有记录</text>
<line x1="80" y1="226" x2="80" y2="244" stroke-width="1.2" stroke="currentColor"/>
<polygon points="80.0,244.0 76.8,237.0 83.2,237.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="250" y1="226" x2="250" y2="244" stroke-width="1.2" stroke="currentColor"/>
<polygon points="250.0,244.0 246.8,237.0 253.2,237.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="246" width="150" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="83.0" y="265.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">DONE → 回放响应</text>
<rect x="182" y="246" width="150" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="257.0" y="265.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">PROCESSING → 409</text>
</svg>
上半是第一次请求，三个动作包在同一个事务（虚线框）里一起提交；下半是第二次相同 key 的请求撞主键之后的两条分支。
**容易错。**
- **分两个事务：** 先单独提交幂等记录再扣款，崩在中间则重试看到记录就认为做过了，丢单；先扣款再写记录，崩在中间则重试找不到记录，重复扣款。
- **PROCESSING 不设超时：** 崩溃后记录卡在处理中，这笔扣款永远处理不了，也永远无法重试。
- **撞键就直接报错：** `DONE` 应当回放第一次的响应，客户端感觉不到重复；只有还在处理才返回 409。
- **以为同事务没有 PROCESSING：** 并发的相同 key 会在数据库里等第一个事务；但先提交占位记录、再去调外部渠道的流程里，别人就能读到 `PROCESSING`，所以这个分支仍然要处理。

