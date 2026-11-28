---
id: bagu-java-threadpool-5-dynamic-isolate
node: a.runtime.java-threadpool
type: qa
step: 5
---
## Q
**线程池 · 怎么动态调参和监控，慢调用要不要隔离**｜追问

面试官：「线上线程池参数不合适，不重启能改吗？你怎么发现线程池出问题？调用大模型这种很慢的接口怎么处理？」

## A
**基本回答。** `ThreadPoolExecutor` 有 `setCorePoolSize`、`setMaximumPoolSize` 等，运行期可调，参数由配置中心推送，事故时不用重启；调小核心数时多余线程在下次空闲时终止，调大且队列有任务时按需新建。队列容量没有 setter，要自定义可变容量的队列。监控活跃线程数、队列长度、完成数、拒绝次数、任务耗时；队列长期接近满、活跃线程数持续等于最大值、拒绝次数上升都是信号。慢调用放独立线程池加有界队列（舱壁隔离 bulkhead），池满时快速失败或提示排队，影响限定在自己的池里。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 282">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">共用一个池：慢任务占满，快任务干等</text>
<rect x="8" y="28" width="38" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="27.0" y="45.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">慢</text>
<rect x="52" y="28" width="38" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="71.0" y="45.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">慢</text>
<rect x="96" y="28" width="38" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="115.0" y="45.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">慢</text>
<text x="144" y="47" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">线程全被占</text>
<rect x="8" y="64" width="38" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="27.0" y="79.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">快</text>
<rect x="52" y="64" width="38" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="71.0" y="79.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">快</text>
<rect x="96" y="64" width="38" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="115.0" y="79.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">快</text>
<rect x="140" y="64" width="38" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="159.0" y="79.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">快</text>
<text x="190" y="80" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">← 在队列里等</text>
<line x1="8" y1="108" x2="332" y2="108" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="8" y="130" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">舱壁隔离：慢任务只占自己的池</text>
<rect x="8" y="142" width="154" height="66" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="85.0" y="163.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">大模型池</text>
<text x="85.0" y="178.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">有界队列、有超时</text>
<text x="85.0" y="193.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">池满提示「排队中」</text>
<rect x="178" y="142" width="154" height="66" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="255.0" y="163.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">普通池</text>
<text x="255.0" y="178.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">快任务照常处理</text>
<text x="255.0" y="193.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不受慢调用拖累</text>
<text x="8" y="232" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">动态调参：setCorePoolSize、</text>
<text x="8" y="250" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">setMaximumPoolSize，配置中心推送</text>
<text x="8" y="272" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">监控：活跃线程、队列长度、拒绝次数</text>
</svg>
上半是共用一个池的坏结果：慢任务把线程全占了，快任务干等；下半是舱壁隔离后各管各的；最下面是调参和监控。
**举个例子。** 聊天里调用大模型，平均几十秒，和普通请求共用池后线程全被占住，普通接口也在队列里等。监控显示活跃线程持续等于最大值、队列近满、拒绝上升；拆出独立池，配有界队列和超时，池满直接提示「排队中」，普通请求恢复；事故中配置中心推送新的最大线程数，`setMaximumPoolSize` 即时生效。
**容易错。**
- **父任务在池里同步等子任务，共用同一个有界池：** 线程全被父任务占住，子任务拿不到线程，死锁。
- **以为 get 超时任务就停了：** `Future.get(timeout)` 只是不再等待，任务还在跑；`cancel(true)` 只发中断，不响应中断的调用不会停。
