---
id: bagu-rate-limit-algorithms-5-sentinel
node: a.protect.rate-limit-algorithms
type: qa
step: 6
---
## Q
**限流实现 · Sentinel 里限流是怎么实现的**｜追问

面试官：「你们用 Sentinel 做限流。一个请求进来，Sentinel 怎么统计、怎么判断要不要拦？规则里能选什么？」

## A
**基本回答。** Sentinel 为每个资源用滑动窗口（LeapArray）统计 QPS 和线程数：默认 1 秒切 2 格，每次请求只更新当前格，开销小。请求经过处理链，统计后到流控环节对照规则，超限抛 `BlockException` 交给 fallback（返回 429 并带 `Retry-After`）。规则选指标（QPS 或并发线程数）和效果：直接拒绝、预热 warm up（冷系统逐步放量，缓存和连接池还空）、匀速排队（漏桶，排队超时才拒）。另有系统保护（load、平均响应时间、线程数、入口 QPS 兜底）、热点参数、按调用方或关联资源限流。单机规则只管单实例，集群总量靠集群流控：token server（内嵌或独立）统一统计，实例向它申请令牌，不可用时客户端退化为本地限流，不会因限流器故障全拒。规则通过配置中心动态推送，不用重启。与 Hystrix 比：Hystrix 已停止演进，靠线程池隔离和熔断；Sentinel 以流量为入口，有流控、熔断、系统自适应保护，信号量隔离更轻，带控制台。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 232">
<rect x="8" y="10" width="56" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="36" y="29" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">请求</text>
<line x1="64" y1="25" x2="79" y2="25" stroke-width="1.2" stroke="currentColor"/>
<polygon points="86.0,25.0 79.0,28.2 79.0,21.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="86" y="10" width="76" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="124" y="29" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">统计</text>
<line x1="162" y1="25" x2="177" y2="25" stroke-width="1.2" stroke="currentColor"/>
<polygon points="184.0,25.0 177.0,28.2 177.0,21.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="184" y="10" width="76" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="222" y="29" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">流控</text>
<line x1="260" y1="25" x2="275" y2="25" stroke-width="1.2" stroke="currentColor"/>
<polygon points="282.0,25.0 275.0,28.2 275.0,21.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="282" y="10" width="50" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="307" y="29" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">业务</text>
<line x1="222" y1="40" x2="222" y2="55" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="222.0,62.0 218.8,55.0 225.2,55.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="184" y="62" width="148" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="258" y="76.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">超限：抛出</text>
<text x="258" y="91.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">BlockException</text>
<text x="8" y="84" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">→ 交给 fallback 处理</text>
<text x="8" y="124" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">统计窗口 1 秒，切成 2 格</text>
<rect x="8" y="132" width="156" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86" y="151" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">格 0：0–500ms</text>
<rect x="176" y="132" width="156" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="254" y="151" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">格 1：500–1000ms</text>
<text x="8" y="182" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">每次请求只更新当前格，开销很小</text>
<text x="8" y="202" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">效果：直接拒绝 · 预热 · 匀速排队（漏桶）</text>
<text x="8" y="222" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">另有系统保护、热点参数、集群流控</text>
</svg>
请求经统计、流控，超限抛异常交给 fallback；中间是两格滑动窗口，下面是规则可选的效果。
**业务场景。** 调用方 appKey=X 配 QPS 100 直接拒绝：格 0 记 40、当前格 55，合计 95 通过，当前格变 56；合计到 100 后再来一个抛 `BlockException`；过 500ms 最老的格被清空复用，合计自动下降。下游变慢时另配一条线程数规则，先于整体超时把流量挡住。
**容易错。**
- **以为单机规则能限住整个集群。**
- **冷启动直接放满量。**
- **规则写死在代码里。**
