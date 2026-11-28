---
id: bagu-rag-pipeline-1-rag-vs-finetune
node: a.agent.rag-pipeline
type: qa
step: 1
---
## Q
**RAG · 什么时候用 RAG，什么时候微调**｜必会

面试官：「公司的商户服务规则经常改，做智能问答，你是用 RAG 还是微调模型？」

## A
**基本回答。** RAG（Retrieval-Augmented Generation，检索增强生成）是回答之前先去资料库检索出相关片段，连同问题一起交给模型，解决模型缺少外部知识或最新知识的问题；微调（Fine-tuning）改的是模型自己的参数，解决的是语气、输出格式或指令遵循不稳的问题。知识会变、要给出处、要按权限过滤，用 RAG；要稳定的风格和输出格式，用微调；两者可以配合。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">RAG：开卷考试</text>
<rect x="8" y="26" width="64" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="40.0" y="48.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">用户问题</text>
<line x1="72" y1="44" x2="93.0" y2="44.0" stroke="currentColor" stroke-width="1.2"/>
<polygon points="100,44 93.0,47.2 93.0,40.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="100" y="26" width="104" height="36" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="152.0" y="48.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">检索资料片段</text>
<line x1="204" y1="44" x2="221.0" y2="44.0" stroke="currentColor" stroke-width="1.2"/>
<polygon points="228,44 221.0,47.2 221.0,40.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="228" y="26" width="104" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="280.0" y="48.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">模型照资料答</text>
<text x="8" y="84" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">规则改了：只更新索引；答案能附条款出处</text>
<text x="8" y="126" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">微调：闭卷背诵</text>
<rect x="8" y="136" width="70" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="43.0" y="158.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">规则改了</text>
<line x1="78" y1="154" x2="89.0" y2="154.0" stroke="currentColor" stroke-width="1.2"/>
<polygon points="96,154 89.0,157.2 89.0,150.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="96" y="136" width="124" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="158.0" y="158.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">重新训练并评测</text>
<line x1="220" y1="154" x2="231.0" y2="154.0" stroke="currentColor" stroke-width="1.2"/>
<polygon points="238,154 231.0,157.2 231.0,150.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="238" y="136" width="94" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="285.0" y="158.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">新模型参数</text>
<text x="8" y="194" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">更新慢，可能张冠李戴，给不出出处</text>
<text x="8" y="224" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">知识会变用 RAG，风格格式用微调</text>
</svg>
上半是 RAG：每次回答前先翻资料，规则变了只动资料；下半是微调：规则变了就要重训、重评。
**容易错。**
- **以为微调能让模型学会新知识：** 微调更适合改风格和格式；会变的事实放在检索里，更新才便宜、可核对。
- **以为长上下文够大就不用 RAG：** 窗口再大也放不下整个知识库，全量输入又贵又慢，权限隔离也做不了。
- **以为 RAG 和微调二选一：**两者解决的问题不同，可以配合：RAG 管知识，微调管风格和格式；先把 RAG 链路和评测集搭稳，确认剩下的痛点是风格或指令遵循，再考虑微调。
**业务场景。** 商户退款规则每周更新：用 RAG，改完规则重建索引，回答附条款出处；若靠微调，每改一次规则就要重训一轮。
