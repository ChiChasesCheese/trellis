---
id: bagu-epoll-io-models-2-select-poll
node: a.net.epoll-io-models
type: qa
step: 2
---
## Q
**select 与 poll · 它们的问题在哪**｜必会

面试官：「select 和 poll 都能监听多个连接，为什么说它们撑不住高并发？」

## A
**基本回答。** 根因是内核无状态：不记得你关心哪些 fd，每次调用都整包传入、整包检查。`select` 用固定大小位图 `fd_set`，上限 `FD_SETSIZE` = 1024（编译期常量，不能靠配置调大），每次把集合从用户态拷进内核，内核线性检查 O(n)，返回后用户态还要再扫一遍找出就绪的；调用后集合被改写成只剩就绪的，下轮必须重新设置。`poll` 改用 `pollfd` 数组，去掉上限和重置，但每次仍传全部 fd、仍线性扫描。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 246">
<text x="4" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">用户态：12 个连接，只有 2 个有数据</text>
<rect x="26" y="22" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="50" y="22" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="74" y="22" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="98" y="22" width="24" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="122" y="22" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="146" y="22" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="170" y="22" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="194" y="22" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="218" y="22" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="242" y="22" width="24" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="266" y="22" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="290" y="22" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="170" y1="48" x2="170" y2="80" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,80.0 166.8,73.0 173.2,73.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="176" y="68" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">① 整包拷进内核</text>
<text x="4" y="96" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">内核：</text>
<rect x="26" y="104" width="24" height="24" rx="3" fill="none" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<rect x="50" y="104" width="24" height="24" rx="3" fill="none" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<rect x="74" y="104" width="24" height="24" rx="3" fill="none" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<rect x="98" y="104" width="24" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="122" y="104" width="24" height="24" rx="3" fill="none" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<rect x="146" y="104" width="24" height="24" rx="3" fill="none" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<rect x="170" y="104" width="24" height="24" rx="3" fill="none" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<rect x="194" y="104" width="24" height="24" rx="3" fill="none" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<rect x="218" y="104" width="24" height="24" rx="3" fill="none" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<rect x="242" y="104" width="24" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="266" y="104" width="24" height="24" rx="3" fill="none" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<rect x="290" y="104" width="24" height="24" rx="3" fill="none" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<line x1="30" y1="140" x2="310" y2="140" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="310.0,140.0 303.0,143.2 303.0,136.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="158" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">② 逐个检查，O(n)</text>
<text x="4" y="184" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">③ 返回后，用户态再扫一遍找出就绪的</text>
<text x="4" y="206" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每次调用都重来：内核不记得你关心谁</text>
<text x="4" y="228" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">代价跟总连接数成正比，不是就绪数</text>
</svg>
12 个连接只有 2 个有数据，但每次调用都整包拷进去、整排检查、整排再找一遍：代价跟总连接数成正比，不是就绪数。
**业务场景。** 推送网关 10000 个连接，某一刻只有 20 个有数据：每轮拷贝 10000 项、内核查 10000 个、进程再扫 10000 个才挑出 20 个；连接涨到 10 万，每轮工作量涨 10 倍，有数据的仍是 20 个。连接只有几十个或大多活跃时，select/poll 的简单和跨平台反而更合适。
**容易错。**
- **以为 poll 比 select 本质更快：** 只去掉了数量上限，拷贝加线性扫描一样。
- **忘了 select 集合被改写：** 循环里不重设会漏监听。
