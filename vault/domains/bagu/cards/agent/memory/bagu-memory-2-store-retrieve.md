---
id: bagu-memory-2-store-retrieve
node: a.agent.memory
type: qa
step: 2
---
## Q
**记忆存储与检索 · 向量记忆和结构化记忆怎么配合**｜必会

面试官：「记忆存向量库就够了吗？向量记忆和结构化记忆怎么配合着检索？」

## A
**基本回答。** 只存向量库不够。不同形态的记忆放不同的存储：模糊的经历和对话片段放向量库做语义召回；结构化事实（地址、偏好、套餐）放关系库或键值，按用户 ID 精确读取；需要关系推理（谁和谁、先后顺序）的放图存储。检索时向量和 BM25 关键词并行，用 RRF（每路名次取倒数相加，常用 1/(60+rank)，不依赖分数量纲，几乎不用调参；有标注数据后可改线性加权）合并，带用户 ID、时间、类型等元数据过滤，最后重排。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 240">
<rect x="4" y="4" width="104" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="56.0" y="20.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">向量库</text>
<text x="56.0" y="35.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">模糊的经历</text>
<rect x="118" y="4" width="104" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="20.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">关系库 / KV</text>
<text x="170.0" y="35.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">地址、偏好</text>
<rect x="232" y="4" width="104" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="284.0" y="20.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">图存储</text>
<text x="284.0" y="35.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">谁和谁、先后</text>
<rect x="4" y="66" width="332" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="170.0" y="83.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">过滤：用户 ID、时间、类型</text>
<rect x="14" y="112" width="140" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="84.0" y="128.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">向量检索</text>
<text x="84.0" y="143.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">语义相近</text>
<rect x="186" y="112" width="140" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="256.0" y="128.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">BM25 关键词</text>
<text x="256.0" y="143.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">型号、编号</text>
<line x1="84" y1="92" x2="84.0" y2="106.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="84.0,112.0 81.0,106.0 87.0,106.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="256" y1="92" x2="256.0" y2="106.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="256.0,112.0 253.0,106.0 259.0,106.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="60" y="170" width="220" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="187.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">RRF：按名次倒数相加</text>
<line x1="84" y1="152" x2="124.41254332176548" y2="167.81360390851694" stroke-width="1.2" stroke="currentColor"/>
<polygon points="130.0,170.0 123.3,170.6 125.5,165.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="256" y1="152" x2="215.58745667823453" y2="167.81360390851694" stroke-width="1.2" stroke="currentColor"/>
<polygon points="210.0,170.0 214.5,165.0 216.7,170.6" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="100" y="208" width="140" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="225.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">重排 → 几条</text>
<line x1="170" y1="196" x2="170.0" y2="202.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,208.0 167.0,202.0 173.0,202.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
</svg>
第一排是三种存储各放什么；其余是一次检索：先过滤，向量和关键词并行，RRF 合并，最后重排。
**容易错。**
- **以为向量库就够了：**型号、编号这类精确词，向量会召回相似但无关的内容。
- **RRF 直接把分数相加：**两路分数量纲不同，不能直接加；RRF 加的是名次的倒数。
- **靠提示词保证不串用户：**必须由数据访问层强制注入用户 ID，写入和检索都走同一层，向量库按用户做 namespace；再加测试：用 A 用户的查询去召回，断言结果里没有 B 用户的数据。
- **记忆没生效就猛改写入：**先看检索 Trace，问题常出在检索而不是写入。
**举个例子。**用户问「ABX-4421 这款耳机还在保修吗」：先按 user_id 和类型过滤；向量路召回几款相似耳机，关键词路让 `ABX-4421` 精确命中。
- 某条在向量路第 1、关键词路第 3：1/61 + 1/63 ≈ 0.0323；购买 ABX-4421 的那条向量路第 2、关键词路第 1：1/62 + 1/61 ≈ 0.0325，排到第一，重排后取几条给模型。
