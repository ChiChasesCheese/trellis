---
id: bagu-eval-1-golden-judge-rollout
node: b.agent.eval
type: qa
step: 1
---
## Q
**Agent 评测 · Golden Set、LLM-as-Judge、回归与灰度**｜追问

面试官：「问答 Agent 要换模型，怎么评测才敢上线？还没有线上日志，Golden Set 怎么冷启动？让 LLM 当裁判有哪些偏差，怎么校准？」

## A
**基本回答。** 先建 Golden Set（每条样本有明确输入和判分标准的测试集）。换模型前离线跑通过率，与旧模型对比；再灰度小流量看线上指标，有问题可回滚，线上轨迹可回放复现问题。冷启动没有日志：人工构造正常路径、信息缺失、对抗越权三类，再用知识库生成种子题，经人工审核，不能直接当发布依据。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 346">
<rect x="8" y="8" width="292" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="154" y="30" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Golden Set：分层覆盖，20–50 条起步</text>
<line x1="154" y1="44" x2="154" y2="60" stroke-width="1.2" stroke="currentColor"/>
<polygon points="154.0,60.0 150.8,53.0 157.2,53.0" fill="currentColor" stroke-width="0.5" stroke="currentColor"/>
<rect x="8" y="60" width="292" height="36" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="154" y="74.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">离线跑：通过率不低于旧模型</text>
<text x="154" y="89.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">越权用例零失败</text>
<line x1="154" y1="96" x2="154" y2="112" stroke-width="1.2" stroke="currentColor"/>
<polygon points="154.0,112.0 150.8,105.0 157.2,105.0" fill="currentColor" stroke-width="0.5" stroke="currentColor"/>
<rect x="8" y="112" width="292" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="154" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">灰度小流量：对比线上指标</text>
<line x1="154" y1="148" x2="154" y2="164" stroke-width="1.2" stroke="currentColor"/>
<polygon points="154.0,164.0 150.8,157.0 157.2,157.0" fill="currentColor" stroke-width="0.5" stroke="currentColor"/>
<rect x="8" y="164" width="292" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="154" y="186" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">全量上线，出问题就回滚</text>
<line x1="300" y1="178" x2="322" y2="178" stroke-width="1.2" stroke="currentColor"/>
<line x1="322" y1="178" x2="322" y2="26" stroke-width="1.2" stroke="currentColor"/>
<line x1="322" y1="26" x2="300" y2="26" stroke-width="1.2" stroke="currentColor"/>
<polygon points="300.0,26.0 307.0,22.8 307.0,29.2" fill="currentColor" stroke-width="0.5" stroke="currentColor"/>
<text x="8" y="226" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">右侧回路：线上新失败回填 Golden Set</text>
<line x1="8" y1="240" x2="332" y2="240" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<text x="8" y="258" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">LLM 当裁判的偏差和对策</text>
<text x="8" y="280" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">位置偏差：交换 A、B 顺序取一致结论</text>
<text x="8" y="298" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">冗长偏差：偏爱写得长的回答</text>
<text x="8" y="316" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">同源偏差：换厂商交叉评</text>
<text x="8" y="334" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">推理有限：给参考答案或测试结果</text>
</svg>
上半部分是换模型的上线路径，失败案例沿右侧回路回到 Golden Set；下半部分是用 LLM 当裁判时要防的四种偏差。
**容易错。**
- **只看总通过率：** 平均值会稀释高权重失败，要分层统计、单独设阈值。
- **样本越多越好：** 200 条同类不如 100 条覆盖 10 类，覆盖比总量重要。
- **合成题直接当发布依据：** 用知识库生成的种子题必须经人工审核。
- **直接信 LLM 裁判：** 位置偏差（每对题交换 A/B 顺序各评一次，取一致结论）、冗长偏差、偏爱同源模型（换厂商交叉评）、推理有限（给参考答案）；要抽样人工标注，算与人工的一致率，不够就改评分提示词或换裁判。
- **只评最终答案：** Agent 的过程也要评，比如是否先验证身份再退款。
- **离线过了就全量：** 离线样本分布和真实流量不同，必须灰度后再放量。
**举个例子。** 退款问答 Agent 从模型 A 换到 B，没有线上日志：
1. 先人工写 150 条（正常退款、缺订单号、诱导越权），加知识库生成并经人工审核的种子题；两个模型离线各跑一遍，B 通过率不低于 A、越权退款用例零失败才进下一步。
2. 抽查 B 的轨迹是否先验证身份再调退款工具；开放题用 LLM 裁判，再抽 30 条人工标注算一致率。
3. 小流量灰度 B 对比线上指标，出问题回滚到 A；线上新失败补回 Golden Set。
