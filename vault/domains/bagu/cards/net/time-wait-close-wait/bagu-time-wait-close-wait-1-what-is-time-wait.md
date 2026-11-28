---
id: bagu-time-wait-close-wait-1-what-is-time-wait
node: a.net.time-wait-close-wait
type: qa
step: 1
---
## Q
**TIME_WAIT · 哪一方进入，它是什么**｜必会

面试官：「连接关闭后，哪一方会进入 TIME_WAIT？它是什么状态？为什么服务器上经常能看到很多？」

## A
**基本回答。** 主动关闭（先发 FIN）的一方，发出最后一个 ACK 后进入 TIME_WAIT，等 2×MSL 才关闭，Linux 固定 60 秒；被动方停在 CLOSE_WAIT，不进 TIME_WAIT。每个 TIME_WAIT 占一个四元组，是正常现象，不是故障。谁先发 FIN 就堆在谁那：HTTP/1.0 或 `Connection: close` 时堆在服务端，只吃内存，几万个影响很小；客户端不断新建短连接再主动关，堆在客户端，吃的是端口，才是大问题。`tcp_fin_timeout` 管的是 FIN_WAIT_2，不是 TIME_WAIT。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 296">
<text x="78" y="14" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">主动方（先发 FIN）</text>
<text x="262" y="14" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">被动方</text>
<rect x="8" y="24" width="140" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="78.0" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">FIN_WAIT_1</text>
<text x="78.0" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">发出 FIN</text>
<rect x="192" y="24" width="140" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="262.0" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">CLOSE_WAIT</text>
<text x="262.0" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">收到 FIN，回 ACK</text>
<line x1="148" y1="36" x2="192" y2="36" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="192.0,36.0 185.0,39.2 185.0,32.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="192" y1="52" x2="148" y2="52" stroke-width="1.2" stroke="currentColor"/>
<polygon points="148.0,52.0 155.0,48.8 155.0,55.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="84" width="140" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="78.0" y="100.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">FIN_WAIT_2</text>
<text x="78.0" y="115.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">收到 ACK，等 FIN</text>
<rect x="192" y="84" width="140" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="262.0" y="100.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">仍是 CLOSE_WAIT</text>
<text x="262.0" y="115.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">等应用 close()</text>
<rect x="192" y="144" width="140" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="262.0" y="160.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">LAST_ACK</text>
<text x="262.0" y="175.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">应用关闭，发 FIN</text>
<rect x="8" y="144" width="140" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="78.0" y="160.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">TIME_WAIT</text>
<text x="78.0" y="175.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">回最后一个 ACK</text>
<line x1="192" y1="156" x2="148" y2="156" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="148.0,156.0 155.0,152.8 155.0,159.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="148" y1="172" x2="192" y2="172" stroke-width="1.2" stroke="currentColor"/>
<polygon points="192.0,172.0 185.0,175.2 185.0,168.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="204" width="140" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="78.0" y="220.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">CLOSED</text>
<text x="78.0" y="235.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">等 2×MSL（60 秒）后</text>
<rect x="192" y="204" width="140" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="262.0" y="220.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">CLOSED</text>
<text x="262.0" y="235.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">收到 ACK 就关闭</text>
<line x1="78" y1="64" x2="78" y2="84" stroke-width="1.2" stroke="currentColor"/>
<polygon points="78.0,84.0 74.8,77.0 81.2,77.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="78" y1="124" x2="78" y2="144" stroke-width="1.2" stroke="currentColor"/>
<polygon points="78.0,144.0 74.8,137.0 81.2,137.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="78" y1="184" x2="78" y2="204" stroke-width="1.2" stroke="currentColor"/>
<polygon points="78.0,204.0 74.8,197.0 81.2,197.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="262" y1="64" x2="262" y2="84" stroke-width="1.2" stroke="currentColor"/>
<polygon points="262.0,84.0 258.8,77.0 265.2,77.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="262" y1="124" x2="262" y2="144" stroke-width="1.2" stroke="currentColor"/>
<polygon points="262.0,144.0 258.8,137.0 265.2,137.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="262" y1="184" x2="262" y2="204" stroke-width="1.2" stroke="currentColor"/>
<polygon points="262.0,204.0 258.8,197.0 265.2,197.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="266" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">TIME_WAIT 只出现在主动方</text>
<text x="8" y="284" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">被动方是 CLOSE_WAIT，不进 TIME_WAIT</text>
</svg>
左列主动方，右列被动方，自上而下是时间：被动方停在 CLOSE_WAIT 等应用关闭，主动方最后进 TIME_WAIT，等够时间才 CLOSED。
**业务场景。** 爬虫每爬一页就新建连接、读完主动关，每个连接占四元组 60 秒，本机堆积数万个 TIME_WAIT；同一站点复用连接后降到几十个。
**容易错。**
- **以为被动方也进 TIME_WAIT。**
- **以为 TIME_WAIT 多就是故障：** 真正的问题是客户端端口耗尽。
- **以为 tcp_fin_timeout 能调短 TIME_WAIT。**
