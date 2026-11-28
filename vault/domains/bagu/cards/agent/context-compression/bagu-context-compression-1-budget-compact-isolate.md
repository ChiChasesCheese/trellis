---
id: bagu-context-compression-1-budget-compact-isolate
node: b.agent.context-compression
type: qa
step: 1
---
## Q
**上下文工程 · Token 预算、压缩与子 Agent 隔离**｜追问

面试官：「Agent 跑长任务，上下文快满了怎么办？Token 预算怎么在历史、检索证据和工具结果之间分？压缩会丢信息，怎么评估压缩质量？」

## A
**基本回答。** 窗口大不等于用得好：内容越长越杂，模型越难稳定找到关键信息（上下文腐化，Context Rot）。三招各管一类：压缩（Compaction）在窗口将满时把历史摘要成要点继续；结构化笔记把进展写进外部文件，重置后再读；子 Agent 在独立上下文里检索，只回传精简摘要。还有 Lost in the Middle：埋在中间的内容最容易被忽略，所以要主动裁剪，不能一直往里塞。
**2026 亮点。** 即时检索（just-in-time）：上下文只放路径、链接等轻量引用，用到时再用工具读；代价是每次取数多一轮调用、延迟变长。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 332">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">上下文窗口的预算（从上到下）</text>
<rect x="8" y="24" width="110" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="63" y="41" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">系统提示</text>
<text x="128" y="41" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">固定，先保</text>
<rect x="8" y="54" width="110" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="63" y="71" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">任务约束</text>
<text x="128" y="71" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">当前目标与约束优先级最高</text>
<rect x="8" y="84" width="110" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="63" y="101" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">历史</text>
<text x="128" y="101" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">近几轮保留，旧的做摘要</text>
<rect x="8" y="114" width="110" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="63" y="131" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">检索证据</text>
<text x="128" y="131" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">按相关度截断</text>
<rect x="8" y="144" width="110" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="63" y="161" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">工具结果</text>
<text x="128" y="161" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">已消化的最先清掉</text>
<rect x="8" y="174" width="110" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="63" y="191" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">输出预留</text>
<text x="128" y="191" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">固定，先保</text>
<line x1="8" y1="212" x2="332" y2="212" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<text x="8" y="232" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">三招各管一类</text>
<rect x="8" y="242" width="104" height="48" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="60" y="262.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">压缩摘要</text>
<text x="60" y="277.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">持续对话</text>
<rect x="118" y="242" width="104" height="48" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="262.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">外部笔记</text>
<text x="170" y="277.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">有里程碑的任务</text>
<rect x="228" y="242" width="104" height="48" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="280" y="262.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">子 Agent</text>
<text x="280" y="277.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">可并行的研究</text>
<text x="8" y="310" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">子 Agent 在独立上下文里探索数万 token，</text>
<text x="8" y="326" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只回传约 1000 到 2000 token 的结论</text>
</svg>
上半部分是一个窗口里各部分怎么分预算：固定部分先保，余量按价值分，旧工具结果最先清；下半部分是三种手段分别对应的任务形态。
**容易错。**
- **以为窗口越大越好：** 大窗口放得进去不等于用得好，更贵，也更容易漏掉埋在中间的信息。
- **只在提示词里写重要：** 关键约束别埋在中间，要放在显眼位置，并在压缩时明确保留。
- **压缩只追求短：** 先保证不漏决策、未解决问题和关键细节，再去冗余；压缩前后要拿任务通过率验证。
- **比例照抄通用值：** 预算比例没有通用值，要用自己的真实轨迹评。
**举个例子。** 支付客服 Agent 处理 30 多轮退款工单，窗口里夹着几万 token 的交易日志，只有一行写着「该笔已退款」：
1. 先清已消化的日志，只留「查过日志，结论：已退款」；早期轮次压成要点，保留决策（已退款）、未解决问题（用户还问发票）、订单号和金额，近几轮原文不动。
2. 拿同一批工单跑压缩前后的上下文，比通过率，查「已退款」这类关键事实还在不在；要核对整月账单就改写进度笔记或派子 Agent，只回传几百字结论。
