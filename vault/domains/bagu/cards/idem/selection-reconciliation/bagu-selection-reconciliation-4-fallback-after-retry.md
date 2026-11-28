---
id: bagu-selection-reconciliation-4-fallback-after-retry
node: a.idem.selection-reconciliation
type: qa
step: 4
---
## Q
**最终一致 · 补偿和重试都失败后的兜底是什么**｜追问

面试官：「消息重试了十次还失败，补偿动作也报错了，这笔业务卡在中间状态。你的系统怎么兜底？」

## A
**基本回答。** 分三层：重试有上限，超限进死信队列并告警；定时任务扫描长时间停在中间状态（PROCESSING、PENDING）的单据，主动向对方查询真实结果，再推进或回滚；仍无法判断的转人工工单。补偿动作本身必须幂等，才能放心反复执行。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="8" y="8" width="324" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① 重试有上限</text>
<text x="170" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">超限进死信队列，并告警</text>
<line x1="170" y1="48" x2="170" y2="57" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,64.0 166.8,57.0 173.2,57.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="64" width="324" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="80.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② 定时扫描卡在中间状态的单据</text>
<text x="170" y="95.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">PROCESSING / PENDING：主动向对方查结果</text>
<line x1="170" y1="104" x2="170" y2="113" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,120.0 166.8,113.0 173.2,113.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="120" width="324" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="136.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ 仍判断不了：转人工工单</text>
<text x="170" y="151.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">有工具：看事件序列、一键重放、追加调整记录</text>
<text x="8" y="188" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">补偿动作本身必须幂等，才能放心反复执行</text>
<text x="8" y="208" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">盯三个指标：中间状态单据数、补偿次数、</text>
<text x="8" y="226" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">对账差异率，任何一个突增都是前面出了问题</text>
<text x="8" y="252" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不要直接改库：靠工具重放、追加调整记录</text>
</svg>
三层兜底从上到下依次升级：先有限重试并告警，再主动查询真实状态，最后才是人工。底下是让它能反复执行的前提和要盯的指标。
**举个例子。** 扣款请求发给渠道后超时，订单一直是 PROCESSING：
1. **重试：** 按退避重试几次，仍拿不到结果，达到上限，消息进死信队列并告警。
2. **十分钟后扫描：** 定时任务扫到这张 PROCESSING 超过阈值的订单，向渠道查询这笔扣款的真实状态。
3. **渠道说已扣款：** 把订单推进为已支付，没有再次扣款。
4. **渠道说没扣：** 回滚订单（或允许重新发起），释放预占的资源。
5. **渠道也查不清：** 转人工工单，工具里能看到这笔订单的事件序列，一键重放或追加调整记录。
**容易错。**
- **无限重试：** 把一次故障放大成风暴，重试要有上限和退避。
- **只重试、不扫描：** 单据卡在 PROCESSING 没人推进，用户看到的是永远「处理中」。
- **人工直接改库：** 没有记录、不能追溯，应该用工具追加调整记录。
- **补偿不幂等：** 扫描、重放一多，就重复补偿。
