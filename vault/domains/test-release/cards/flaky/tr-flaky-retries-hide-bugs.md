---
id: tr-flaky-retries-hide-bugs
node: flaky.retries
type: qa
step: 1
---
## Q
为什么"失败就自动重试，直到通过"会掩盖真实缺陷？用概率说明。

## A
**数字**：假设产品里有一个真实的竞态（race condition），让某条测试每次运行有 10% 的概率失败。
- 不重试：每 10 次运行约有 1 次红灯，大家会去查，最终找到竞态。
- 允许重试 2 次（最多跑 3 次）：三次全失败的概率是 0.1³ = 0.001，即 99.9% 的运行显示绿灯。
- 这个竞态在线上会以 10% 的概率出现在真实请求上，但测试几乎永远是绿的。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<g font-family="sans-serif" font-size="12">
<text x="10" y="47" fill="currentColor">不重试</text>
<rect x="100" y="30" width="198.0" height="26" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="0.8"/>
<rect x="298.0" y="30" width="22.0" height="26" fill="currentColor" fill-opacity="0.7"/>
<text x="110" y="47" fill="currentColor">90% 绿灯</text>
<text x="320" y="72" text-anchor="end" fill="currentColor">10% 红灯</text>
<text x="10" y="107" fill="currentColor">最多跑 3 次</text>
<rect x="100" y="90" width="219.8" height="26" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="0.8"/>
<rect x="319.8" y="90" width="1.5" height="26" fill="currentColor" fill-opacity="0.7"/>
<text x="110" y="107" fill="currentColor">99.9% 绿灯</text>
<text x="320" y="132" text-anchor="end" fill="currentColor">0.1% 红灯</text>
<text x="170" y="16" text-anchor="middle" fill="currentColor">真实竞态 每次 10% 失败</text>
</g>
</svg>

**掩盖的三种方式**：
- **真实的间歇性产品缺陷**：竞态、超时设置太紧、资源泄漏导致的偶发失败，本来就是"有时出错"的，重试正好把它们过滤掉。
- **回归被延迟发现**：一个改动让失败率从 1% 升到 30%，重试后看起来仍然大多是绿的，没有人注意到变化。
- **团队失去改进动力**：重试让问题"消失"，没人再去修根因，flaky 越积越多，重试次数越加越大，CI 越来越慢。

**判断一个失败该不该被重试吸收**：问"如果这个失败发生在用户身上，算不算问题？"测试里的竞态如果对应产品代码的竞态，就算；只是测试机器的网络临时断开，就不算。前者必须修，后者才允许重试。
