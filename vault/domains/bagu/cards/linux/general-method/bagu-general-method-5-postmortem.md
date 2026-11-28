---
id: bagu-general-method-5-postmortem
node: a.linux.general-method
type: qa
step: 5
---
## Q
**故障复盘 · 要记录什么**｜追问

面试官：「故障恢复之后，你会怎么复盘？」

## A
**基本回答。** 复盘文档至少包含：时间线（发现、定位、止血、恢复各时间点）、影响范围（用户、订单、金额、时长）、根因和触发条件、哪些监控或预案没起作用、带负责人和完成时间的改进项。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<line x1="20" y1="54" x2="320" y2="54" stroke-width="1.2" stroke="currentColor"/>
<rect x="16" y="50" width="8" height="8" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="256" y="50" width="8" height="8" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="316" y="50" width="8" height="8" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="20" y="38" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">故障开始</text>
<text x="330" y="38" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">回滚完 15 分</text>
<text x="260" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">发现</text>
<text x="140" y="96" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">发现用 12 分钟</text>
<text x="290" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">回滚 3 分钟</text>
<text x="4" y="148" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">① 时间线：发现·定位·止血·恢复</text>
<text x="4" y="170" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">② 影响：用户·订单·金额·时长</text>
<text x="4" y="192" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">③ 根因和触发条件</text>
<text x="4" y="214" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">④ 哪些监控或预案没起作用</text>
<text x="4" y="236" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">⑤ 改进项：负责人+完成时间</text>
<text x="4" y="254" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">目的：下次不再发生，或更快恢复</text>
</svg>
上半部分是一条时间线：故障开始、第 12 分钟发现、第 15 分钟回滚完成。下半部分是复盘文档的五个组成部分，第 5 项（改进项）是整份文档的价值所在。
**举个例子。** 支付成功率下降事故复盘：
1. **时间线：** 14:00 发布上线；14:10 成功率开始下降；14:22 告警触发，发现用了 12 分钟；14:25 回滚完成，回滚用了 3 分钟。
2. **影响范围：** 从 14:10 到 14:25 共 15 分钟，写清这段时间内支付失败的订单笔数、金额和受影响用户数；其中状态不明的订单需要对账补查。
3. **根因和触发条件：** 新版本对渠道超时的处理有缺陷；渠道变慢时触发。
4. **没起作用的监控：** 没有渠道超时率的告警，靠成功率告警才发现，慢了 12 分钟。
5. **改进项：** 给渠道超时率加告警，负责人某某，两周内完成；补查故障窗口内状态不明的订单做对账。
**容易错。**
- **复盘变成追责：** 一旦变成找人背锅，大家就会隐瞒信息，下次更难查清。
- **改进项写得空：** 「提高警惕」「加强测试」没法验证是否做到。
- **只写为什么发生：** 不分析为什么扩大，漏掉了「发现太慢」「回滚太慢」这类能缩短影响的改进。
- **改进项没人跟：** 没有负责人和完成时间，写完就石沉大海；上线后还要回头检查是否真的生效。
