---
id: bagu-rate-limit-algorithms-4-qps-vs-concurrency
node: a.protect.rate-limit-algorithms
type: qa
step: 4
---
## Q
**限流对象 · 限 QPS 还是限并发，利特尔定律怎么用**｜必会

面试官：「判题服务每个任务要跑几秒，机器同时只能跑 50 个。你是按 QPS 限流还是按并发限流？依据是什么？」

## A
**基本回答。** 保护线程池、连接池、沙箱槽位这类资源时限并发，因为耗尽的是并发而不是每秒请求数。利特尔定律：并发 = QPS × 平均延迟，三个量知道两个就能算第三个；并发上限固定 200，延迟 100ms 撑 2000 QPS，涨到 400ms 自动降到 500。下游变慢时同样 QPS 对应的并发成倍增长，到上限后放行的 QPS 自动下降，不用人调参。QPS 限流管配额和公平，并发限流管自保，两者配合。自适应并发限制借鉴 TCP 拥塞控制（AIMD）：延迟低加一点上限，超时减半（Netflix concurrency-limits）；Sentinel 规则可选 QPS 或并发线程数。排队也要设上限。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">并发 = QPS × 平均延迟（利特尔定律）</text>
<text x="8" y="52" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">延迟 100ms</text>
<rect x="100" y="36" width="224" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="212" y="53" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">QPS 上限 2000</text>
<text x="8" y="90" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">延迟 400ms</text>
<rect x="100" y="74" width="56" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="128" y="91" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">500</text>
<text x="8" y="124" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">并发上限固定 200：QPS 上限 = 200 ÷ 延迟</text>
<text x="8" y="148" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">判题：50 个沙箱槽位，每个任务 10 秒</text>
<text x="8" y="168" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">QPS = 50 ÷ 10 = 5，变慢了会自动少放</text>
</svg>
并发上限固定时，延迟越高能撑的 QPS 越低，限并发让放行速度自己跟着下游快慢走。
**业务场景。** 判题沙箱同时最多跑 50 个任务，平时每个 10 秒，QPS 上限 50 ÷ 10 = 5。比赛开始涌入 100 个提交，只限 QPS 到 5 看起来没问题，但任务因机器忙变慢到 20 秒，每秒放 5 个会堆出 5 × 20 = 100 个并发，沙箱早就爆了；限并发 50 则放行速度自动降到 50 ÷ 20 = 2.5 个/秒，多出来的排队或返回「判题繁忙」。
**容易错。**
- **只限 QPS 保护线程池。**
- **把并发上限写死不管延迟。**
