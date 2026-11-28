---
id: bagu-harness-1-model-plus-harness
node: b.agent.harness
type: qa
step: 1
---
## Q
**Harness Engineering · Agent = Model + Harness、断点续跑**｜追问

面试官：「什么是 Harness Engineering？它和 Prompt、Context Engineering 是什么关系？长任务跑到一半进程重启，怎么从断点继续，怎么人工接管？」

## A
**基本回答。** Agent = Model + Harness：模型只做推理和生成；Harness 是模型之外的一切，包括工具、文件系统、沙箱、上下文管理、验证反馈和错误恢复。三者像三层套娃：Prompt 解决怎么把指令说清，Context 解决该给它看什么，Harness 解决系统怎么持续执行、纠偏、观测和恢复。Agent 不稳，先查工具接口和错误信息是否清楚、有没有验证闭环（跑测试或校验结果）、上下文是否塞了无关内容、失败后有无重试回退，用 Trace 找到第一步出错的位置，不是先换模型。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="8" y="8" width="324" height="138" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="26" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Harness：工具、沙箱、验证、检查点、恢复</text>
<rect x="22" y="36" width="296" height="100" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="54" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Context：该给模型看什么</text>
<rect x="38" y="64" width="264" height="62" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="91.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Prompt：怎么把指令说清</text>
<text x="170" y="106.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">模型：只做推理和生成</text>
<line x1="8" y1="160" x2="332" y2="160" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<text x="8" y="178" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">长任务进程重启：从检查点续跑</text>
<rect x="8" y="188" width="142" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="79" y="206.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">第 1–3000 笔</text>
<text x="79" y="221.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">已写入检查点</text>
<line x1="150" y1="210" x2="190" y2="210" stroke-width="1.2" stroke="currentColor"/>
<polygon points="190.0,210.0 183.0,213.2 183.0,206.8" fill="currentColor" stroke-width="0.5" stroke="currentColor"/>
<text x="170" y="202" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">重启</text>
<rect x="190" y="188" width="142" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="261" y="206.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">从第 3001 笔续跑</text>
<text x="261" y="221.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">幂等键防重复</text>
<text x="8" y="252" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">检查点存：计划、已完成步骤、产物引用、预算</text>
</svg>
上半部分是三层套娃：Harness 最大，里面是 Context，最里面才是 Prompt；下半部分是长任务重启后，靠检查点接着干。
**容易错。**
- **Agent 不稳就换模型：** 先查工具接口、错误信息和验证闭环，往往是 Harness 的问题。
- **检查点只存聊天记录：** 要存计划、已完成步骤、产物引用和预算，聊天记录恢复不出这些。
- **重试所有工具调用：** 只有读操作可以直接重试，有副作用的必须带幂等键。
- **让模型自己填幂等键：** 幂等键由执行层按业务请求 ID 和动作生成，不让模型自己填。
- **把六层框架当标准：** 它只是分析时用的框架，不是行业标准。
**业务场景。** 对账 Agent 核对 5000 笔订单，跑到第 3000 笔时进程重启：从检查点恢复，前 3000 笔不重核；已建的差异工单带幂等键，服务端唯一约束挡住重复；崩溃时正在核的那笔结果未知，先查状态再决定是否重放；批量关单前暂停，等人工批准。
