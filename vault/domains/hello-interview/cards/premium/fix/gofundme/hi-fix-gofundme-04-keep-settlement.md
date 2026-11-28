---
id: hi-fix-gofundme-04-keep-settlement
node: fix.gofundme
type: qa
step: 4
---
## Q
**GoFundMe · 第 24:34 分 · 保持：挂起捐款的结算**｜复盘

面试官：「PSP 超时了，捐款人不知道到底扣了没有。你怎么办？」

你会怎么回答？

## A
**当时的回答。**
- **不当成失败：** 超时的捐款留在 Pending。
- **结算任务：** 一个任务定期取出 Pending 的行。
- **同一个编号去问：** 用保存下来的 donation UUID 当订单引用去查 PSP，再把已有的行更新成成功或失败。
**差在哪。**
- **这段不用改：** 行、PSP 查询、重试、最终状态，面试官能顺着听完。
- **只差一个收口：** 没说 PSP 查不到这一单时怎么办；补上这一句就完整了。
**应该这样说。**
- **照旧说：** 「超时不是失败。我保持 Pending，结算任务按 donation_id 问 PSP，只更新这一行，不新建捐款。」
- **补一句查不到：** 「PSP 查不到这一单，说明没扣款：我把这一笔标 Failed；捐款人再点一次就是新的 key。」
- **补一句时限：** 「每分钟扫描超过 60 秒的 Pending。PSP 的幂等记录通常只保留约一天，具体以所用 PSP 的文档为准，所以必须在窗口内查清。」
- **为什么用同一个编号：** 「同一个编号让「查」和「重试」都落在同一笔上，而不是凭用户和金额去猜。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 286">
<rect x="16" y="8" width="88" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="60" y="23.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">结算任务</text>
<text x="60" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每分钟</text>
<rect x="126" y="8" width="88" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<rect x="236" y="8" width="88" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="280" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">PSP</text>
<text x="64" y="72" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">扫 Pending 超过 60 秒</text>
<polyline points="60,84 170,84" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,84 163.0,87.2 163.0,80.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="64" y="106" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">donation_id 列表</text>
<polyline points="170,118 60,118" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="60,118 67.0,114.8 67.0,121.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="64" y="140" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">按 donation_id 查订单</text>
<polyline points="60,152 280,152" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="280,152 273.0,155.2 273.0,148.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="64" y="174" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">已扣款 / 已拒绝 / 无此单</text>
<polyline points="280,186 60,186" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="60,186 67.0,182.8 67.0,189.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="64" y="208" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">更新同一行</text>
<polyline points="60,220 170,220" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,220 163.0,223.2 163.0,216.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="104.32" y="234" width="131.36" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="248" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Success 或 Failed</text>
<text x="8" y="274" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不新建、不重扣；只把已有的行推到终态</text>
<line x1="60" y1="48" x2="60" y2="263" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="60" y1="278" x2="60" y2="282" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="48" x2="170" y2="61" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="76" x2="170" y2="95" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="110" x2="170" y2="129" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="144" x2="170" y2="163" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="178" x2="170" y2="232" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="256" x2="170" y2="263" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="278" x2="170" y2="282" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="280" y1="48" x2="280" y2="282" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>
白板上：结算任务、数据库、PSP 三方；结算只把已有的行推到终态。
**面试官可能接着问。**
- 结算任务自己崩了怎么办？ → 它无状态，下一轮重新扫；每次只把行推到终态，重复执行结果一样。
- 结算和一个迟到的响应同时更新同一行呢？ → 条件更新：UPDATE … WHERE status = 'Pending'。只有一个影响 1 行，另一个影响 0 行，直接跳过。
- 用户一直等着怎么办？ → 前端轮询 GET /donations/{id}；看到 Pending 就显示「处理中」，不让他再付一次。
**同类题。**
- **限时捐款网站：** 结果未知的对账。
- **Payment System、钱包转账：** 转账悬在中间状态时的结算。
- **Robinhood 下单：** 订单已发出、成交回报丢了。
- **Uber 支付：** 行程结束后扣款超时。
