---
id: bagu-payment-system-6-qps
node: a.scenario.payment-system
type: qa
step: 6
---
## Q
**容量估算 · 日交易额到 QPS 再到容量**｜必会

面试官：「假设日支付 500 万笔，QPS 大概多少？你怎么估容量？」

## A
**基本回答。** 日均 QPS：500 万笔 ÷ 86,400 秒 ≈ 58 笔/秒；流量集中在活动和整点，乘日均的 3 到 10 倍，活动取 10，约 580 笔/秒（也参考历史曲线）。利特尔法则：在途请求 = 到达速率 × 停留时间，580 × 0.5 秒（渠道响应）≈ 290 个调用同时在飞，留 1.5 到 2 倍冗余，线程按约 435 到 580 规划。法则只在未饱和的稳态成立，接近拐点响应时间非线性上升，所以纸面估算只是压测目标的起点。数据库连接池不能照搬，受数据库核数限制通常几十个；按渠道隔离线程池，设超时和限流，防一个慢渠道拖垮全部。写入放大：一笔支付约写 5 行（订单、支付单、两条分录、回调记录），580 × 5 ≈ 2,900 行/秒。QPS 与 TPS 不同，一次支付包含下单、查询、回调多个请求。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<rect x="8" y="8" width="156" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86.0" y="26.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">日支付 500 万笔</text>
<rect x="8" y="54" width="156" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86.0" y="72.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">日均 ≈ 58 笔/秒</text>
<rect x="8" y="100" width="156" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86.0" y="118.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">峰值 ≈ 580 笔/秒</text>
<rect x="8" y="146" width="156" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86.0" y="164.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">在途 ≈ 290 个调用</text>
<rect x="8" y="192" width="156" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="86.0" y="210.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">线程 / 连接 435~580</text>
<line x1="86" y1="36" x2="86.0" y2="48.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="86.0,54.0 83.0,48.0 89.0,48.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="98" y="49" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">÷ 86,400 秒</text>
<line x1="86" y1="82" x2="86.0" y2="94.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="86.0,100.0 83.0,94.0 89.0,94.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="98" y="95" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">× 峰值倍数 10</text>
<line x1="86" y1="128" x2="86.0" y2="140.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="86.0,146.0 83.0,140.0 89.0,140.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="98" y="141" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">× 渠道响应 0.5 秒</text>
<line x1="86" y1="174" x2="86.0" y2="186.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="86.0,192.0 83.0,186.0 89.0,186.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="98" y="187" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">× 冗余 1.5~2</text>
<rect x="176" y="100" width="160" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="256.0" y="118.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">写放大 ≈ 2,900 行/秒</text>
</svg>
从日交易量一路乘除到线程数；最右的灰框是顺手估出的写入放大。
**举个例子。** 直播开场一分钟充值涌入，峰值 580 笔/秒：渠道 0.5 秒时 290 个在飞，线程池 435 到 580 够用；渠道变慢到 3 秒则需 580 × 3 = 1,740 个在飞，线程池很快耗尽，排队时间叠加进响应时间，连别的渠道请求也被堵在池外；对策是每次调用设超时、限流，按渠道隔离线程池，慢渠道只拖垮自己那份。
**容易错。**
- **用均值估峰值：** 按 58 笔/秒配资源，活动一来就被打穿。
- **连接池开到线程数那么大：** 开 500 个只会压垮数据库。
