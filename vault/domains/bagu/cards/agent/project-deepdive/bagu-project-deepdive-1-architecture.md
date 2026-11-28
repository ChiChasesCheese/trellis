---
id: bagu-project-deepdive-1-architecture
node: a.agent.project-deepdive
type: qa
step: 1
---
## Q
**Agent 项目 · 从一次请求讲清整体架构**｜必会

面试官：「你们 Agent 项目的整体架构是怎么设计的？」

## A
**基本回答。** 不要报技术栈，带面试官走完一次请求，再回头说各层职责。以「申请售后」为例：
1. 接入层：鉴权、限流，生成 `requestId` 和 `runId`。
2. 编排层读取任务状态，判断信息是否齐全。
3. Agent 选工具查订单，业务层再校验一次权限；检索售后政策作为证据。
4. 写工单前展示参数让用户确认，确认后校验幂等键再执行。
5. 保存业务工单号和最终状态，全程记录 Trace。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 300">
<rect x="8" y="8" width="232" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="124.0" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1 接入：鉴权、限流</text>
<text x="124.0" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">生成 requestId、runId</text>
<line x1="124" y1="48" x2="124.0" y2="55.0" stroke="currentColor" stroke-width="1.2"/>
<polygon points="124,62 120.8,55.0 127.2,55.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="62" width="232" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="124.0" y="78.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2 编排：读任务状态</text>
<text x="124.0" y="93.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">判断信息齐不齐</text>
<line x1="124" y1="102" x2="124.0" y2="109.0" stroke="currentColor" stroke-width="1.2"/>
<polygon points="124,116 120.8,109.0 127.2,109.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="116" width="232" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="124.0" y="132.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3 Agent 选工具查订单</text>
<text x="124.0" y="147.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">业务层再校验权限；检索政策</text>
<line x1="124" y1="156" x2="124.0" y2="163.0" stroke="currentColor" stroke-width="1.2"/>
<polygon points="124,170 120.8,163.0 127.2,163.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="170" width="232" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="124.0" y="186.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4 写之前：展示参数</text>
<text x="124.0" y="201.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">用户确认，再校验幂等键</text>
<line x1="124" y1="210" x2="124.0" y2="217.0" stroke="currentColor" stroke-width="1.2"/>
<polygon points="124,224 120.8,217.0 127.2,217.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="224" width="232" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="124.0" y="240.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5 落库：业务工单号</text>
<text x="124.0" y="255.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">和最终状态，不只在对话里</text>
<rect x="256" y="8" width="76" height="256" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="294" y="130" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">全程</text>
<text x="294" y="148" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Trace</text>
<text x="8" y="292" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">走完一次请求，再回头讲各层职责</text>
</svg>
一次「申请售后」请求自上而下走五站，右边的虚线框表示全程都在记录 Trace（链路追踪）；高亮的是会改数据的那一站。
**容易错。**
- **只报技术栈和分层名词：** 面试官听不出你做了什么决策；要走完一次请求。
- **以为状态存在对话历史里就够：** 业务状态要存在业务库里。
- **只靠模型判断权限：** 业务层在工具里要再校验一次。
- **硬说微服务：** 没有那么多服务，就如实讲逻辑分层（接入、编排、模型、上下文、工具、状态、治理）。
- **说不清框架和自研的边界：** 哪些是框架提供的、哪些是自己补的，一被追问就露馅。
