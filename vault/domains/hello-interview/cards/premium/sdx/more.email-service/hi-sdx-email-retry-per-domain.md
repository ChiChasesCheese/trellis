---
id: hi-sdx-email-retry-per-domain
node: more.email-service
type: qa
step: 5
---
## Q
**出站重试按目的域分队**｜补充 · 邮件服务（Gmail） · 追问

面试官：「出站邮件投递失败后进重试队列。你只用一个全局先进先出队列，某个目的域名限流了会怎样？每天发 45 亿封、2% 延迟进重试、平均停留 6 小时，这个重试状态有多大？」

## A
**结论。** 全局队列会让一个慢域名拖住排在它后面的所有域名，所以重试要按目的域名分队，各自带退避状态。重试状态稳态约 2250 万条，必须放持久化、带索引的存储。

**要点。**
- **队头阻塞：** 全局先进先出时，限流域名的邮件反复失败又排回，后面发往健康域名的邮件跟着延迟。
- **按目的域分队：** 每个域名有独立的下次重试时间、退避间隔和并发上限，一个域名故障只影响它自己。
- **不是百万个真队列：** 实现上是以 (目的域, 下次重试时间) 为键的持久化表，调度器按到期时间跨域名轮转取任务。
- **Little 定律：** 2% × 4.5×10^9 = 9×10^7/天 ≈ 1042/秒，乘 21600 秒停留，稳态约 2.25×10^7 条。
- **所以要持久化：** 单机内存放不下，重启也不能丢；一封信在被接受时已经承诺了投递。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<text x="10" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">全局 FIFO：slow.com 限流，后面全被拖住</text>
<rect x="10" y="26" width="74" height="30" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="47.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">slow.com</text>
<rect x="92" y="26" width="74" height="30" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="129.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">slow.com</text>
<rect x="174" y="26" width="74" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="211.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a.com</text>
<rect x="256" y="26" width="74" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="293.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b.com</text>
<text x="10" y="82" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">按目的域分队：各自退避，互不影响</text>
<rect x="10" y="92" width="92" height="30" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="56.0" y="111.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">slow.com</text>
<rect x="110" y="92" width="220" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="220.0" y="111.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">退避 1h → 2h → 4h，限并发</text>
<rect x="10" y="130" width="92" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="56.0" y="149.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a.com</text>
<rect x="110" y="130" width="220" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="220.0" y="149.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">下次重试 5 分钟后</text>
<rect x="10" y="168" width="92" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="56.0" y="187.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b.com</text>
<rect x="110" y="168" width="220" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="220.0" y="187.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">下次重试 20 分钟后</text>
<text x="10" y="226" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">重试状态：9×10^7/天 ≈ 1042/秒 × 6 小时</text>
<text x="10" y="244" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">≈ 2250 万条常驻，需持久化带索引的存储</text>
</svg>

**为什么。** 队列深度等于到达速率乘停留时间。重试的停留时间是小时级，积压必然大，隔离粒度就该落在会出问题的单位，也就是目的域。

**面试里这样说。** 「重试按目的域名分区，每个域有自己的退避和并发上限，调度器按下次重试时间取任务。规模上，每天 9 千万条进重试，约 1042 条每秒，停留 6 小时就是 2250 万条常驻，所以放持久化的索引表，不放内存队列。」

**易错。**
- **全局先进先出：** 一个限流域名拖慢所有投递，延迟集中在无辜的收件域。
- **所有域名同一个退避：** 对健康域名等太久，对故障域名又重试太猛，可能被对方进一步限流。
- **重试状态放内存：** 节点重启就丢信，违反已接受即承诺投递。
