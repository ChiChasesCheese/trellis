---
id: tr-test-infra-sharding-limits
node: test-infra.sharding
type: qa
step: 4
---
## Q
测试套件串行要 120 分钟。分成 4 片能到 30 分钟吗？分成 40 片能到 3 分钟吗？哪些因素限制了分片的收益？

## A
**每个分片的实际时长 = 固定开销 + 分到的测试耗时**，总时长取最慢的那个分片。

例：每片固定开销 4 分钟（拉代码、装依赖、启动服务），测试总耗时 120 分钟，最长的单条测试 6 分钟。
- **4 片**：4 + 120 ÷ 4 = 34 分钟。
- **10 片**：4 + 12 = 16 分钟。
- **40 片**：4 + 3 = 7 分钟，但最长那条测试单独就要 6 分钟，最慢的分片至少 4 + 6 = 10 分钟。
- **机器成本**：40 片总共消耗 40 × 4 = 160 分钟的固定开销，比测试本身还多。

最慢分片的时长：

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 180">
<g font-family="sans-serif" font-size="12">
<text x="10" y="29" fill="currentColor">4 片</text>
<rect x="50" y="14" width="24" height="22" fill="currentColor" fill-opacity="0.45" stroke="currentColor" stroke-width="0.8"/>
<rect x="74" y="14" width="180" height="22" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.8"/>
<text x="78" y="29" fill="currentColor">120÷4=30</text>
<text x="330" y="29" text-anchor="end" fill="currentColor">34 分钟</text>
<text x="10" y="73" fill="currentColor">10 片</text>
<rect x="50" y="58" width="24" height="22" fill="currentColor" fill-opacity="0.45" stroke="currentColor" stroke-width="0.8"/>
<rect x="74" y="58" width="72" height="22" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.8"/>
<text x="78" y="73" fill="currentColor">12</text>
<text x="330" y="73" text-anchor="end" fill="currentColor">16 分钟</text>
<text x="10" y="117" fill="currentColor">40 片</text>
<rect x="50" y="102" width="24" height="22" fill="currentColor" fill-opacity="0.45" stroke="currentColor" stroke-width="0.8"/>
<rect x="74" y="102" width="36" height="22" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.8"/>
<text x="116" y="117" fill="currentColor">最长单条 6</text>
<text x="330" y="117" text-anchor="end" fill="currentColor">10 分钟</text>
<rect x="50" y="146" width="14" height="12" fill="currentColor" fill-opacity="0.45" stroke="currentColor" stroke-width="0.8"/>
<text x="70" y="156" fill="currentColor">固定开销 4 分钟</text>
<rect x="180" y="146" width="14" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.8"/>
<text x="200" y="156" fill="currentColor">最慢分片的测试</text>
</g>
</svg>

**限制收益的因素**：
- **固定开销**：分片越多，开销占比越大。用预装依赖的镜像、缓存把它压低，是加分片之前该先做的。
- **最长的单条测试**：总时长不可能低于它。要么把它拆开，要么把它移出这一档（放到夜间）。
- **耗时估计过时**：测试变慢了而历史数据没更新，分片失衡。每天用最新结果重算。
- **长尾机器**：40 台机器里总有一台慢或排队久，分片越多，碰上慢机器的概率越大。
- **共享资源**：所有分片都打同一个数据库或同一个制品服务器，并发上去后它成了瓶颈。

**判断要不要再加分片**：看最慢分片时长和平均分片时长的比值。比值接近 1 且固定开销占比低，加分片才有用；比值大，先去处理最长测试和失衡。

一句话：分片能把"测试耗时"除以 N，但除不掉固定开销和最长的那条测试。
