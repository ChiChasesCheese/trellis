---
id: bagu-time-wait-close-wait-5-ss-troubleshoot
node: a.net.time-wait-close-wait
type: qa
step: 5
---
## Q
**TIME_WAIT 与 CLOSE_WAIT · 线上怎么用 ss 区分排查，谁主动关闭**｜追问

面试官：「机器上连接状态很乱。你怎么快速判断是 TIME_WAIT 多、CLOSE_WAIT 多，还是别的问题？」

## A
**基本回答。** 先按状态数量：`ss -ant | awk 'NR>1{print $1}' | sort | uniq -c`，或 `ss -s` 看概览。状态指向责任方：谁出现 TIME_WAIT 谁是主动关闭方，对策是复用连接；谁出现 CLOSE_WAIT 谁是没 close 的被动方，用 `ss -antp state close-wait` 看进程和对端，对策是改代码，对端集中在同一个下游就是对它的调用没关闭；SYN-RECV 多可能是 SYN 洪泛或队列太小；监听端口用 `ss -lnt` 看 Recv-Q 与 Send-Q 判断全连接队列是否被打满。`ss` 直接读内核套接字信息，连接多时比老的 `netstat` 快得多，还能按状态过滤并显示进程。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 240">
<rect x="8" y="6" width="324" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="21.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ss -ant 统计各状态数量</text>
<text x="170.0" y="36.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">（或 ss -s 看概览）</text>
<rect x="8" y="84" width="102" height="62" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="59.0" y="104.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">TIME_WAIT 多</text>
<text x="59.0" y="119.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">本机主动关</text>
<text x="59.0" y="134.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">→ 复用连接</text>
<line x1="170" y1="44" x2="59" y2="84" stroke-width="1.2" stroke="currentColor"/>
<polygon points="59.0,84.0 64.5,78.6 66.7,84.6" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="119" y="84" width="102" height="62" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="104.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">CLOSE_WAIT 多</text>
<text x="170.0" y="119.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">应用没 close</text>
<text x="170.0" y="134.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">→ 改代码</text>
<line x1="170" y1="44" x2="170" y2="84" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,84.0 166.8,77.0 173.2,77.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="230" y="84" width="102" height="62" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="281.0" y="104.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SYN-RECV 多</text>
<text x="281.0" y="119.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SYN 洪泛或</text>
<text x="281.0" y="134.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">队列太小</text>
<line x1="170" y1="44" x2="281" y2="84" stroke-width="1.2" stroke="currentColor"/>
<polygon points="281.0,84.0 273.3,84.6 275.5,78.6" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="172" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">CLOSE_WAIT：ss -antp state close-wait</text>
<text x="8" y="190" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">监听端口：ss -lnt 看 Recv-Q、Send-Q</text>
<text x="8" y="212" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">对端集中在同一个下游 → 调它的代码没关闭</text>
<text x="8" y="230" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">谁有 TIME_WAIT，谁是主动关闭方</text>
</svg>
先统计各状态，再按哪个多分三条路。
**业务场景。** 某服务描述符使用率告警，`ss -ant` 里三万个连接全是 CLOSE_WAIT，`ss -antp state close-wait` 显示都指向同一个下游地址，直接定位到调用它的代码漏了关闭。长期把各状态数量和描述符使用率做成趋势告警，看趋势不看绝对值：服务端几万个 TIME_WAIT 可能正常，CLOSE_WAIT 持续上涨才是泄漏。
**容易错。**
- **以为连接状态乱就是机器坏了。**
- **只看总连接数：** 要按状态拆开。
- **以为两种状态处理方式一样。**
