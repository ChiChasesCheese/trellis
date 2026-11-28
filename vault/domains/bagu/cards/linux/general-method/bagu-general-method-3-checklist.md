---
id: bagu-general-method-3-checklist
node: a.linux.general-method
type: qa
step: 3
---
## Q
**服务突然变慢 · 完整排查清单**｜必会

面试官：「线上服务突然变慢，给我一个完整的排查清单。」

## A
**基本回答。** 由外到内六步：范围 → 变更 → 依赖 → 机器资源 → 应用内部 → 保护动作。开口先说「我先看范围和最近的变更」，再说命令，这比一上来报命令更像有经验的人。
各步看什么：范围（接口、机房、实例、用户）；变更（最近 30 分钟的发布、配置、扩缩容）；依赖（慢查询、缓存命中率、下游、消息积压）；机器资源（CPU、IO、内存与 GC、网络、fd）；应用内部（线程池、连接池、Full GC、锁竞争，`jstack` 看是否大量线程卡在同一调用点的 BLOCKED / WAITING）；保护动作（限流、降级、扩容、熔断）。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 284">
<rect x="4" y="4" width="100" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="54" y="22" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1 范围</text>
<text x="110" y="22" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">接口·机房·实例·用户</text>
<rect x="4" y="42" width="100" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="54" y="60" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2 变更</text>
<text x="110" y="60" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">最近 30 分钟，有就回滚</text>
<line x1="54" y1="33" x2="54" y2="41" stroke-width="1.2" stroke="currentColor"/>
<polygon points="54.0,41.0 50.8,34.0 57.2,34.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="4" y="80" width="100" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="54" y="98" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3 依赖</text>
<text x="110" y="98" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">慢查询·命中率·下游·积压</text>
<line x1="54" y1="71" x2="54" y2="79" stroke-width="1.2" stroke="currentColor"/>
<polygon points="54.0,79.0 50.8,72.0 57.2,72.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="4" y="118" width="100" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="54" y="136" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4 机器资源</text>
<text x="110" y="136" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">CPU·IO·内存 GC·网络·fd</text>
<line x1="54" y1="109" x2="54" y2="117" stroke-width="1.2" stroke="currentColor"/>
<polygon points="54.0,117.0 50.8,110.0 57.2,110.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="4" y="156" width="100" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="54" y="174" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5 应用内部</text>
<text x="110" y="174" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">线程池·连接池·Full GC·锁</text>
<line x1="54" y1="147" x2="54" y2="155" stroke-width="1.2" stroke="currentColor"/>
<polygon points="54.0,155.0 50.8,148.0 57.2,148.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="4" y="194" width="100" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="54" y="212" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6 保护动作</text>
<text x="110" y="212" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">限流·降级·扩容·熔断</text>
<line x1="54" y1="185" x2="54" y2="193" stroke-width="1.2" stroke="currentColor"/>
<polygon points="54.0,193.0 50.8,186.0 57.2,186.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="4" y="240" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">越往下越要登录机器，成本越高，放后面</text>
</svg>
六步从上到下，成本由低到高。高亮的前两步最便宜，也最可能一击命中，所以答题时先说它们。
**举个例子。** 用户反馈视频发布成功，但很久才出现在主页：
1. **范围：** 只有「发布后的处理链路」慢，浏览和点赞正常，说明问题局限在这条链路。
2. **变更：** 最近 30 分钟没有发布和配置变更，排除。
3. **依赖：** 看调用链和队列指标，发现处理视频的消息队列大量积压。
4. **定位到消费端：** 积压是因为消费端处理变慢，生产端正常。
5. **保护动作：** 临时扩容消费者，加快消化积压。
6. **继续找根因：** 消费端为什么变慢，再看它的资源和应用内部。
**容易错。**
- **一上来报命令：** 先说范围和变更，再说命令，更像有经验的人。
- **忽略变更：** 大多数事故和变更有关，不看变更就直接查机器，很可能白忙。
- **顺序反了：** 先登机器查线程栈，而依赖那一步一眼就能看出的问题却没看。
- **忘了保护动作：** 排查期间用户还在受损，需要限流、降级、扩容先保住核心链路。
