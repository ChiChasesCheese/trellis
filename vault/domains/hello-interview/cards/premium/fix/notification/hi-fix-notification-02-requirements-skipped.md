---
id: hi-fix-notification-02-requirements-skipped
node: fix.notification
type: qa
step: 2
---
## Q
**通知系统 · 开场该问什么**｜复盘

面试官：「设计一个通知系统，覆盖 push、邮件和短信。你可以先问我任何需求问题，边问边在白板上画。」

你会怎么回答？

## A
**当时的回答。** 先复述题目（01:14，面试官说「you're restating the problem」）；面试官问「scale or delivery guarantees」，只问了每天多少用户、多少条（02:30）；整场没问交付保证、退订、延迟，最后反馈里都被点名。

**应该这样说。**
- **先确认五件事再画图：** 流量种类、交付保证、每类延迟、退订和偏好、渠道和保留期。Senior 的开场是在收窄题目，不是复述，也不是只问规模。
- **流量种类：** 交易类（回执、验证码）单条、要快；营销类一次千万条、可以慢。
- **交付保证：** 到供应商是至少一次（at-least-once），靠去重键让用户最多看到一条；恰好一次到手机供应商不给保证，不承诺。没有「不丢」，就说不清为什么 200 要放在持久化之后。
- **延迟，每类一个数：** 回执接受后 5 秒内交给供应商；营销 1,000,000 条 30 分钟发完，10,000,000 ÷ 1,800 秒 ≈ 5,600 条/秒，远低于 83,000 条/秒的尖峰，所以活动可以限速。没有「回执 5 秒」，就说不清为什么要拆优先级。
- **退订和偏好：** 这是合规，不是加分项；营销要查偏好（渠道、类别、静默时间），短信回 STOP 必须生效，回执不受影响。检查两处：扇出时先过滤，发送前再查一次，因为偏好会变。
- **写下假设：** 1 亿月活、日均 5 亿条、尖峰 500 万条/分钟，状态保留 90 天。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 204">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">4 退订和偏好　5 渠道、保留期</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">4 退订与偏好</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">营销必须能退订；短信回 STOP 生效</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">回执、验证码不能被营销退订挡住</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">5 渠道与保留</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">push、邮件、短信，各有供应商限速</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">状态保留 90 天，更久归档</text>
<text x="8" y="182" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">问完马上写下假设再画图</text>
<text x="8" y="198" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">10,000,000 ÷ 1,800 秒/30 分钟 ≈ 5,600 条/秒</text>
</svg>
白板上：五行需求，每行一个数或一个决定；右边留空，设计画在右边。

**常见失分。**
- **复述题目：** 面试官已经知道题目。
- **只问规模：** 规模只决定要不要分片，决定不了保证和检查点。
- **问了不落地：** 问出「要不要退订」，设计里却没有偏好这一步。

**面试官可能接着问。**
- 回执可以丢吗？ → 不可以，200 要等消息写进持久日志后才返回；营销我也按不丢设计，成本相同。
- 用户在收到前退订了？ → 发送前再查一次偏好；已发出的收不回，所以静默检查靠近发送，不靠近扇出。
