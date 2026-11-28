---
id: bagu-general-method-2-locate-layer
node: a.linux.general-method
type: qa
step: 2
---
## Q
**定位层次 · 问题在接入、应用、依赖还是资源**｜必会

面试官：「怎么判断问题出在哪一层？」

## A
**基本回答。** 由外到内缩小：接入层（负载均衡、网关、CDN）、应用自身、依赖（数据库、缓存、下游服务、消息队列）、机器资源。手段是对比和追踪：对比各实例的指标，看是个别机器还是整体；用调用链（trace）看时间花在哪一段；看状态码和错误类型。
**一句话记住。** 定位层次像排查家里水管不出水：先看总阀门（接入层）、再看自家水龙头（应用）、再看是不是水厂（依赖）出问题，最后才看自己家水管（机器资源）；每一层有自己的信号，先排除外层，不在错的地方使劲。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 240">
<rect x="4" y="4" width="100" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="54" y="23" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">接入层</text>
<text x="110" y="23" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">LB·网关·CDN：看状态码</text>
<rect x="4" y="46" width="100" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="54" y="65" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">应用自身</text>
<text x="110" y="65" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">线程池·连接池是否打满</text>
<line x1="54" y1="35" x2="54" y2="45" stroke-width="1.2" stroke="currentColor"/>
<polygon points="54.0,45.0 50.8,38.0 57.2,38.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="4" y="88" width="100" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="54" y="107" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">依赖</text>
<text x="110" y="107" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">库·缓存·下游·MQ：看调用链</text>
<line x1="54" y1="77" x2="54" y2="87" stroke-width="1.2" stroke="currentColor"/>
<polygon points="54.0,87.0 50.8,80.0 57.2,80.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="4" y="130" width="100" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="54" y="149" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">机器资源</text>
<text x="110" y="149" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">CPU·内存·磁盘·网络</text>
<line x1="54" y1="119" x2="54" y2="129" stroke-width="1.2" stroke="currentColor"/>
<polygon points="54.0,129.0 50.8,122.0 57.2,122.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="4" y="176" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">由外到内缩小；先对比各实例：</text>
<text x="4" y="194" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">个别异常→摘除，整体慢→看共同依赖</text>
</svg>
四层从外到内，右边是每层最容易看到的信号。高亮的「依赖」是线上最常见的元凶，往往需要靠调用链才看得出来。
**讲明白。**
- **为什么要分层：** 每层有各自的特征信号，先排除外层再进内层，不会在错误的层上花时间。
- **接入层看状态码：** 502 多是网关连不上或收到无效的后端响应，504 是后端超时。
- **应用层看黄金指标：** 延迟、流量、错误、饱和度；线程池、连接池打满是应用层的饱和信号。
- **依赖层看调用链：** 数据库、缓存、下游服务、消息队列的问题，用调用链（trace）看时间花在哪一段，哪一段占大头就是它。
- **机器资源层看 CPU、内存、磁盘、网络：** 机器指标正常，说明不是本机资源的问题。
- **对比是核心手段：** 对比各实例的指标。个别实例异常，多半是机器资源或实例自身问题，直接摘除；全部实例一起慢，看共同依赖或最近变更。
- **对比不同下游：** 只有一个下游变慢，就是依赖问题，而不是本服务的问题。
- **确认依赖后的做法：** 该做超时、熔断、降级，加机器没用。
**举个例子。** 接口大量超时，但 CPU 和内存都正常：
1. **机器层：** CPU、内存、磁盘、网络都正常，排除本机资源。
2. **对比实例：** 所有实例一起超时，不是个别机器的问题。
3. **看调用链：** 一条典型请求 2 秒，其中 1.8 秒花在调用支付渠道（PSP）这一段。
4. **对比下游：** 渠道 A 正常，只有渠道 B 变慢，进一步确认是渠道 B 的问题。
5. **结论与动作：** 问题在依赖，不在本服务。对渠道 B 做超时、熔断和降级，加机器没用。
**容易错。**
- **一看到超时就扩容：** 如果时间花在下游，加本服务的机器只会增加对下游的压力。
- **把 502 和 504 混为一谈：** 502 是网关连不上后端或收到无效响应，504 是后端超时。方向不同。
- **只看自己的指标：** 机器指标正常不等于服务正常，要用调用链看时间花在哪一段。
- **不做对比：** 不对比实例，就分不清是个别机器还是整体问题。
**业务场景。** 接口大量超时但 CPU 和内存都正常：调用链显示时间全花在调用支付渠道（PSP）这一段，问题在依赖，不在本服务。此时该做超时、熔断和降级，加机器没用。
**系统设计。** [[links.payment-batch-processing|支付处理系统（授权冻结 + 每日批量结算）]]：被问「渠道变慢时怎么判断是自己的问题还是渠道的」，答看调用链里渠道调用的耗时占比，并对比各渠道，只有一个渠道变慢就是依赖问题。
**可能问法。**
- 接口超时但机器指标正常，怎么查？ → 机器指标正常说明不是本机资源问题，用调用链（trace）看时间花在哪一段，多半在某个依赖：数据库、缓存、下游服务或渠道。再看线程池、连接池是否打满，以及超时、错误率。确认是依赖后，该做超时、熔断、降级，加机器没用。
- 怎么区分是自己的问题还是下游的问题？ → 对比：看各实例是个别异常还是整体都慢；看调用链里对该下游的调用耗时占比；对比不同下游，只有一个下游变慢就是依赖问题。再看状态码：502 多是网关连不上后端，504 是后端超时。
- 个别实例慢，整体不慢，怎么处理？ → 多半是那台机器的资源或实例自身的问题：先把它从流量里摘除，保住整体服务，再登上去看 CPU、内存、磁盘、网络和进程状态找原因。
