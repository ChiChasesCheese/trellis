---
id: hi-fix-recon-sweep-04-alert-on-age
node: fix.recon-sweep
type: qa
step: 4
---
## Q
**回调是常态路径 · 怎么知道兜底在工作**｜补强

面试官：「扫描任务自己也可能挂。你怎么知道有转账卡在 pending？卡住之后谁来处理？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **四层，规则相同：** 「webhook 是常态；用户读之后最多 30 秒会触发一次刷新；每天扫描兜底；超过窗口两倍还没收尾的，开工单。四层用的是同一个事务规则，所以谁先到都安全。」
- **告警一，最老 pending 的年龄：** 「now() − min(created_at) 超过 48 小时，也就是窗口的 2 倍，就告警；有 (status, created_at) 索引，这个查询是一次索引读。」
- **告警二，扫描心跳：** 「凌晨 4 点前没有扫描的完成记录，就告警，说明任务没跑或者半路死了。」
- **告警三，补回比例：** 「每天扫描补回的笔数除以当天转账数，超过 1%（约 14,300 笔，就是前面估容量用的那个假设），或者高出前 7 天均值 3 倍，说明 webhook 本身有问题，去查 endpoint 和验签。」
- **人工那一层：** 「超过 48 小时：工单带着 transaction_id 和 vendor_transfer_id，让运营和平台对账；资金不动，on_hold 继续冻着。」
- **成本：** 「多三个指标和一个值班流程，换来的是不会悄悄丢一笔转账。」
**白板。**
```
SELECT now() - min(created_at)
         AS oldest_pending
FROM transactions
WHERE status = 'pending';
-- > 48h : alert
```

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 238">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">四层，谁先到谁收尾，规则相同</text>
<rect x="8" y="26" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">① webhook：常态</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">几秒到几分钟；改状态和钱包</text>
<rect x="8" y="78" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="96.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">② 用户读触发的刷新</text>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">读之后最多 30 秒；受全局上限</text>
<rect x="8" y="130" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="148.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">③ 每日扫描：兜底</text>
<text x="18" y="163.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">pending 且超过 1 小时；24 小时内补上</text>
<rect x="8" y="182" width="324" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="200.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">④ 告警和人工</text>
<text x="18" y="215.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">pending 超过 48 小时：开工单，查账</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 201">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">三个告警，各一个阈值</text>
<rect x="8" y="26" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">最老 pending 的年龄</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">超过 48 小时（窗口的 2 倍）</text>
<rect x="8" y="78" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="96.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">扫描心跳</text>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">凌晨 4 点前没有完成记录</text>
<rect x="8" y="130" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="148.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">扫描补回的比例</text>
<text x="18" y="163.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">补回 ÷ 当天转账 &gt; 1%（14,300）</text>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">说明 webhook 本身有问题</text>
</svg>
白板上：四层各一行，旁边是三个告警和阈值。
**为什么这样说。** （约 1 分钟。）面试官看你的兜底有没有「兜底的兜底」。强的回答给出可观察的指标和阈值，并说出谁来处理；弱的回答是「加监控」，没有说监控什么。
**面试官可能接着问。**
- 为什么阈值是 48 小时？ → 窗口 24 小时，扫描最多再失败一次；2 倍窗口之内还没收尾就是异常，不是延迟。
- 补回比例平时是多少？ → 1% 是估容量用的保守假设，真实值应该低得多；上线后用实际的做基线，我看趋势，不只看绝对值。
- 工单上的转账，钱怎么办？ → on_hold 一直冻着，不释放也不扣；对账查清是 completed 还是 failed，再走同一个状态变更。
**常见失分。**
- **只说「加监控」：** 没有指标、没有阈值、没有人。
- **扫描没有心跳：** 任务悄悄挂了，所有人以为兜底在跑。
- **按笔数告警：** 平均值掩盖了某一笔卡了三天。
