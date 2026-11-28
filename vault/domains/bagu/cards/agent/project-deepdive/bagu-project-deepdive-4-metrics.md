---
id: bagu-project-deepdive-4-metrics
node: a.agent.project-deepdive
type: qa
step: 4
---
## Q
**指标 · 用什么衡量项目效果，数据怎么支撑**｜必会

面试官：「你说这个 Agent 效果不错，用什么指标衡量的？数据怎么来的？」

## A
**基本回答。** 先讲任务有没有完成，再讲过程、成本和失败后是否可控：
- 效果：任务完成率、最终业务状态正确率、事实有据率。
- 过程：工具选择与参数正确率、多余调用率、越权调用数。
- 成本延迟：端到端 P50/P95、模型调用数、Token、单任务成本。
- 可控性：转人工率、重复副作用数、故障恢复率。
并交代评测集来源、成功怎么判定、每个任务跑几次、和哪个基线比。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<rect x="8" y="8" width="160" height="76" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="88.0" y="27.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">效果</text>
<text x="88.0" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">任务完成率</text>
<text x="88.0" y="57.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">业务状态正确率</text>
<text x="88.0" y="72.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">事实有据率</text>
<rect x="172" y="8" width="160" height="76" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="252.0" y="27.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">过程</text>
<text x="252.0" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">工具选择与参数正确率</text>
<text x="252.0" y="57.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">多余调用率</text>
<text x="252.0" y="72.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">越权调用数</text>
<rect x="8" y="92" width="160" height="76" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="88.0" y="111.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">成本延迟</text>
<text x="88.0" y="126.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">P50、P95 延迟</text>
<text x="88.0" y="141.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">模型调用数、Token</text>
<text x="88.0" y="156.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">单任务成本</text>
<rect x="172" y="92" width="160" height="76" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="252.0" y="111.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">可控性</text>
<text x="252.0" y="126.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">转人工率</text>
<text x="252.0" y="141.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">重复副作用数</text>
<text x="252.0" y="156.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">故障恢复率</text>
<text x="8" y="192" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">先交代评测集来源、成功怎么判、</text>
<text x="8" y="210" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每任务跑几次、和哪个基线比</text>
</svg>
四组指标：效果、过程、成本延迟、可控性；高亮的可控性管「出了事能不能兜住」，对会写数据的 Agent 最要紧。
**容易错。**
- **只报一个准确率：** 没有评测集、成功判定、运行次数和基线，这个数字不可核对。
- **只看平均延迟：** 平均值会掩盖长尾；P50 是一半请求比它快，P95 是 95% 的请求比它快，看 P95、P99。
- **要求步骤顺序一致才算对：** 开放任务有多条正确路径，先验证最终业务状态和安全规则。
- **补造线上数据：** 没上线就讲离线评测集、错误分布和故障注入结果，并明说是离线数据；被追问口径会穿帮。
**举个例子。** 退款 Agent 有 100 个评测任务（来自历史工单），每个跑 5 次：500 次里最终业务状态正确 425 次，正确率 85%；成功按最终状态和安全规则判定，基线是只用规则的机器人。把 500 次耗时排序，第 475 次附近就是 P95。重复退款数和越权调用数必须是 0，比回答自然不自然重要。
