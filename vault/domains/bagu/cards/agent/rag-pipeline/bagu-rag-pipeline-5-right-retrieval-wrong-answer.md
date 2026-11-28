---
id: bagu-rag-pipeline-5-right-retrieval-wrong-answer
node: a.agent.rag-pipeline
type: qa
step: 5
---
## Q
**排查 · 检索结果对但回答错，怎么定位**｜必会

面试官：「RAG 答非所问，你确认过检索回来的内容是对的，接下来怎么定位？」

## A
**基本回答。** 按链路逐段判断，每次只改一个变量：
1. 正确证据进候选池了吗？没有，查解析、Chunk、过滤和召回。
2. 在候选池里但排名靠后？查 Rerank。
3. 排名靠前却没进最终上下文？查 `top_n`、截断、相邻块合并。
4. 上下文正确、答案仍错：查提示词是否要求依据上下文，上下文里有没有互相冲突的版本，证据是否被埋在中间位置。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 300">
<rect x="8" y="8" width="150" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83.0" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">正确证据</text>
<text x="83.0" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">进候选池了吗？</text>
<line x1="158" y1="28" x2="171.0" y2="28.0" stroke="currentColor" stroke-width="1.2"/>
<polygon points="178,28 171.0,31.2 171.0,24.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="178" y="8" width="154" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="255.0" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">没进：查解析、</text>
<text x="255.0" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Chunk、过滤、召回</text>
<line x1="83" y1="48" x2="83.0" y2="59.0" stroke="currentColor" stroke-width="1.2"/>
<polygon points="83,66 79.8,59.0 86.2,59.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="66" width="150" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83.0" y="82.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">在池里，但</text>
<text x="83.0" y="97.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">排名靠后？</text>
<line x1="158" y1="86" x2="171.0" y2="86.0" stroke="currentColor" stroke-width="1.2"/>
<polygon points="178,86 171.0,89.2 171.0,82.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="178" y="66" width="154" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="255.0" y="82.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">查 Rerank</text>
<text x="255.0" y="97.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">（输入有没有被截断）</text>
<line x1="83" y1="106" x2="83.0" y2="117.0" stroke="currentColor" stroke-width="1.2"/>
<polygon points="83,124 79.8,117.0 86.2,117.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="124" width="150" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83.0" y="140.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">排名靠前，</text>
<text x="83.0" y="155.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">却没进上下文？</text>
<line x1="158" y1="144" x2="171.0" y2="144.0" stroke="currentColor" stroke-width="1.2"/>
<polygon points="178,144 171.0,147.2 171.0,140.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="178" y="124" width="154" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="255.0" y="140.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">查 top_n、截断、</text>
<text x="255.0" y="155.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">相邻块合并</text>
<line x1="83" y1="164" x2="83.0" y2="175.0" stroke="currentColor" stroke-width="1.2"/>
<polygon points="83,182 79.8,175.0 86.2,175.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="182" width="150" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="83.0" y="198.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">上下文正确，</text>
<text x="83.0" y="213.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">答案仍错？</text>
<line x1="158" y1="202" x2="171.0" y2="202.0" stroke="currentColor" stroke-width="1.2"/>
<polygon points="178,202 171.0,205.2 171.0,198.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="178" y="182" width="154" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="255.0" y="198.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">查提示词、冲突版本、</text>
<text x="255.0" y="213.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">证据被埋在中间</text>
<text x="8" y="252" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">从上往下，哪一段先出问题就修哪一段</text>
<rect x="8" y="262" width="324" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="280.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">每次只改一个变量</text>
</svg>
从上往下四站：入池、排序、进上下文、生成；左边是要问的问题，右边是不满足时查什么。
**容易错。**
- **看到答错就先改提示词或换模型：** 不知道哪一站出的错，改了也无法归因。
- **以为检索对了生成就一定对：** 证据被埋在中间、新旧版冲突、提示词没要求依据上下文，都会让答案错。
- **一次改多个变量：** 同时改提示词、模型和检索参数，就分不清是谁起了作用。
- **完全信任 LLM 评审：** 它只是辅助信号，要抽样人工复核。
- **指标混在一起看：**Hit Rate、MRR 看召回排序；Faithfulness（答案是否忠于上下文）、Answer Relevancy（是否切题）看生成。
**业务场景。** 用户问「退款时限多久」，答「7 到 15 天」，既不是旧规则也不是新规则：新旧两版都入池（新版第 1、旧版第 3），`top_n` 取 5 两版都进了上下文，模型把冲突的两个时限综合成一个错误时限。按版本元数据只保留生效版，并加入回归样例。
