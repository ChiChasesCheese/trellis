---
id: hi-fix-airbnb-wallet-01-bound-vendor-call
node: fix.airbnb-wallet
type: qa
step: 1
---
## Q
**Airbnb Wallet · 待处理转账的状态**｜复盘

面试官：「用户打开一笔转账，它还是 pending。你怎么告诉用户现在是什么状态？」

你会怎么回答？

## A
**当时的回答。**
- **先读本地：** 你先读钱包和交易表，这一步是对的。
- **然后问外部：** 如果交易还是 pending，你说可以实时查一下支付平台（payment platform）。
**差在哪。**
- **pending 这一支没有上限：** completed、failed 直接返回没问题；pending 的转账每被刷新一次，就多打一次支付平台。
- **用户的读被外部拖住：** 支付平台一慢，用户的读跟着慢；一阵集中的刷新，就变成一阵打向支付平台的流量。
- **没说谁负责刷新：** 面试官听不到频率，也听不到上限，只听到「可能查一下」。
**应该这样说。**
- **先说规则：** 「用户能触发的外部调用，必须有新鲜度窗口。交易行上加 last_vendor_check_at，窗口我假设 30 秒。」
- **三种情况：** 「终态直接返回；pending 且 30 秒内查过，返回 pending，不调外部；pending 且超过 30 秒，往队列放一个刷新任务，仍然返回 pending。」
- **谁来刷新：** 「worker 调支付平台，再用一个数据库事务同时更新交易状态和钱包余额。用户的读永远不等支付平台。」
- **上限怎么算：** 「支付平台对每笔交易每个窗口最多看到一次刷新：10,000 笔 pending ÷ 30 秒 ≈ 333 次/秒，不再随用户刷新的速度变化。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 261">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">GET /transactions/{id}：先读本地一行</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">终态：completed / failed</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">直接返回</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不碰支付平台</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">pending，且 30 秒内查过</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">last_vendor_check_at 很新</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">返回 pending，不调外部</text>
<rect x="8" y="160" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">pending，且超过 30 秒</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">往队列放一个刷新任务</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">仍然立刻返回 pending</text>
<text x="8" y="255" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">用户的读从不等支付平台，只等自己的数据库</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 194">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同样 10,000 笔 pending，打向支付平台的次数</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">没有窗口：每笔每 2 秒被刷新一次</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">10,000 笔 ÷ 2 秒 = 5,000 次/秒</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">对方慢 1 秒：同时在飞 5,000 个</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">30 秒窗口：每笔每窗口一次</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">10,000 笔 ÷ 30 秒 ≈ 333 次/秒（上限）</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">再加全局上限 50 次/秒</text>
<text x="8" y="188" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">上限 = pending 笔数 ÷ 窗口秒数，与用户刷新多快无关</text>
</svg>
白板上：读路径的三个分支，加上有窗口和没窗口的调用次数对比。
**为什么这样说。** （约 1 分钟。）面试官在看你能不能管住「别人能触发的流量」。强的回答给出一个窗口、一个字段、一条上限公式；弱的回答是「实时查一下」，上限落在用户手里。
**面试官可能接着问。**
- 30 秒怎么定？ → 是假设：看支付平台的状态多久变一次、额度多大。窗口越短越新鲜，调用越多；上限 = 待处理笔数 ÷ 窗口。
- 用户盯着页面看怎么办？ → 前端每 5 秒读一次本地行，主键读很便宜；页面显示 last_checked_at，用户看到的是「30 秒前确认过，处理中」。
- 为什么返回 pending，不等刷新结果？ → 等就把用户的延迟绑在支付平台上；pending 本来就是真实状态。
**同类题。**
- **订单物流、股票报价：** 用户读触发外部取数，同一条规则，见「用户能触发的外部调用要有上限」。
- **GoFundMe 的 GET /donations/{id}：** 前端轮询 Pending 行，也是读本地，不直接问 PSP。
