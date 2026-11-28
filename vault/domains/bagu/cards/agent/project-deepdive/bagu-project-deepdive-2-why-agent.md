---
id: bagu-project-deepdive-2-why-agent
node: a.agent.project-deepdive
type: qa
step: 2
---
## Q
**选型 · 为什么用 Agent 而不是 Workflow，为什么先单 Agent**｜必会

面试官：「这个场景为什么要用 Agent，普通 Workflow 不行吗？为什么不直接上 Multi-Agent？」

## A
**基本回答。** 先答「去掉大模型，原流程是什么」，再用约束说明取舍（规则有限且稳定时，意图分类加表单补齐就够，自然语言入口不能证明必须用 Agent）：
- 用 Agent：鉴权、确认、写入、审计这些固定步骤放确定性 Workflow；只有「先查订单、检索政策还是追问」这种路径写不死的局部交给 Agent Loop。
- 先单 Agent：状态、Trace 和故障链路更短，更好评测。工具多了先缩减工具集、合并重叠工具、重写描述、用代码路由，再考虑拆。
- 拆 Multi-Agent 的条件：子任务能独立、需要各自上下文、权限差异大、由不同团队维护，至少满足一条；拆分带来通信、成本、调试和延迟的增加。
**2026 亮点。** 多 Agent 约是普通聊天 15 倍的 token（单 Agent 约 4 倍），只有任务可并行、信息量超过单窗口、价值覆盖成本才值得；厂商内部评测在研究任务上比单 Agent 高约 90%，别当通用基准。要有检查点，出错从断点续跑。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 284">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">一次请求的主干：固定步骤写成代码</text>
<rect x="8" y="28" width="46" height="50" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="31.0" y="57.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">鉴权</text>
<rect x="62" y="28" width="100" height="50" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="112.0" y="49.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Agent Loop</text>
<text x="112.0" y="64.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">查单/检索/追问</text>
<rect x="170" y="28" width="46" height="50" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="193.0" y="57.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">确认</text>
<rect x="224" y="28" width="46" height="50" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="247.0" y="57.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写入</text>
<rect x="278" y="28" width="54" height="50" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="305.0" y="57.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">审计</text>
<line x1="54" y1="53" x2="55.0" y2="53.0" stroke="currentColor" stroke-width="1.2"/>
<polygon points="62,53 55.0,56.2 55.0,49.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="162" y1="53" x2="163.0" y2="53.0" stroke="currentColor" stroke-width="1.2"/>
<polygon points="170,53 163.0,56.2 163.0,49.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="216" y1="53" x2="217.0" y2="53.0" stroke="currentColor" stroke-width="1.2"/>
<polygon points="224,53 217.0,56.2 217.0,49.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="270" y1="53" x2="271.0" y2="53.0" stroke="currentColor" stroke-width="1.2"/>
<polygon points="278,53 271.0,56.2 271.0,49.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="102" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">路径写不死的这一小段才交给模型</text>
<text x="8" y="140" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">先单 Agent；工具多了先缩减、合并、</text>
<text x="8" y="158" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">重写描述、用代码路由，再考虑拆</text>
<text x="8" y="188" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">满足下面才拆成 Multi-Agent：</text>
<rect x="8" y="198" width="156" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86.0" y="217.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">子任务能独立</text>
<rect x="176" y="198" width="156" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="254.0" y="217.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">需要各自上下文</text>
<rect x="8" y="238" width="156" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86.0" y="257.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">权限差异大</text>
<rect x="176" y="238" width="156" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="254.0" y="257.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不同团队维护</text>
</svg>
上排是一次请求的固定主干，只有高亮的一小段交给 Agent；下排是拆成多个 Agent 之前必须满足的条件。
**容易错。**
- **说「大模型很强所以用 Agent」：** 没有约束、代价和证据，等于没回答。
- **把所有步骤都交给 Agent：** 鉴权、确认、写入、审计这些固定步骤应由 Workflow 保证确定性。
- **一上来就 Multi-Agent：** 通信、成本、调试和延迟都会增加；先单 Agent，工具多了先缩减和重写。
- **用「提升效果」做证据：** 回答要有约束、选择、代价、证据四样；要给能核对的数字，如「工具选错率从 8% 降到 3%」，「用了 Multi-Agent 提升效果」只是结论，经不起追问。
**举个例子。** 打赏退款：「这笔能不能退」（是否在可退期内、是否已退过）规则固定，写成代码；用户说「刚才那个多扣了」没说哪一笔，先追问还是先查最近订单，交给 Agent Loop。
- 「查通用退款政策」和「查这笔订单能否退」两个工具总被选错，先重写描述、有订单号才暴露后者，选错率从 8% 降到 3%，用评测集核对，而不是直接拆成两个 Agent。
