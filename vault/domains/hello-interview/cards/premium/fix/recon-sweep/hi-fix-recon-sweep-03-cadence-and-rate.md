---
id: hi-fix-recon-sweep-03-cadence-and-rate
node: fix.recon-sweep
type: qa
step: 3
---
## Q
**回调是常态路径 · 频率和限速**｜补强

面试官：「扫描多久跑一次？它会不会把支付平台打爆？比如你们的 webhook 挂了两个小时之后。」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **频率从恢复窗口推出来：** 「产品要求丢失的回调 24 小时内补上，所以扫描间隔不能超过 24 小时，我选每天一次，凌晨低峰。严格算，1 小时的门槛加一天的间隔，最长约 25 小时；要卡死 24 小时，就改成每 12 小时一次。如果要求是 1 小时内，就改成每小时。」
- **任务本身也要被监控：** 「凌晨 2 点开始，4 点还没有完成记录就告警，当天再手动重跑，仍在窗口里。」
- **平时的量：** 「每天约 14,300 笔需要问平台；限速 10 次/秒，14,300 ÷ 10 = 1,430 秒，约 24 分钟。」
- **限速和用户刷新共用上限：** 「全局上限 50 次/秒，其中扫描最多 10 次/秒，不会把用户刷新的额度占光，也不会被它们挤掉。」
- **webhook 挂了 2 小时：** 「16.5 笔/秒 × 7,200 秒 ≈ 119,000 笔积压，加平时的 14,300，约 133,000 笔；133,000 ÷ 10 ≈ 13,300 秒，约 3.7 小时，仍在 24 小时窗口内。没有限速，133,000 个调用会一次冲向平台。」
- **扫描可以重跑：** 「每批按游标，状态落库是条件更新，跑两遍结果一样。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 179">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">频率与限速，各用一个数字推出来</text>
<rect x="8" y="26" width="324" height="74" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">频率：来自恢复窗口</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">要求：丢失的回调 24 小时内补上</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">扫描间隔 ≤ 24 小时：每天一次，凌晨</text>
<text x="18" y="89.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">窗口缩到 1 小时，就按小时跑</text>
<rect x="8" y="108" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">限速：和用户刷新共用上限</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">总上限 50 次/秒；扫描最多占 10 次/秒</text>
<text x="18" y="156.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">14,300 次 ÷ 10 = 1,430 秒 ≈ 24 分钟</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 231">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">webhook 挂了 2 小时之后的那次扫描</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">积压</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">16.5 笔/秒 × 7,200 秒 ≈ 119,000 笔</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">加上平时的 14,300，约 133,000 笔</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">不限速</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">一次性 133,000 个调用冲向平台</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">被 429，用户刷新也被挤掉</text>
<rect x="8" y="160" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">限速 10 次/秒</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">133,000 ÷ 10 ≈ 13,300 秒 ≈ 3.7 小时</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">仍在 24 小时窗口内</text>
</svg>
白板上：频率一行、限速一行，旁边画 2 小时故障的三行数字。
**为什么这样说。** （约 1 分钟。）面试官要一个频率和一个调用量，两个都有来历。强的回答把频率写成「窗口」的函数，把调用量写成速率除以额度；弱的回答是「每天扫一次」或「定期轮询」。
**面试官可能接着问。**
- 为什么不实时轮询所有 pending？ → 每笔转账平均几分钟内由 webhook 收尾，实时轮询是把平台额度花在绝大多数不需要的行上；扫描只处理异常。
- 窗口收紧到 1 小时呢？ → 扫描改成每小时一次，选择规则里的 1 小时也要缩小，否则每次都扫到还在处理的行；同时检查额度还够不够。
- 平台限额是 20 次/秒呢？ → 总上限取 10，扫描只占 2；2 小时故障后清完要 133,000 ÷ 2 = 66,500 秒，约 18.5 小时，仍在 24 小时内，但已经没有余量，应该告警并和平台沟通。
**常见失分。**
- **频率没有来历：** 「每天」是不是对的，说不出为什么。
- **不限速：** 故障之后的积压把平台打到 429。
- **占光额度：** 扫描挤掉用户的刷新。
