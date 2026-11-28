---
id: bagu-epoll-io-models-4-lt-et
node: a.net.epoll-io-models
type: qa
step: 4
---
## Q
**水平触发与边缘触发 · 区别和使用注意**｜必会

面试官：「epoll 的水平触发和边缘触发有什么区别？边缘触发要注意什么？」

## A
**基本回答。** 水平触发（LT，默认）：只要缓冲区还有数据可读，每次 `epoll_wait` 都通知，不易漏数据，编程简单。边缘触发（ET）：只在状态变化（新数据到达）时通知一次，没读完也不再提醒，系统调用更少，但「读干净」的责任转给程序：必须循环读到 `EAGAIN`，且 fd 必须非阻塞，否则最后一次读睡死，卡住整个事件循环。没有明确需求选 LT；Nginx 用 ET，Redis 用 LT。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 232">
<text x="4" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">对端写入 10 字节，应用只读了 4 个</text>
<text x="4" y="90" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">wait</text>
<rect x="20" y="22" width="30" height="24" rx="3" fill="none" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<rect x="50" y="22" width="30" height="24" rx="3" fill="none" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<rect x="80" y="22" width="30" height="24" rx="3" fill="none" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<rect x="110" y="22" width="30" height="24" rx="3" fill="none" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<rect x="140" y="22" width="30" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="170" y="22" width="30" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="200" y="22" width="30" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="230" y="22" width="30" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="260" y="22" width="30" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="290" y="22" width="30" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="80" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">已读 4</text>
<text x="230" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">缓冲区还剩 6</text>
<text x="114" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">第 1 次</text>
<text x="198" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">第 2 次</text>
<text x="282" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">第 3 次</text>
<text x="4" y="118" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">LT</text>
<text x="4" y="160" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ET</text>
<rect x="72" y="98" width="84" height="32" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="114" y="118" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">通知：可读</text>
<rect x="156" y="98" width="84" height="32" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="198" y="118" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">通知：可读</text>
<rect x="240" y="98" width="84" height="32" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="282" y="118" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">通知：可读</text>
<rect x="72" y="140" width="84" height="32" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="114" y="160" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">通知：可读</text>
<rect x="156" y="140" width="84" height="32" rx="3" fill="none" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="198" y="160" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不再通知</text>
<rect x="240" y="140" width="84" height="32" rx="3" fill="none" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="282" y="160" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不再通知</text>
<text x="4" y="198" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ET：剩下的 6 字节没人提醒，要自己读到 EAGAIN</text>
<text x="4" y="218" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">所以 fd 必须非阻塞，否则最后一次读会睡死</text>
</svg>
10 字节到达、应用只读了 4 个：之后三次 `epoll_wait`，LT 每次都再提醒，ET 只在第一次提醒，剩下 6 字节没人管。
**业务场景。** 网关用 ET 读弹幕，一次只读固定 4 KB 就返回，剩下的留在缓冲区，这条连接「卡住」，直到对端再发数据才恢复，表现为偶发的消息延迟。
**容易错。**
- **以为 ET 一定比 LT 快：** 只是少了重复通知，换来出错风险。
- **ET 下只读一次：** 剩下的数据被遗忘。
- **以为 LT 是定时通知：** 是只要有数据就每次返回，与时间无关。
