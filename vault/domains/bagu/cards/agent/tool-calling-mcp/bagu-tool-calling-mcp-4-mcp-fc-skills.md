---
id: bagu-tool-calling-mcp-4-mcp-fc-skills
node: a.agent.tool-calling-mcp
type: qa
step: 4
---
## Q
**MCP · 解决什么问题，和 Function Calling、Skills 的区别**｜追问

面试官：「MCP 解决什么问题？它和 Function Calling、Skills 是什么关系？」

## A
**基本回答。** 三者在不同层，不互相替代。Function Calling 在模型侧，把自然语言变成「工具名 + 参数」。MCP（Model Context Protocol）是应用层协议，规定 Host、Client、Server 之间怎么发现工具、调用工具、返回结果，同一个 Server 可被多个 Agent 和 IDE 复用。Skills 是可复用的任务说明（SOP），按需加载进上下文（启动只载入名称和描述，命中才读正文），可以指导调用多个工具，也可以不调工具。
**2026 亮点。** Agent 调工具和数据用 MCP，不同团队或厂商的 Agent 之间发现与委派任务用 A2A，两者都在 Linux Foundation 开放治理下，不必自造私有协议；协议只解决互通，认证、配额、审计仍要自己做。单团队内部的多 Agent 用进程内编排就够，跨组织才值得上 A2A。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 232">
<rect x="4" y="4" width="80" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="44.0" y="15.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Function</text>
<text x="44.0" y="30.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Calling</text>
<rect x="94" y="4" width="242" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="215.0" y="23.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">模型侧：自然语言 → 工具名 + 参数</text>
<rect x="4" y="52" width="80" height="74" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="44.0" y="93.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">MCP</text>
<rect x="94" y="52" width="62" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="125.0" y="71.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Host</text>
<rect x="176" y="52" width="66" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="209.0" y="71.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Client</text>
<rect x="262" y="52" width="74" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="299.0" y="71.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Server</text>
<line x1="156" y1="67" x2="170.0" y2="67.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="176.0,67.0 170.0,70.0 170.0,64.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="242" y1="67" x2="256.0" y2="67.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="262.0,67.0 256.0,70.0 256.0,64.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="215" y="108" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">应用层协议：发现工具、调用、返回结果</text>
<rect x="4" y="144" width="80" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="44.0" y="163.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Skills</text>
<rect x="94" y="144" width="242" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="215.0" y="163.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">任务说明（SOP）：按需加载</text>
<rect x="4" y="188" width="332" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="170.0" y="208.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">N 个应用 × M 个工具 → 各接一次标准协议</text>
</svg>
三行是三个层次：模型怎么发出调用、工具怎么被接入和复用、一类任务怎么做。最下面是 MCP 省掉的重复工作。
**容易错。**
- **以为 MCP 取代了 Function Calling：**MCP 管工具怎么接入，模型仍然用 Function Calling 选工具。
- **以为上了 MCP 就自带安全：**鉴权、审计、限流、版本管理都要自己做。
- **把 Skills 当成工具：**Skills 是任务说明，不是可调用的接口。
- **所有工具都上 MCP：**只给当前应用用的工具，直接注册本地函数更简单。
**业务场景。** 工单系统被客服 Agent 和值班 Agent 同时使用：封装成一个 MCP Server，两边各接一次；字段 `amount` 的单位（元还是分）写进 Schema，避免两边理解不同。
