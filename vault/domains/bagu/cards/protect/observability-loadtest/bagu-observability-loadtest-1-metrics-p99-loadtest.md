---
id: bagu-observability-loadtest-1-metrics-p99-loadtest
node: b.protect.observability-loadtest
type: qa
step: 1
---
## Q
**可观测性与压测 · 指标怎么设计、为什么看 P99、压测怎么隔离**｜追问

面试官：「给直播互动服务设计监控体系，采哪些指标？告警为什么看 P99 不看平均？上线前怎么做全链路压测？」

## A
**基本回答。** 三根支柱：Metrics（数值，告警和趋势）、Logs（事件现场）、Traces（一次请求跨服务的路径，Trace ID 128 位串起多个 Span，Span 有 64 位 ID 和父 ID，靠 W3C `traceparent` 头传递）。指标四类：QPS、错误率、延迟分位数、饱和度（CPU、线程池、队列）；类型 Counter、Gauge、Histogram。告警看 P99：平均数被大量快请求稀释，看不见用户抱怨的长尾。分位数不能跨实例平均，要合并各实例的直方图桶再读。全链路压测隔离：压测账号、影子表或影子库，标记随链路透传，监控要含 MQ 堆积、慢 SQL、GC、线程池，限流熔断先生效，每轮记录并发、QPS、P90 / P99、错误率；容量要用压测找拐点验证，不靠公式。
**2026 亮点。** Prometheus 原生直方图（Native Histogram）已稳定：稀疏指数桶、不必手配边界，各实例直方图可直接合并再算分位数；要显式开启采集（`scrape_native_histograms`）并走 protobuf，OpenMetrics 文本格式暂不支持，桶数要设上限防膨胀。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 232">
<text x="8" y="16" text-anchor="acc" font-size="12" font-family="sans-serif" fill="currentColor">1000 个请求，快的 ≤100ms，慢的 2s</text>
<text x="121" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">≤100ms</text>
<text x="212" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2s</text>
<text x="332" y="46" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">P99</text>
<text x="8" y="76" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">实例 A</text>
<rect x="76" y="56" width="90" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="121" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">900</text>
<rect x="170" y="56" width="84" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="212" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="332" y="76" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">100ms</text>
<text x="8" y="112" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">实例 B</text>
<rect x="76" y="92" width="90" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="121" y="110" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">95</text>
<rect x="170" y="92" width="84" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="212" y="110" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<text x="332" y="112" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2000ms</text>
<rect x="76" y="130" width="90" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="121" y="148" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">995</text>
<rect x="170" y="130" width="84" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="212" y="148" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<text x="8" y="150" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">合并桶</text>
<text x="332" y="150" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">≈100ms</text>
<text x="8" y="182" text-anchor="dim" font-size="12" font-family="sans-serif" fill="currentColor">995 ÷ 1000 = 99.5% ≥ 99%，P99 落在 ≤100ms 桶</text>
<text x="8" y="200" text-anchor="acc" font-size="12" font-family="sans-serif" fill="currentColor">两个 P99 取平均得 1050ms，完全不对</text>
<text x="8" y="220" text-anchor="dim" font-size="12" font-family="sans-serif" fill="currentColor">要合并桶，不是平均分位数</text>
</svg>
实例 A 的 900 个都 ≤100ms，P99 为 100ms；实例 B 的 100 个里有 5 个 2 秒，P99 为 2000ms。两个 P99 平均得 1050ms 是错的：合并桶后 995 个 ≤100ms，占 99.5% ≥ 99%，整体 P99 落在 100ms 桶。
**业务场景。** 直播互动服务做全链路压测，打赏请求带压测标记写进影子表，不污染真实账务。
**容易错。**
- **用平均延迟做告警。**
- **把各实例 P99 取平均。**
- **压测打到真实库，或压测前限流熔断没开。**
