---
id: bagu-project-deepdive-5-badcase
node: a.agent.project-deepdive
type: qa
step: 5
---
## Q
**Badcase 复盘 · 从发现、定位、修复到回归**｜必会

面试官：「讲一个你遇到的 Badcase：怎么发现的，怎么定位，怎么修复，怎么防止再出现？」

## A
**基本回答。** Badcase 就是 Agent 做错了的一个具体案例。按七步讲，并先说明证据是线上事故、离线注入还是设计预案：
1. 保存现场：输入、版本、上下文、检索结果、工具请求与响应。
2. 说清预期、实际和影响范围。
3. 分层假设：数据、检索、模型、工具、编排、第三方。
4. 控制变量，一次只改一项。
5. 用能稳定复现的证据确认根因。
6. 在正确的层修复。
7. **bad case 进回归集：** 把原始 case 和相邻边界 case 加入回归集。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 318">
<rect x="8" y="8" width="324" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="26.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1 保存现场：输入、版本、检索、工具响应</text>
<line x1="170" y1="36" x2="170.0" y2="39.0" stroke="currentColor" stroke-width="1.2"/>
<polygon points="170,46 166.8,39.0 173.2,39.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="46" width="324" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2 说清预期、实际和影响范围</text>
<line x1="170" y1="74" x2="170.0" y2="77.0" stroke="currentColor" stroke-width="1.2"/>
<polygon points="170,84 166.8,77.0 173.2,77.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="84" width="324" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="102.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3 分层假设：数据、检索、模型、工具、编排、第三方</text>
<line x1="170" y1="112" x2="170.0" y2="115.0" stroke="currentColor" stroke-width="1.2"/>
<polygon points="170,122 166.8,115.0 173.2,115.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="122" width="324" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="140.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4 控制变量，一次只改一项</text>
<line x1="170" y1="150" x2="170.0" y2="153.0" stroke="currentColor" stroke-width="1.2"/>
<polygon points="170,160 166.8,153.0 173.2,153.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="160" width="324" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="178.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5 用稳定复现的证据确认根因</text>
<line x1="170" y1="188" x2="170.0" y2="191.0" stroke="currentColor" stroke-width="1.2"/>
<polygon points="170,198 166.8,191.0 173.2,191.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="198" width="324" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="216.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6 在正确的那一层修复</text>
<line x1="170" y1="226" x2="170.0" y2="229.0" stroke="currentColor" stroke-width="1.2"/>
<polygon points="170,236 166.8,229.0 173.2,229.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="236" width="324" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="254.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7 原 case 加相邻边界 case 进回归集</text>
<text x="8" y="296" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">开头先说明证据：线上事故、离线注入还是设计预案</text>
</svg>
七步从上到下：先保现场，再分层假设、控制变量、确认根因，修复后把案例沉淀进回归集。
**容易错。**
- **只说优化了提示词：** 看不出根因是否找对。
- **一次改多项：** 改了提示词、工具描述和模型，不知道是谁起了作用。
- **把预案讲成真实事故：** 先说明证据是线上事故、离线注入还是设计预案。
- **修好就完：** 不进回归集，同类问题还会再出现。
**举个例子。** 工程类：创建工单超时后出现两张工单。只关掉重试现象消失，只加幂等键也消失，确认根因是超时被记成失败、Agent 重试，而接口没有幂等、第一次其实已写入。修复：稳定的 `actionId` 作幂等键，超时先查状态，Trace 标记「结果未知」；回归用例模拟「服务端已写入、响应丢失」，并加相邻边界 case。
效果类：「查通用退款政策」与「查这笔订单能否退」两个工具名相近，用户给了订单号，Agent 却选了前者。修复：写清两者职责，把订单号放进状态摘要，有订单号才暴露后者。
