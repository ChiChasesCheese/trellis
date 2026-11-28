---
id: bagu-loop-react-planning-1-agent-vs-workflow
node: a.agent.loop-react-planning
type: qa
step: 1
---
## Q
**Agent · 和 Chatbot、Workflow 的区别**｜必会

面试官：「Agent 和普通聊天机器人、固定工作流到底有什么区别？什么任务该用 Agent？」

## A
**基本回答。** 区别在谁决定执行路径。Chatbot（聊天机器人）只生成回复，不做事；Workflow（工作流）的步骤和分支由人事先画好；Agent 由模型在运行中根据中间结果决定下一步，并调用工具真正做事，由 LLM（推理决策）、规划（拆任务）、记忆（短期是当前对话，长期是跨会话偏好）、工具（查接口、执行代码）四块组成，外面还有一层 Harness 管循环控制、权限、预算和观测。Agent 每步都是一次模型决策，更慢更贵更难调试。路径能事先写死就用 Workflow，写不死才用 Agent；两者都有，就在固定流程里嵌一个 Agent 子循环。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<text x="40" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">名称</text>
<text x="142" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">谁决定路径</text>
<text x="273" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">典型例子</text>
<rect x="4" y="24" width="72" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="40.0" y="44.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Chatbot</text>
<rect x="80" y="24" width="126" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="143.0" y="44.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">没有路径：只回复</text>
<rect x="210" y="24" width="126" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="273.0" y="44.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">闲聊、问答</text>
<rect x="4" y="64" width="72" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="40.0" y="84.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Workflow</text>
<rect x="80" y="64" width="126" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="143.0" y="84.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">人事先画好流程</text>
<rect x="210" y="64" width="126" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="273.0" y="84.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">扣库存、支付流转</text>
<rect x="4" y="104" width="72" height="32" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="40.0" y="124.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Agent</text>
<rect x="80" y="104" width="126" height="32" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="143.0" y="124.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">模型边做边决定</text>
<rect x="210" y="104" width="126" height="32" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="273.0" y="124.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">排障、调研</text>
<rect x="4" y="152" width="332" height="50" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="170.0" y="173.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">常见组合：固定主流程</text>
<text x="170.0" y="188.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">里嵌一个有步数上限的 Agent 子循环</text>
</svg>
三种东西按「谁决定路径」排开：只有最后一行的路径是模型在运行时临时决定的。
**容易错。**
- **以为 Agent 更高级，什么都用它：**固定逻辑交给 Agent 只会更慢更贵更难测。
- **以为给聊天机器人接个工具就叫 Agent：**关键看下一步是不是由模型在运行中决定，而不是有没有工具。
- **以为路径不确定就该用 Agent：**很多时候是需求没拆清楚，拆开后是固定节点加局部模型判断。
- **以为 Agentic Workflow 就是自主 Agent：**它的路径仍由人定义，模型只在节点里做生成或判断。
**业务场景。** 「排查今天打赏到账变慢」：先看监控，渠道延迟高就查渠道状态，正常就翻日志，下一步取决于上一步发现了什么，适合 Agent；「打赏扣币」校验余额、扣币、记账、通知，步骤固定，写成普通服务；视频审核是固定流水线（抽帧、模型打分、人工复核），只在规则判不了的疑难样本上放一个有步数上限的 Agent。
