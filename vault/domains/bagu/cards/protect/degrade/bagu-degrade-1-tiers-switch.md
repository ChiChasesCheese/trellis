---
id: bagu-degrade-1-tiers-switch
node: b.protect.degrade
type: qa
step: 1
---
## Q
**降级 · 降什么、怎么触发、和熔断限流的区别**｜追问

面试官：「大促时系统扛不住了，你会主动关掉哪些功能？怎么保证关得住、恢复得稳？」

## A
**基本回答。** 降级（degradation）是资源紧张或依赖故障时，主动关闭或简化次要功能保核心路径。要提前分级，临时判断来不及：P0 下单、支付最后才碰；P1 商品详情、搜索；P2 推荐、评价、浏览历史、积分展示先降。手段：读降级（推荐挂了返回静态热门列表、按时间排序）、写降级（评论点赞改异步写队列）、功能开关、兜底数据（缓存旧值、默认头像）、数据库故障切只读。触发：手动开关放配置中心，按功能粒度独立、秒级生效，配置中心不可用时用本地缓存值，预案提前演练；或自动（熔断、负载、错误率）。恢复要逐步放量（10%、50%、全量），降级期间要有监控告警，防长期无声降级。熔断是技术上自动快速失败，熔断后的 fallback 就是一种降级；降级是业务决策，限流控制进来多少，三者常组合。
**2026 亮点。** 分级可做进过载保护本身：服务内按请求重要度分档（关键、降级、尽力、批量），按并发或 CPU、延迟水位越高越先丢低档，比另起非核心集群便宜；从自动扩缩容的目标 CPU 才开始丢，不挡住扩容信号。被丢的请求要可快速失败、可重试，并配退避防重试风暴。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<text x="8" y="16" text-anchor="acc" font-size="12" font-family="sans-serif" fill="currentColor">先给功能分级，从最下面一级开始降</text>
<rect x="8" y="26" width="324" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="170" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">P2：推荐、评价、浏览历史、积分展示</text>
<text x="170" y="57.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">先降</text>
<rect x="8" y="76" width="324" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="92.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">P1：商品详情、搜索</text>
<text x="170" y="107.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">资源紧再降</text>
<rect x="8" y="126" width="324" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="142.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">P0：下单、支付</text>
<text x="170" y="157.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">最后才碰，要保住</text>
<text x="8" y="192" text-anchor="dim" font-size="12" font-family="sans-serif" fill="currentColor">触发：手动开关（配置中心）或自动（熔断、负载、错误率）</text>
<text x="8" y="210" text-anchor="dim" font-size="12" font-family="sans-serif" fill="currentColor">手段：读降级、写降级、功能开关、只读模式</text>
<text x="8" y="228" text-anchor="dim" font-size="12" font-family="sans-serif" fill="currentColor">恢复：逐步放量，不要一下全开</text>
<text x="8" y="244" text-anchor="dim" font-size="12" font-family="sans-serif" fill="currentColor">降级期间要有监控告警</text>
</svg>
金字塔按重要性分三级，压力来了从上往下降，下单支付在最底层最后才动。
**业务场景。** 大促推荐依赖错误率超阈值，降级开关自动打开，首页推荐位返回提前缓存的热门列表；评论发布改写队列，用户看到「已提交」；仍紧张再手动关积分展示、浏览历史；压力降下来后推荐先放 10% 再放大。
**容易错。**
- **没提前分级、开关没演练过。**
- **以为降级就是熔断。**
- **降级后不管了、恢复时全量放开。**
