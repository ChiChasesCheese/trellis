---
id: hi-mock-notification-07-dive-provider
node: fix.notification-mock
type: qa
step: 7
---
## Q
**通知系统 · 第 7 步 · 深入二：供应商慢了或挂了**｜模拟面试

面试官：「苹果的推送服务正在返回错误。你的 worker 怎么办？怎么避免它拖住邮件、短信和回执？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先给原则：** 「供应商慢或挂，不能让别的渠道和回执等它。我做三件事：隔离、有节制地重试、止血。」
- **隔离：** 「日志的主题按（优先级，供应商）切：tx 与 bulk 各四个，一共八个，每个有自己的 worker 池。苹果挂了，只堵 tx.apns 和 bulk.apns，邮件和短信照常流。如果所有渠道共用一个主题，苹果的失败消息会堵在后面所有消息前面。」
- **哪些错才重试：** 「超时、5xx、429 重试，429 要遵守 Retry-After。参数错和令牌失效（例如苹果返回设备令牌已失效）不重试：直接标记失败，并通知令牌管理去清理。」
- **退避加抖动：** 「失败的消息带着尝试次数转进重试主题，第 n 次等待 random(0, 30 秒 × 2^n)，这叫 full jitter，最多 5 次，最长一次等待上限 16 分钟。不加抖动，一次故障后所有消息会在同一秒一起重试，把刚恢复的供应商又打垮。」
- **死信：** 「5 次都失败进死信队列（DLQ），状态记 failed。DLQ 不是垃圾桶：回执的 DLQ 深度大于 0 就告警，保留 14 天，修好之后可以回放。」
- **熔断：** 「光重试不够：苹果整个挂了，每次调用都要等 3 秒超时，40,000 次/秒 × 3 秒 = 12 万个请求在飞，worker 的线程全被耗光。每个供应商一个熔断器：10 秒内至少 100 次调用、失败率超过 50% 就打开，30 秒内不再调用，消息直接进重试主题，不消耗尝试次数；30 秒后半开，放 10 个探测，至少 8 个成功就关闭。」
- **限流器仍然在：** 「限流保护供应商不被我们打爆，熔断保护我们不被它拖垮，两者不是一回事。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 168">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">隔离：每个（优先级，供应商）一个主题</text>
<rect x="8" y="26" width="76.5" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="46.25" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">tx</text>
<text x="46.25" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">apns</text>
<rect x="90.5" y="26" width="76.5" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="128.75" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">tx</text>
<text x="128.75" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">fcm</text>
<rect x="173" y="26" width="76.5" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="211.25" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">tx</text>
<text x="211.25" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">email</text>
<rect x="255.5" y="26" width="76.5" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="293.75" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">tx</text>
<text x="293.75" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">sms</text>
<rect x="8" y="76" width="76.5" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="46.25" y="94.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">bulk</text>
<text x="46.25" y="109.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">apns</text>
<rect x="90.5" y="76" width="76.5" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="128.75" y="94.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">bulk</text>
<text x="128.75" y="109.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">fcm</text>
<rect x="173" y="76" width="76.5" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="211.25" y="94.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">bulk</text>
<text x="211.25" y="109.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">email</text>
<rect x="255.5" y="76" width="76.5" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="293.75" y="94.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">bulk</text>
<text x="293.75" y="109.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">sms</text>
<text x="8" y="146" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">苹果挂了：只堵左边一列，邮件和短信照常流动</text>
<text x="8" y="162" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每个主题有自己的 worker 池和自己的积压</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 194">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">重试：full jitter，5 次</text>
<rect x="8" y="26" width="324" height="89" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">第 n 次等待 = random(0, 30 秒 × 2^n)</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">n=1　0–60 秒</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">n=2　0–2 分钟　n=3　0–4 分钟</text>
<text x="18" y="89.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">n=4　0–8 分钟　n=5　0–16 分钟</text>
<text x="18" y="104.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">5 次都失败：进死信队列（DLQ）</text>
<rect x="8" y="123" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">只重试临时错误</text>
<text x="18" y="156.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">超时 · 5xx · 429（遵守 Retry-After）</text>
<text x="18" y="171.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">令牌失效（如 APNs 410）不重试，标记失败</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 134">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">熔断器：每个供应商一个</text>
<rect x="8" y="26" width="102.67" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="59.33" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">关闭</text>
<text x="59.33" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">正常调用</text>
<rect x="118.67" y="26" width="102.67" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">打开</text>
<text x="170" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">30 秒不调用</text>
<rect x="229.33" y="26" width="102.67" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="280.67" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">半开</text>
<text x="280.67" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">放 10 个探测</text>
<text x="8" y="96" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">打开条件：10 秒内 ≥ 100 次且失败率 &gt; 50%</text>
<text x="8" y="112" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">半开：≥ 8 个成功就关闭，否则再打开 30 秒</text>
<text x="8" y="128" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">没有熔断：40,000/秒 × 3 秒超时 = 12 万个在飞</text>
</svg>
白板上新增：八个主题，重试的等待表，和熔断器的三个状态。
**为什么这样说。** （约 4 分钟，累计第 27 分钟。）面试官看你是不是把「供应商会坏」当作常态来设计：隔离、重试有上限、死信有人看、熔断止血。他当时先说「从数据库里把 pending 的捞出来重发」，后来才说到重试主题和死信，但一直没回答邮件和短信怎么不被苹果拖住。强的回答第一句话就说隔离。
**面试官可能接着问。**
- 重试期间要不要写状态库？ → 不要。重试消息自带尝试次数和下次时间，状态库只在终态写：sent 或 failed，写得少，就不会变成热点。
- 回执重试 5 次最长要等多久？ → 最多约 16 分钟，一张支付回执晚 16 分钟仍有价值。活动的消息带 expires_at，过期就丢，不再发。
- 苹果挂了，回执怎么办？ → 熔断打开后，回执可以改走邮件：偏好允许的话，由 worker 换渠道重新入队。
- 重试主题怎么实现延迟？ → Kafka 没有延迟投递：按延迟分层的重试主题，消费者等到 not_before 才处理；或者用带延迟的队列。我选分层主题，不引入新组件。
**常见失分。**
- **把 pending 从库里扫出来重发：** 他当时这样答，隔离不了渠道，库也被拖着。
- **只有限流，没有熔断：** 供应商全挂时，线程被超时耗光。
- **重试没有上限，也没有抖动：** 故障恢复的那一刻，同步重试的消息把供应商再次打垮。
- **失败的永远在重试：** 毒消息要进死信，否则堵住后面的消息。
