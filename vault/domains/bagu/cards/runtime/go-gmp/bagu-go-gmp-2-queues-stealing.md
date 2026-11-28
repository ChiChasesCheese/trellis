---
id: bagu-go-gmp-2-queues-stealing
node: a.runtime.go-gmp
type: qa
step: 2
---
## Q
**Go 调度 · 本地队列、全局队列和工作窃取怎么配合**｜必会

面试官：「一个 M 要找下一个 G 来运行，它去哪里找？本地队列空了怎么办？」

## A
**基本回答。** M 找下一个 G 的顺序：先取绑定 P 的本地队列（最多 256 个，几乎无锁、缓存友好）；每调度 61 次看一次全局队列（要加锁，所以只定期查，防止里面的 G 饿死；本地空时也会去取）；都空就查网络轮询器（netpoller，管理等网络事件的 G）；还没有就从别的 P 的本地队列偷走一半（work stealing）。只偷一半：让被偷的 P 还留有活，又偷到足够多以减少再次窃取。本地队列满了把一半挪到全局队列；新建的 goroutine 优先放当前 P 的 `runnext`，父子靠得近，缓存命中更好。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 296">
<rect x="8" y="8" width="210" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="113.0" y="27.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① 本地队列（最多 256 个）</text>
<rect x="8" y="56" width="210" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="113.0" y="75.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② 全局队列（要加锁）</text>
<line x1="113" y1="38" x2="113" y2="56" stroke-width="1.2" stroke="currentColor"/>
<polygon points="113.0,56.0 109.8,49.0 116.2,49.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="122" y="51" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">空了</text>
<rect x="8" y="104" width="210" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="113.0" y="123.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ 网络轮询器 netpoller</text>
<line x1="113" y1="86" x2="113" y2="104" stroke-width="1.2" stroke="currentColor"/>
<polygon points="113.0,104.0 109.8,97.0 116.2,97.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="122" y="99" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">空了</text>
<rect x="8" y="152" width="210" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="113.0" y="171.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">④ 偷别的 P 的一半</text>
<line x1="113" y1="134" x2="113" y2="152" stroke-width="1.2" stroke="currentColor"/>
<polygon points="113.0,152.0 109.8,145.0 116.2,145.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="122" y="147" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">空了</text>
<rect x="228" y="8" width="104" height="60" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="280.0" y="27.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">每调度 61</text>
<text x="280.0" y="42.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">次先看一眼</text>
<text x="280.0" y="57.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">全局队列</text>
<line x1="228" y1="62" x2="218" y2="62" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="218.0,62.0 225.0,58.8 225.0,65.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="8" y="214" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">窃取：P0 空了，从 P1 偷走一半</text>
<rect x="8" y="224" width="130" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="73.0" y="242.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">P1：G G G G</text>
<rect x="202" y="224" width="130" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="267.0" y="242.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">P0：（空）</text>
<line x1="138" y1="238" x2="202" y2="238" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="202.0,238.0 195.0,241.2 195.0,234.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="8" y="262" width="130" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="73.0" y="280.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">P1：G G</text>
<rect x="202" y="262" width="130" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="267.0" y="280.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">P0：G G</text>
<text x="170" y="280" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">偷完后</text>
</svg>
左边从上到下是 M 找活的顺序，每一步「空了」才往下走；右上角是插进来的 61 次规则；下面演示窃取：P0 空了，从 P1 偷走一半。
**业务场景。** 任务执行器收到一批任务，goroutine 先全进 P1 的本地队列（假设 8 个）；P0 本地、全局、netpoller 都空，偷走 4 个，其他空闲 P 也来偷，十几个核很快都忙起来，不用手写负载均衡。窃取只在单机内把任务摊到各核，机器之间还要靠任务分发层。
**容易错。**
- **以为全局队列优先：** 先本地，全局每 61 次才查一次。
- **以为窃取只偷一个，或需要中央调度器：** 偷一半，各 P 自己去偷。
