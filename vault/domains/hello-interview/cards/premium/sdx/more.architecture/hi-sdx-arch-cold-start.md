---
id: hi-sdx-arch-cold-start
node: more.architecture
type: qa
step: 8
---
## Q
**FaaS 冷启动：花在哪、怎么压**｜补充 · 服务架构：微服务、服务发现、Serverless · 追问

面试官：「我们的 Serverless 接口偶尔特别慢，说是冷启动。冷启动具体发生了什么，大概多慢，有哪些缓解办法？」

## A
**结论。** 没有空闲实例时，平台要现场建沙箱（microVM 或容器）、加载运行时、加载你的代码、跑初始化，然后才处理请求。官方给的量级是不到 100 毫秒到一秒多，JVM 和大依赖包更慢。缓解：预置并发、缩小初始化、快照启动。

**要点。**
- **预置并发：** 付费让 N 个实例一直保持已初始化，延迟敏感的路径靠它。
- **缩小初始化：** 精简依赖包，依赖惰性加载，选轻量运行时。
- **快照启动：** 初始化完成后拍快照，新实例从快照恢复（如 Lambda SnapStart，支持 Java、Python、.NET 的较新版本，不能和预置并发同时用）。
- **尾延迟：** 冷启动只占少数请求（官方说通常不到 1%），却决定 p99；流量突增时每多开一个并发实例就是一次冷启动。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">冷启动（没有空闲实例）</text>
<rect x="8" y="26" width="70" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="43.0" y="47.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">建沙箱</text>
<rect x="82" y="26" width="78" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="121.0" y="47.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">载运行时</text>
<rect x="164" y="26" width="98" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="213.0" y="47.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">载代码+init</text>
<rect x="266" y="26" width="66" height="34" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="299.0" y="47.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">处理请求</text>
<text x="8" y="92" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">热实例（复用已有环境）</text>
<rect x="266" y="102" width="66" height="34" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="299.0" y="123.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">处理请求</text>
<text x="8" y="126" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">直接进入</text>
<line x1="8" y1="150" x2="332" y2="150" stroke-width="1" stroke="currentColor" opacity="0.4" stroke-dasharray="3 3"/>
<text x="8" y="172" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">预置并发：提前把前三步做好并保温</text>
<text x="8" y="192" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">缩小初始化 / 快照启动：压短前三步</text>
</svg>

**面试里这样说。** 「冷启动要分开看：它不影响平均值，但会拖高 p99。延迟敏感的接口我用预置并发保温，其余的缩小包体、把初始化挪到惰性加载；Java 再加快照启动。」

**易错。**
- **以为冷启动免费：** Lambda 从 2025 年 8 月起，按需调用的 ZIP 函数其初始化阶段也计费。
- **只看平均延迟：** 平均值正常，p99 被冷启动拖垮，用户照样感知到。
