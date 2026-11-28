---
id: hi-sdx-cdn-dynamic-accel
node: sd.core-concepts.caching.more
type: qa
step: 8
---
## Q
**不能缓存的接口放 CDN**｜补充 · 缓存 · 加分

你的 API 响应完全个性化，不能缓存。同事问：「那放 CDN 还有什么意思？」怎么回答？

## A
**结论。** 不缓存也有收益：用户在近处的边缘完成握手，边缘再通过长连接和骨干网转给源站，冷连接的首个请求能快一半以上；同时边缘能挡掉恶意流量。

**要点。**
- **近处完成握手：** 假设用户到边缘 RTT 20 ms、到源站 150 ms。冷连接首个请求要 TCP 1 个、TLS 1.3 1 个、请求 1 个往返：直连 3×150 = 450 ms；经边缘，用户这一段 3×20 = 60 ms。
- **边缘到源站是热连接：** 边缘与源站保持长连接池，不再握手，只剩一次 150 ms，合计 210 ms。
- **骨干网路由：** 边缘到源站走提供商自己的网络，通常比公网中转更稳、丢包更少。
- **边缘挡流量：** WAF、机器人过滤、DDoS 吸收，都在流量到达你的基础设施之前完成。
- **源站连接数少：** 源站看到的是少量边缘连接，而不是海量用户连接。

**为什么。** 跨洲延迟的主因是往返次数。把多次往返放到短路径上，只把一次必须的长距离往返留在已建好的连接上。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 222">
<text x="8" y="18" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">冷连接上的首个请求（往返 RTT）</text>
<text x="20" y="44" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">直连源站，RTT 150 ms</text>
<rect x="20" y="52" width="98" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="69" y="70" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">TCP 150</text>
<rect x="120" y="52" width="98" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="169" y="70" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">TLS 150</text>
<rect x="220" y="52" width="98" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="269" y="70" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">请求 150</text>
<text x="320" y="100" text-anchor="end" font-size="12" font-family="sans-serif" fill="currentColor">450 ms</text>
<text x="20" y="126" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">经边缘，用户到边缘 RTT 20 ms</text>
<rect x="20" y="134" width="38" height="28" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="39" y="152" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">60</text>
<rect x="60" y="134" width="98" height="28" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="109" y="152" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">边缘→源站 150</text>
<text x="168" y="178" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">210 ms</text>
<text x="20" y="196" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">60 = 3 个往返 × 20 ms；边缘与源站的</text>
<text x="20" y="212" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">长连接早已建好，不再握手</text>
</svg>

**面试里这样说。** 「个性化接口我也会走 CDN 做动态加速，不是为了缓存：冷连接首个请求从 450 ms 降到 210 ms，因为握手在 20 ms 外的边缘完成，边缘到源站是已建好的长连接。」

**易错。**
- **以为总是更快：** 用户若已有长连接，直连只要 150 ms，经边缘反而是 20 + 150 = 170 ms。收益主要在首个请求和弱网。
- **忘了边缘到源站这一跳：** 150 ms 的跨洲往返依然存在，CDN 不会让它消失。
