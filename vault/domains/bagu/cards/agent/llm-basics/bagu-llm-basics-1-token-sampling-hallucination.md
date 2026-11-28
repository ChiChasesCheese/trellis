---
id: bagu-llm-basics-1-token-sampling-hallucination
node: b.agent.llm-basics
type: qa
step: 1
---
## Q
**LLM 运行机制 · Token、上下文窗口、采样参数与幻觉**｜加分

面试官：「Token 是什么，上下文窗口越大效果越好吗？Temperature 和 Top-P 控制什么，为什么模型会有幻觉？」

## A
**基本回答。** 模型是自回归的：每一步根据前文预测下一个 Token（文本碎片，由 BPE 这类子词切分算法得到），选中后接进上下文，再预测下一个。上下文窗口是一次调用里系统提示、历史、当前输入和输出共同占用的 Token 上限。窗口大只是放得进去，不等于用得好：更贵，也更容易漏掉埋在中间的信息。Temperature 在 softmax 前把分数除以 T，T 小更确定、T 大更随机：分数 2、0、0 时，最高分的概率 T=0.2 约 99.99%，T=1 约 78.70%，T=1.5 约 65.48%；结构化提取用 0 到 0.3，创作用 0.8 以上。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 280">
<rect x="8" y="14" width="96" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="56" y="32.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">前文</text>
<text x="56" y="47.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Token 序列</text>
<rect x="122" y="14" width="96" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="32.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">打分变概率</text>
<text x="170" y="47.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">再抽一个</text>
<rect x="236" y="14" width="96" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="284" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">新 Token</text>
<line x1="104" y1="36" x2="122" y2="36" stroke-width="1.2" stroke="currentColor"/>
<polygon points="122.0,36.0 115.0,39.2 115.0,32.8" fill="currentColor" stroke-width="0.5" stroke="currentColor"/>
<line x1="218" y1="36" x2="236" y2="36" stroke-width="1.2" stroke="currentColor"/>
<polygon points="236.0,36.0 229.0,39.2 229.0,32.8" fill="currentColor" stroke-width="0.5" stroke="currentColor"/>
<line x1="284" y1="58" x2="284" y2="76" stroke-width="1.2" stroke="currentColor"/>
<line x1="284" y1="76" x2="56" y2="76" stroke-width="1.2" stroke="currentColor"/>
<line x1="56" y1="76" x2="56" y2="60" stroke-width="1.2" stroke="currentColor"/>
<polygon points="56.0,60.0 59.2,67.0 52.8,67.0" fill="currentColor" stroke-width="0.5" stroke="currentColor"/>
<text x="170" y="94" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">接回上下文，再预测下一个</text>
<line x1="8" y1="106" x2="332" y2="106" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<text x="8" y="124" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Temperature 越小，分布越尖</text>
<text x="8" y="142" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">三个候选分数 2、0、0，「好」的概率：</text>
<text x="8" y="168" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">T=0.2</text>
<rect x="58" y="158" width="220.0" height="12" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="283.95" y="168" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">99.99%</text>
<text x="8" y="198" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">T=1</text>
<rect x="58" y="188" width="173.1" height="12" rx="0" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="237.107" y="198" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">78.70%</text>
<text x="8" y="228" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">T=1.5</text>
<rect x="58" y="218" width="144.1" height="12" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="208.025" y="228" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">65.48%</text>
<line x1="8" y1="232" x2="332" y2="232" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<text x="8" y="250" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">T=0 也不保证逐字相同：版本更新、</text>
<text x="8" y="268" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">跨区域部署、并行计算都会变</text>
</svg>
上半部分是接龙循环：每次生成的 Token 立刻接回上下文；下半部分是同一组分数（2、0、0）下，温度越低，「好」被选中的概率越接近 100%。
**容易错。**
- **以为窗口越大效果越好：** 放得进去不等于用得好，更贵，也更容易漏掉埋在中间的信息。
- **以为温度 0 就完全确定：** 只是倾向选概率最高的 Token，版本更新、跨区域部署、并行计算都会让结果略有不同，`seed` 只能尽力复现。
- **以为模型在查事实库：** 它在预测像样的下一个 Token，缺知识时也会流畅地编，所以需要 RAG、校验和允许拒答。
- **以为 Token 等于字：** 英文约 3 到 4 个字符一个 Token，中文约 1 到 2 个汉字，精确值读 API 返回的 `usage`。
- **以为多轮对话成本是常数：** 每一轮都要重发历史，单轮成本随历史长度线性上升。

