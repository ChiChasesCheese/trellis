---
id: bagu-time-wait-close-wait-3-too-many
node: a.net.time-wait-close-wait
type: qa
step: 3
---
## Q
**TIME_WAIT · 太多有什么危害，怎么优化，tw_reuse 有什么风险**｜必会

面试官：「线上调用下游，TIME_WAIT 到了几万个，开始报 Cannot assign requested address。怎么办？tcp_tw_reuse 能随便开吗？」

## A
**基本回答。** 危害在客户端：每个出站连接占一个临时端口，端口用完报 `Cannot assign requested address`。默认范围 32768 到 60999 共 28232 个，每个 TIME_WAIT 占 60 秒，所以对同一目标 IP 和端口每秒最多约 470 个新连接（28232 ÷ 60）。根因是短连接太多，调参数只让它撑得久一点。优先级：① 复用连接（keep-alive、连接池，治本）；② `tcp_tw_reuse`：只对出站，靠时间戳判断新连接时间戳更大才复用，要双方开时间戳，对端不支持或经某些 NAT 可能出问题（取值 0 关、1 全局、2 仅回环，较新内核默认 2）；③ 扩大端口范围或增加目标地址。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 232">
<rect x="8" y="6" width="324" height="48" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="26.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">临时端口 32768–60999，共 28232 个</text>
<text x="170.0" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">每个 TIME_WAIT 占 60 秒 → 每秒约 470 个</text>
<rect x="8" y="66" width="324" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="86.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① 复用连接：keep-alive、连接池（治本）</text>
<rect x="8" y="106" width="324" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="126.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② tcp_tw_reuse：只对出站，靠时间戳</text>
<rect x="8" y="146" width="324" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="166.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ 扩大端口范围，或增加目标地址</text>
<line x1="170" y1="98" x2="170" y2="106" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,106.0 166.8,99.0 173.2,99.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="170" y1="138" x2="170" y2="146" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,146.0 166.8,139.0 173.2,139.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="202" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">tcp_tw_recycle：别用，NAT 后丢包，4.12 已删</text>
<text x="8" y="222" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">SO_LINGER 超时 0 强行 RST：会丢未发数据</text>
</svg>
先算账：28232 个端口各占 60 秒；下面三个办法优先级递减，最后两行不要用。`tcp_tw_recycle` 在 NAT 后多个客户端时间戳不单调，SYN 被当旧包丢弃，Linux 4.12 已删；`SO_LINGER` 超时 0 强行 RST，会丢未发数据。
**业务场景。** 支付网关每次调银行接口都新建短连接，高峰期每秒几百个，TIME_WAIT 堆到几万，端口耗尽；改用 HTTP 连接池后降到几百个，扣款成功率恢复。改不了代码时才对出站开 `tcp_tw_reuse` 并扩端口范围。连接池大小还要不超过渠道允许的连接数。
**容易错。**
- **把 470 当每 60 秒的总数：** 是每秒；每 60 秒共约 28232 个。
- **以为 tcp_tw_reuse 没风险。**
- **让客户端主动关：** TIME_WAIT 应落在代价小的服务端一侧。
