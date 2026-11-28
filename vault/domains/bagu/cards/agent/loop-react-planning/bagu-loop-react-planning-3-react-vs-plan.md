---
id: bagu-loop-react-planning-3-react-vs-plan
node: a.agent.loop-react-planning
type: qa
step: 3
---
## Q
**ReAct 与 Plan-and-Execute · 怎么选**｜必会

面试官：「ReAct 和 Plan-and-Execute 有什么区别？你的任务该选哪个？」

## A
**基本回答。** ReAct 是推理一步、调用一次工具、看结果再推理，边走边调整，适合路径不确定、工具反馈快的任务（排查问题、查资料），代价是步数多、Token 贵、容易局部打转。Plan-and-Execute 是先由模型列出完整的分步计划，再逐项执行，适合步骤多、依赖清晰的长任务，代价是计划会过时、遇到意外调整弱：计划只在开头生成一次，所以要允许重新规划（replan）并记录计划版本，否则退化成静态流程。常见组合是外层 Plan 给结构，每一步内部跑 ReAct 子循环。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<text x="6" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ReAct：边走边看</text>
<rect x="6" y="24" width="80" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="46.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">推理一步</text>
<rect x="130" y="24" width="80" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">调一次工具</text>
<rect x="254" y="24" width="80" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="294.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">看结果</text>
<line x1="86" y1="39" x2="124.0" y2="39.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="130.0,39.0 124.0,42.0 124.0,36.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="210" y1="39" x2="248.0" y2="39.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="254.0,39.0 248.0,42.0 248.0,36.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="294" y1="54" x2="294" y2="70" stroke-width="1.2" stroke="currentColor"/>
<line x1="294" y1="70" x2="46" y2="70" stroke-width="1.2" stroke="currentColor"/>
<line x1="46" y1="70" x2="46.0" y2="60.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="46.0,54.0 49.0,60.0 43.0,60.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="6" y="104" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Plan-and-Execute：先列计划</text>
<rect x="4" y="114" width="76" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="42.0" y="133.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">查订单</text>
<line x1="80" y1="129" x2="83.0" y2="129.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="89.0,129.0 83.0,132.0 83.0,126.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="89" y="114" width="76" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="127.0" y="133.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">查退款规则</text>
<line x1="165" y1="129" x2="168.0" y2="129.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="174.0,129.0 168.0,132.0 168.0,126.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="174" y="114" width="76" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="212.0" y="133.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">发起退款</text>
<line x1="250" y1="129" x2="253.0" y2="129.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="259.0,129.0 253.0,132.0 253.0,126.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="259" y="114" width="76" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="297.0" y="133.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">通知用户</text>
<line x1="127" y1="144" x2="127.0" y2="164.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="127.0,170.0 124.0,164.0 130.0,164.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="30" y="170" width="220" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="140.0" y="189.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">订单已部分退款 → 重新规划</text>
<text x="170" y="224" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">组合：外层 Plan，每一步里跑 ReAct</text>
</svg>
第一行是 ReAct 的小循环；第二行是先定好的计划，中途遇到意外就重新规划。
**容易错。**
- **以为 Plan 更先进，ReAct 过时了：**两者适用的任务不同：路径不确定用 ReAct，步骤依赖清晰的长任务用 Plan。
- **以为计划写好就不用改：**不允许重新规划，遇到意外只能硬跑，等于静态流程。
- **以为 Reflection 是第三种架构：**它是叠在前两者上的失败复盘，不单独成一种；多一次模型调用，要限制反思轮数。
- **一上来就上 Multi-Agent：**先用最简单的方式跑通，按失败模式再升级。
**业务场景。** 退款 Agent 处理「退掉订单 1029」：外层计划「查订单 → 查退款规则 → 发起退款 → 通知用户」，第 1 步内部是 ReAct 小循环；执行到第 2 步发现订单已部分退款，计划前提不成立，重新规划为只退差额，记成 v2，旧版本保留便于排查。
