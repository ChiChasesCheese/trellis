---
id: bagu-multi-agent-workflow-1-patterns-recovery
node: b.agent.multi-agent-workflow
type: qa
step: 1
---
## Q
**多 Agent 协作 · 编排模式、Workflow / Graph 与失败恢复**｜追问

面试官：「什么时候该用多 Agent，而不是单 Agent 加工具？研究、写作、审核、发布四个 Agent，审核失败要回到写作，怎么表达？失败后怎么恢复，人工审批怎么暂停和恢复？」

## A
**基本回答。** 单 Agent 加工具能解决的先别拆；子任务能并行、需要隔离上下文或权限、角色差异大时才拆。常见编排：顺序、并行、路由、Supervisor（主 Agent 动态调度）、Handoff（移交控制权）、评审与优化循环。四个 Agent 用 Graph 表达：节点是 Agent，共享同一份 State，审核到写作用条件边（这就是 Loop，图上的回退控制），并设最大回退次数。步骤固定就用代码静态编排，子任务无法预知才动态委派。失败要分类：输入和权限错误不重试，瞬时故障有界重试加退避抖动，质量不达标最多修正一次或降级。恢复靠检查点，存阶段、已完成角色、产物引用、预算；有外部副作用的动作交给统一执行器并带幂等键，高风险动作前暂停，批准后恢复。
**2026 亮点。** 长时间运行的 Agent 可交给持久化执行引擎（如 Temporal 加 OpenAI Agents SDK，Python 版已 GA）：Agent 循环放进 Workflow，模型调用是 Activity，结果写进事件历史，崩溃重放不重复调模型、不重复计费；代价是代码要遵守确定性约束，MCP 服务器在引擎之外不受保护。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<rect x="8" y="34" width="66" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="41" y="58" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">研究</text>
<rect x="94" y="34" width="66" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="127" y="58" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写作</text>
<rect x="180" y="34" width="66" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="213" y="58" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">审核</text>
<rect x="266" y="34" width="66" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="299" y="58" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">发布</text>
<line x1="74" y1="54" x2="94" y2="54" stroke-width="1.2" stroke="currentColor"/>
<polygon points="94.0,54.0 87.0,57.2 87.0,50.8" fill="currentColor" stroke-width="0.5" stroke="currentColor"/>
<line x1="160" y1="54" x2="180" y2="54" stroke-width="1.2" stroke="currentColor"/>
<polygon points="180.0,54.0 173.0,57.2 173.0,50.8" fill="currentColor" stroke-width="0.5" stroke="currentColor"/>
<line x1="246" y1="54" x2="266" y2="54" stroke-width="1.2" stroke="currentColor"/>
<polygon points="266.0,54.0 259.0,57.2 259.0,50.8" fill="currentColor" stroke-width="0.5" stroke="currentColor"/>
<text x="299" y="26" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">人工确认</text>
<line x1="213" y1="74" x2="213" y2="96" stroke-width="1.2" stroke="currentColor"/>
<line x1="213" y1="96" x2="127" y2="96" stroke-width="1.2" stroke="currentColor"/>
<line x1="127" y1="96" x2="127" y2="76" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="127.0,76.0 130.2,83.0 123.8,83.0" style="fill:var(--accent,#3b6fd4)" stroke-width="0.5" style="stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="116" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">审核不通过：回写作，有最大回退次数</text>
<rect x="8" y="134" width="324" height="36" rx="3" fill="none" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="170" y="156" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">共享 State：阶段、已完成角色、产物引用、预算</text>
<text x="8" y="192" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每个节点执行完就写检查点，</text>
<text x="8" y="210" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">重启或审批通过后，从最近检查点接着跑</text>
</svg>
节点是 Agent，箭头是下一步；审核到写作是一条条件边，满足「不通过」才走，并有次数上限；所有节点读写同一份 State，也是检查点存的内容。
**容易错。**
- **一上来就拆多 Agent：** 能用单 Agent 加工具解决的先别拆，多 Agent 的 Token 成本和时延会叠加，调试更难。
- **回退不设上限：** 审核到写作的回路必须设最大回退次数，否则可能无限返工。
- **失败统一重试：** 输入和权限错误重试没用；只有瞬时故障才有界重试。
- **每层都重试：** SDK、执行器、网关各重试一轮，次数会相乘，重试预算只留一个持有者。
- **把 Agent 当确定性代码：** Agent 节点输出不确定，要多做质量校验。

**业务场景。** 退款工单：分类、查单、审核、执行四个 Agent，审核不过退回查单，执行前人工确认，确认时的金额参数被绑定、改了就要重批。
