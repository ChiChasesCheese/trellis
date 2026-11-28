---
id: bagu-breaker-1-three-states
node: b.protect.breaker
type: qa
step: 1
---
## Q
**熔断器 · 三态怎么转换、阈值怎么设**｜必会

面试官：「支付渠道连续超时，你怎么让系统不再傻等？熔断器的状态怎么转换？」

## A
**基本回答。** 三态：Closed 正常放行并在滑动窗口（如最近 100 个）内统计，达到最小样本量（如 20）且失败率 ≥ 50%（或慢调用比例）转 Open；Open 所有调用立即失败走 fallback，等一段时间（如 30 秒，太短会探测过频）转 Half-Open；Half-Open 放少量请求（如 5 个）探测，全成功回 Closed，有失败回 Open。样本量要够：3 个请求挂 2 个失败率 67% 不能说明下游坏了。超时和 5xx 算失败，4xx 是调用方的问题不算。fallback 返回缓存、默认值或友好错误，不要再调另一个不稳定服务。熔断是对下游的快速失败，由下游失败率触发；限流是对上游的拒绝，由进来的流量触发。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 270">
<rect x="8" y="30" width="100" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58" y="46.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Closed</text>
<text x="58" y="61.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">正常调用</text>
<rect x="232" y="30" width="100" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="282" y="46.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Open</text>
<text x="282" y="61.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">立即失败</text>
<rect x="120" y="150" width="100" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="166.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Half-Open</text>
<text x="170" y="181.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">放少量探测</text>
<line x1="108" y1="50" x2="225" y2="50" stroke-width="1.2" stroke="currentColor"/>
<polygon points="232.0,50.0 225.0,53.2 225.0,46.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">失败率超阈值</text>
<text x="170" y="66" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">（样本够）</text>
<line x1="255" y1="70" x2="217.193" y2="143.77" stroke-width="1.2" stroke="currentColor"/>
<polygon points="214.0,150.0 214.3,142.3 220.0,145.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="250" y="118" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">等 30 秒</text>
<line x1="126" y1="150" x2="64.4547" y2="75.3996" stroke-width="1.2" stroke="currentColor"/>
<polygon points="60.0,70.0 66.9,73.4 62.0,77.4" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="118" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">探测全成功</text>
<line x1="220" y1="175" x2="312" y2="175" stroke-width="1.2" stroke="currentColor"/>
<line x1="312" y1="175" x2="312" y2="77" stroke-width="1.2" stroke="currentColor"/>
<polygon points="312.0,70.0 315.2,77.0 308.8,77.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="240" y="194" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">有失败回 Open</text>
<text x="8" y="216" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Closed：滑动窗口（如最近 100 个）统计</text>
<text x="8" y="232" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">最小样本量 20、失败率 ≥ 50% 转 Open</text>
<text x="8" y="248" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Open 期间所有调用走 fallback</text>
<text x="8" y="264" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Half-Open 放 5 个探测请求</text>
</svg>
四条箭头是全部转换：失败率超阈值进 Open，等够时间进 Half-Open，探测全成功回 Closed，有失败回 Open。
**工具。** Resilience4j（默认窗口 100、阈值 50%、Open 等 60 秒、半开 10 个）；Sentinel（慢调用比例、异常比例、异常数三种策略；Hystrix 已停止维护）；Envoy / Istio 的 outlier detection 剔除异常实例。
**业务场景。** 支付渠道 A，窗口 100、最小样本 20、阈值 50%：前 10 个挂 8 个失败率 80% 但样本不足不熔断；凑到 20 个挂 11 个（55%）转 Open，请求立即失败并切备用渠道，30 秒内 A 一个请求都不发；到时放 5 个探测，全成功回 Closed，有 1 个失败立刻回 Open 再等 30 秒。
**容易错。**
- **只看失败次数不看样本。**
- **把 4xx 也算失败。**
- **fallback 里再调别的不稳定服务：** 把故障转移到别处。
