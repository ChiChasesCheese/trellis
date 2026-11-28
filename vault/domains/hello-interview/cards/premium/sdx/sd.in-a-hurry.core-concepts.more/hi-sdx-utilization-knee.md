---
id: hi-sdx-utilization-knee
node: sd.in-a-hurry.core-concepts.more
type: qa
step: 1
---
## Q
**利用率为什么不能拉满**｜补充 · 核心概念速览 · 追问

财务想把延迟敏感服务的 CPU 利用率从 60% 提到 90% 来省机器。为什么响应时间在到 100% 之前就爆了？该留多少余量？

## A
**结论。** 因为排队：请求随机且成簇到达，利用率越接近 1，队列越难排空，响应时间按 1/(1−ρ) 增长。60% 到 90% 不是慢 50%，而是约 4 倍。

**要点。**
- **算一笔账：** 用简化的单队列模型：平均响应时间 = 服务时间 ÷ (1 − 利用率)。60% 时是 2.5 倍，90% 时是 10 倍，95% 时是 20 倍。
- **尾部更惨：** 响应时间近似指数分布，p99 约为平均的 4.6 倍：60% 时约 11.5 倍服务时间，90% 时约 46 倍。
- **机器账：** 90% 比 60% 少用三分之一的机器，但 p99 变成 4 倍。
- **空闲不是浪费：** 它是吸收突发的缓冲，让队列保持很短。
- **经验值：** 延迟敏感的服务利用率控制在 50% 到 70%；只有吞吐优先的批处理才跑到接近满载。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<text x="8" y="18" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">响应时间 ÷ 服务时间</text>
<line x1="40" y1="176" x2="310" y2="176" stroke-width="1.2" stroke="currentColor"/>
<line x1="40" y1="176" x2="40" y2="32" stroke-width="1.2" stroke="currentColor"/>
<polyline points="40,169 48.1,168.784 56.2,168.553 64.3,168.308 72.4,168.045 80.5,167.765 88.6,167.463 96.7,167.139 104.8,166.789 112.9,166.411 121,166 129.1,165.552 137.2,165.062 145.3,164.525 153.4,163.931 161.5,163.273 169.6,162.538 177.7,161.714 185.8,160.783 193.9,159.721 202,158.5 210.1,157.081 218.2,155.412 226.3,153.419 234.4,151 242.5,148 250.6,144.182 258.7,139.158 266.8,132.25 274.9,122.154 283,106 291.1,76 296.5,36" fill="none" stroke-width="1.6" style="stroke:var(--accent,#3b6fd4)"/>
<circle cx="202" cy="158.5" r="3.5" style="fill:var(--accent,#3b6fd4)"/>
<circle cx="283" cy="106" r="3.5" style="fill:var(--accent,#3b6fd4)"/>
<text x="196" y="146.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">60% → 2.5 倍</text>
<text x="271" y="94" text-anchor="end" font-size="12" font-family="sans-serif" fill="currentColor">90% → 10 倍</text>
<text x="40" y="192" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0%</text>
<text x="175" y="192" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">50%</text>
<text x="310" y="192" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">100%</text>
<text x="175" y="210" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">CPU 利用率</text>
</svg>

**面试里这样说。** 「延迟敏感的服务我把利用率控制在 50% 到 70%。排队时间按 1/(1−ρ) 增长，从 60% 提到 90%，平均响应变成 4 倍，尾部更糟，省下的三分之一机器不值得。」

**易错。**
- **把利用率线性外推到延迟：** 曲线是膝盖形，过了拐点会急剧恶化。
- **只看平均值：** 突发先体现在 p99 上。
- **把模型当精确值：** 真实负载比模型更成簇，拐点来得更早，这里的数字只是量级。
