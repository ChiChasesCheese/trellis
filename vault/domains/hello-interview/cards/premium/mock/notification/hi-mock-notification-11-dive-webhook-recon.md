---
id: hi-mock-notification-11-dive-webhook-recon
node: fix.notification-mock
type: qa
step: 11
---
## Q
**通知系统 · 第 11 步 · 深入六：供应商回调与对账**｜模拟面试

面试官：「供应商是怎么告诉你消息送达了没有的？如果它的回调丢了，你怎么发现？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **结论：** 回调（webhook）是常态路径，更新送达状态；它会丢、重复、乱序，所以另有对账任务兜底。回调说明送达结果，不是扇出进度（那看分块表）。
- **入口，和 202 同一条规则：** 验签，原始事件追加进 provider-events 日志，立刻回 200，不在请求里处理；消费者随后处理，`(provider, event_id)` 唯一，重复的忽略。入口不直接写库：回调峰值与消息速率同量级（最高 83k/秒），直接写会打满状态库。
- **状态只往前走：** `UPDATE notification SET status='delivered' WHERE notification_id=$1 AND status='sent'`，0 行就是已终态或乱序，忽略；晚到的 sent 不会把 delivered 改回去。
- **渠道差异：** 邮件有送达、退回、投诉；短信有送达报告；推送只有「供应商已接受」，终态就是 sent，不承诺送达，只处理令牌失效错误。
- **对账规则：** 每 10 分钟每分片取 `status='sent'` 且 sent_at 早于 1 小时的邮件和短信（刚发出的回调多半还在路上），每次最多 1,000 行，调供应商查询接口，用同一条只向前的更新写回；部分索引 `(status, sent_at) WHERE status IN ('queued','sent')` 只含未完成的行，很小。
- **量级：** 假设回调丢 0.1%：5 亿 × 0.1% = 50 万条/天 ≈ 5.8 次/秒，远小于供应商额度；对账再限制在额度的 5% 内。
- **另一类缝隙：** status 停在 queued 超过 5 分钟（进了库没发出）重新入队；24 小时仍无终态的记 unknown 并计入告警。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 298">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">对账：选择、频率、上限、告警</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">选择</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">status='sent' 且 sent_at &lt; 现在 − 1 小时</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">queued 超过 5 分钟：重新入队</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">量级（假设丢 0.1%）</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">5 亿条/天 × 0.1% = 50 万条/天</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">÷ 86,400 秒 ≈ 5.8 次/秒</text>
<rect x="8" y="160" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">上限</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">查询不超过供应商额度的 5%</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每个分片每次取 1,000 行</text>
<rect x="8" y="227" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="245.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">告警</text>
<text x="18" y="260.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">最老 sent 超过 24 小时：状态记 unknown</text>
<text x="18" y="275.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">unknown 比例与 DLQ 深度上看板</text>
</svg>
白板上新增：回调到状态库的一条线，对账任务，和一条只向前的更新语句。

**常见失分。**
- **用回调回答进度：** 回调不说明扇出做到哪。
- **只有「定时扫一下」：** 没有选择规则、频率、上限、告警。
- **回调入口里直接写库或调别的服务：** 供应商超时重发，入口越慢越重复。
- **允许状态倒退：** 晚到的 sent 把 delivered 改回去。

**面试官可能接着问。**
- 回调可以伪造吗？ → 验签并查时间戳；更保险是只当提示、取出 id 后回查供应商，代价多一次调用，所以默认验签后直接应用，对账兜底。
