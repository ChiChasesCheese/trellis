---
id: bagu-rate-limit-algorithms-1-four-algorithms
node: a.protect.rate-limit-algorithms
type: qa
step: 1
---
## Q
**限流算法 · 固定窗口、滑动窗口、漏桶、令牌桶各是什么**｜必会

面试官：「你们的开放接口要给第三方商户限流。常见的限流算法有哪几种，各自特点是什么？」

## A
**基本回答。** 固定窗口：每窗口一个计数器，超阈值拒绝，最简单但边界突刺。滑动窗口：切小格统计最近一段，更平滑、内存更多。漏桶（Nginx `limit_req`）：请求以恒定速率流出，输出永远匀速，突发只能排队，桶满就拒。令牌桶（Guava `RateLimiter`，支持预热）：按固定速率放令牌，拿到才通过，限制平均速率加突发上限；速率 r 是长期平均，容量 b 是突发量，r=1000、b=200 表示平均每秒 1000、瞬时多放 200。被限流返回 HTTP 429 并带 `Retry-After`。限流维度全局、接口、用户、调用方要分开配，避免一个大客户占满配额。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 220">
<rect x="8" y="8" width="156" height="76" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86" y="35" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">固定窗口</text>
<text x="86" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">每窗口一个计数器</text>
<text x="86" y="65" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">最简单，边界会突刺</text>
<rect x="176" y="8" width="156" height="76" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="254" y="35" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">滑动窗口</text>
<text x="254" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">切小格，统计最近一段</text>
<text x="254" y="65" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">更平滑，内存更多</text>
<rect x="8" y="92" width="156" height="76" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86" y="119" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">漏桶</text>
<text x="86" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">请求以恒定速率流出</text>
<text x="86" y="149" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">突发排队，桶满就拒</text>
<rect x="176" y="92" width="156" height="76" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="254" y="119" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">令牌桶</text>
<text x="254" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">匀速放令牌，拿到才过</text>
<text x="254" y="149" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">允许突发</text>
<text x="8" y="188" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">令牌桶：速率 r = 长期平均，容量 b = 突发上限</text>
<text x="8" y="208" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">r=1000、b=200：平均每秒 1000，瞬时多放 200</text>
</svg>
令牌桶用蓝色标出，因为多数场景选它；图下方是它的两个参数。
**业务场景。** 令牌桶 r = 2/秒、b = 4、初始满：t=0 来 6 个，前 4 个通过，后 2 个 429；t=1 补了 2 个，来 3 个通过 2 个。商户开放接口按商户 ID 各配一个桶，允许开票时刻的短时突发，某商户脚本狂刷只触发它自己的 429。对比「每 10 秒最多 20 个」的固定窗口：第 9 秒来 20 个、第 11 秒又来 20 个都通过，两秒内放了 40 个。
**容易错。**
- **把令牌桶和漏桶混为一谈：** 漏桶限输出速率，令牌桶限平均速率并允许突发。
- **以为令牌桶能无限突发：** 最多 b 个。
- **只配一个全局限额。**
