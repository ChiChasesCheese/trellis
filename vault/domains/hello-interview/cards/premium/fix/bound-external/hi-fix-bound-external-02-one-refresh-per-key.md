---
id: hi-fix-bound-external-02-one-refresh-per-key
node: fix.bound-external
type: qa
step: 2
---
## Q
**用户能触发的外部调用 · 一笔一次刷新**｜补强

面试官：「十台服务器同时收到同一笔 pending 转账的读请求，每台都发现它过期了。会不会各自去问一遍支付平台？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **键是交易，不是用户，也不是请求：** 「刷新的键是 transaction_id；一笔交易在一个窗口里只有一个刷新任务。」
- **用一条条件 UPDATE 抢占：** 「入队之前先执行下面这条；影响 1 行的那个请求才入队，影响 0 行的直接返回 pending。建行时就把 last_vendor_check_at 设成 now()，不留 NULL，否则「NULL < 时间」永远不成立。」
- **队列里只放 ID：** 「消息只有 transaction_id；worker 取出后重新读这一行，已经是终态就丢弃，所以重复的任务也无害。」
- **崩在中间：** 「抢占成功、入队之前崩了，这次刷新丢了；30 秒后下一次读会再抢占，最多晚一个窗口，每日扫描也兜底。」
- **worker 成功之后：** 「在一个事务里 UPDATE status WHERE status = pending，再更新钱包；0 行说明别人已经落了终态。」
**白板。**
```
UPDATE transactions
SET last_vendor_check_at = now()
WHERE id = $1
  AND status = 'pending'
  AND last_vendor_check_at
      < now() - interval '30 seconds';
-- 1 行：入队；0 行：已有人排过
-- 建行时 last_vendor_check_at = now()
```

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 196">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同一笔交易，10 台服务器同时发现它过期</text>
<rect x="8" y="26" width="324" height="29" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10 个请求 · 同一个 transaction_id</text>
<polyline points="170,55 170,89" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,89 166.8,82 173.2,82" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="176" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">条件 UPDATE 抢占</text>
<rect x="8" y="89" width="158" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="87" y="107.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">1 个返回 1 行</text>
<text x="87" y="122.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">入队刷新任务</text>
<rect x="174" y="89" width="158" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="253" y="107.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">9 个返回 0 行</text>
<text x="253" y="122.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">直接返回 pending</text>
<polyline points="90,133 90,163" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="90,163 86.8,156 93.2,156" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="96" y="152" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">transaction_id</text>
<rect x="8" y="163" width="324" height="29" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="181.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">队列：每笔每窗口最多一个任务</text>
</svg>
白板上：10 个请求进来，1 个入队，9 个直接返回。
**为什么这样说。** （约 1 分钟。）这是「先答被问的竞态」在读路径上的版本：多个请求抢同一个动作，由数据库放行一个。强的回答说出键和那条语句；弱的回答是「用一个去重的队列」，没有说去重发生在哪里。
**面试官可能接着问。**
- 为什么不用 Redis 的 SET NX EX 30 抢占？ → 也可以，键 refresh:{id}，30 秒过期；代价是又多一个要保证可用的组件，而数据库行本来就在手边。
- last_vendor_check_at 在抢占时就写了，worker 失败怎么办？ → 它表示「最近一次尝试」；失败就等下一个窗口再来，worker 对失败退避重试，但每次尝试都受窗口和全局上限约束。
- 队列本身重复投递呢？ → worker 先读行，终态就丢弃；仍是 pending 才调外部，状态落库是条件更新，所以重复执行结果不变。
**常见失分。**
- **以键为用户：** 十个用户看同一笔，仍然发十次。
- **先查后排：** 两个请求都查到「过期」，都入队；检查和占用要是同一条语句。
- **在队列里放整行数据：** 任务执行时数据已经变了，应该放 ID，执行时重读。
