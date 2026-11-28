---
id: bagu-spike-10x-1-first-response
node: a.protect.spike-10x
type: qa
step: 1
---
## Q
**QPS 突增十倍 · 先怎么应对**｜必会

面试官：「线上 QPS 突然从 1 万涨到 10 万，你怎么办？」

## A
**基本回答。** 顺序：判断、保核心、削峰、扩容、复盘，先挡再扩，因为扩容有冷启动（拉镜像、启动、预热要几分钟，数据库这类有状态的更难扩），救不了秒级突发。先几分钟判断真假：真实用户、攻击、客户端重试风暴处理完全不同，看来源是否集中、接口是否只打一两个、独立用户数涨没涨，判断错了扩容是白花钱。入口（网关）按优先级限流，进房、下单多放，榜单、推荐少放，超出返回 429；读走缓存、写先进队列由消费者按数据库能承受的速度写，把尖峰压平；降级关掉次要功能，熔断慢下游，保护线程池和连接池。目标是优雅拒绝：撑得住 3 倍、拒绝其余 7 倍，好过硬吃 10 倍全部超时。事后压测找延迟陡增的拐点，生产容量取其约 70%，补预案。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="8" y="8" width="112" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="64.0" y="27.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1 判断真假</text>
<text x="132" y="28" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">几分钟内：看来源和用户数</text>
<line x1="64" y1="40" x2="64" y2="50" stroke-width="1.2" stroke="currentColor"/>
<polygon points="64.0,50.0 67.2,43.0 60.8,43.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="50" width="112" height="32" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="64.0" y="69.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2 入口限流</text>
<text x="132" y="70" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">保核心，超出的返回 429</text>
<line x1="64" y1="82" x2="64" y2="92" stroke-width="1.2" stroke="currentColor"/>
<polygon points="64.0,92.0 67.2,85.0 60.8,85.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="92" width="112" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="64.0" y="111.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3 缓存加队列</text>
<text x="132" y="112" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">读走缓存，写先进队列</text>
<line x1="64" y1="124" x2="64" y2="134" stroke-width="1.2" stroke="currentColor"/>
<polygon points="64.0,134.0 67.2,127.0 60.8,127.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="134" width="112" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="64.0" y="153.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4 再扩容</text>
<text x="132" y="154" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">容器起来要几分钟</text>
<line x1="64" y1="166" x2="64" y2="176" stroke-width="1.2" stroke="currentColor"/>
<polygon points="64.0,176.0 67.2,169.0 60.8,169.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="176" width="112" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="64.0" y="195.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5 事后复盘</text>
<text x="132" y="196" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">压测找拐点，补预案</text>
<text x="8" y="238" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">先挡再扩：挡是秒级，扩是分钟级</text>
<text x="8" y="256" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">宁可优雅拒绝 7 倍，也别全部超时</text>
</svg>
五步有先后：前三步是秒到分钟级，扩容要等容器起来所以靠后；高亮的第二步是核心。
**业务场景。** 直播间被推上热搜，进房请求从 1 万涨到 10 万 QPS（假设稳定上限约 3 万）：独立用户数也涨约十倍、来源分散，是真实流量；网关只放行约 3 万、其余 7 万返回 429 或排队，进房和发弹幕优先；关掉榜单实时刷新、推荐位返回默认内容；弹幕写队列再批量落库，房间信息读缓存；同时发出扩容，几分钟后新实例就绪，这几分钟靠前面几步顶住。
**容易错。**
- **以为先扩容就行：** 应用层扩大只是把压力推给数据库和下游。
- **以为要把十倍全处理掉。**
- **不先判断真假：** 对攻击扩容等于出钱帮它。
- **只罗列手段不讲顺序。**
