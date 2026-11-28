---
id: hi-sdx-tail-amplification
node: sd.core-concepts.numbers-to-know.more
type: qa
step: 2
---
## Q
**扇出与多跳放大尾延迟**｜补充 · 必须知道的数字 · 追问

一个页面并行调用 100 个后端，每个后端 p99 为 200 ms（1% 的调用更慢）。页面延迟会怎样？如果是串行的 10 跳微服务、同机房往返只有 0.5 ms，延迟预算又该怎么看？

## A
**结论。** 扇出会把后端的尾部变成用户看到的常态：100 个并行调用时，约 63% 的页面至少碰上一个慢调用。串行链路同理，网络往返不是问题，每一跳的尾部才是。

**要点。**
- **扇出的账：** 每个调用快的概率是 0.99，100 个全快是 0.99¹⁰⁰ ≈ 37%，所以约 63% 的页面要等最慢的那个。后端的 p99 近似成了页面的中位数。
- **串行链路：** 10 跳都不慢的概率 0.99¹⁰ ≈ 90.4%，约 9.6% 的请求会带上一个慢跳。要让链路 p99 达标，每跳要做到 p99.9（1 − 0.999¹⁰ ≈ 1%）。
- **往返很便宜：** 10 跳同机房往返 10 × 0.5 = 5 ms，相对一次 200 ms 的慢调用微不足道。真正贵的是碰磁盘（约 10 ms）和跨地域（约 100 ms）的跳。
- **对策：** 减少扇出和层数；每个调用设超时并接受部分结果；请求对冲；给最慢的依赖加缓存。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 210">
<text x="8" y="18" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每个调用 1% 概率变慢时，</text>
<text x="8" y="34" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一次请求至少碰上一个慢调用的概率</text>
<rect x="24" y="178" width="50" height="2" rx="3" stroke-width="1" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="49" y="172" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1.0%</text>
<text x="49" y="196" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1 个</text>
<rect x="102" y="169.484" width="50" height="10.516" rx="3" stroke-width="1" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="127" y="163.484" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9.6%</text>
<text x="127" y="196" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10 个</text>
<rect x="180" y="110.26" width="50" height="69.74" rx="3" stroke-width="1" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="205" y="104.26" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">63.4%</text>
<text x="205" y="196" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">100 个</text>
<rect x="258" y="70.0044" width="50" height="109.996" rx="3" stroke-width="1" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="283" y="64.0044" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">≈100%</text>
<text x="283" y="196" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1000 个</text>
<line x1="16" y1="180" x2="324" y2="180" stroke-width="1.2" stroke="currentColor"/>
</svg>

**面试里这样说。** 「扇出 100 的话，单个后端的 p99 会变成页面约 63% 的体验，所以我不看平均值，而是对每一跳的 p99.9 提要求，同时减少扇出、对慢调用做超时和部分结果。」

**易错。**
- **把平均往返加起来当预算：** 5 ms 的往返看起来没事，漏掉了尾部的叠加。
- **只优化中位数：** 高扇出系统的体验由尾部决定。
