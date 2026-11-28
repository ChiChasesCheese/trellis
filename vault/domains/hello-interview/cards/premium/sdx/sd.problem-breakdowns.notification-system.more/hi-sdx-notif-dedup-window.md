---
id: hi-sdx-notif-dedup-window
node: sd.problem-breakdowns.notification-system.more
type: qa
step: 2
---
## Q
**去重记录要保留多久**｜补充 · 通知系统 · 追问

面试官：「通知系统用事件 ID 做去重记录。这条记录你保留多久？如果短信服务商会把消息在自己的队列里最多留 10 小时再重试或放弃，窗口怎么定？」

## A
**结论。** 去重窗口必须长于链路里所有可能重发同一条通知的环节的最长排队加重试时间，否则迟到的合法重试会被当成新通知再发一遍。服务商队列最长 10 小时，就至少留 11 小时，再按自己的死信回放时长取更大值。

**要点。**
- **窗口太短的后果：** 记录过期后，一次延迟很久才到的重试没有记录可查，被当作新通知发出，用户收到两条。
- **要比较哪些时间：** 服务商的最长排队时间、自己的重试和退避总时长、死信队列的回放时长，取最大的再加余量。
- **算例：** 10 小时加 1 小时余量，至少 11 小时；若死信回放按 48 小时设计，窗口取 48 小时以上。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 122" font-family="sans-serif" font-size="11">
<text x="20" y="16" fill="currentColor">服务商排队、重试：最长 10h</text>
<rect x="20" y="22" width="100" height="8" fill="currentColor" fill-opacity="0.3" stroke="currentColor"/>
<text x="20" y="46" fill="currentColor">最短去重窗口：10h + 1h 余量 = 11h</text>
<rect x="20" y="52" width="140" height="8" fill="currentColor" fill-opacity="0.3" stroke="currentColor"/>
<text x="20" y="76" fill="currentColor">死信回放按 48h 设计：窗口取 48h 以上</text>
<rect x="20" y="82" width="270" height="8" fill="currentColor" fill-opacity="0.3" stroke="currentColor"/>
<line x1="20" y1="100" x2="300" y2="100" stroke="currentColor"/>
<line x1="20" y1="96" x2="20" y2="104" stroke="currentColor"/>
<line x1="120" y1="96" x2="120" y2="104" stroke="currentColor"/>
<line x1="160" y1="96" x2="160" y2="104" stroke="currentColor"/>
<line x1="290" y1="96" x2="290" y2="104" stroke="currentColor"/>
<text x="225" y="104" text-anchor="middle" fill="currentColor">≈</text>
<text x="20" y="116" text-anchor="middle" fill="currentColor">0</text>
<text x="120" y="116" text-anchor="middle" fill="currentColor">10h</text>
<text x="160" y="116" text-anchor="middle" fill="currentColor">11h</text>
<text x="290" y="116" text-anchor="middle" fill="currentColor">48h</text>
</svg>

- **别无限留：** 记录越久占存储越多，到期自动清理，用 TTL 即可，不要手工清。
- **服务商的数字要查：** 最长排队时间随服务商和版本变化，写进配置并定期核对，不要写死在代码里。

**为什么。** 去重记录是为了挡住重复，重复能出现多久之后，就得有多长的记录。

**面试里这样说。** 「去重窗口要大于所有下游环节的最长重发间隔。短信服务商队列最长 10 小时，我留 11 小时起，如果死信回放按 48 小时设计就用 48 小时，并用 TTL 自动过期。」

**易错。**
- **随手设 1 小时：** 慢的重试会在记录过期后到达，产生重复短信。
- **只看自己的重试：** 忽略了服务商自己的队列和重试。
- **窗口当永久：** 存储无限增长，查询也越来越慢。
