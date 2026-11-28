---
id: bagu-memory-4-million-recall
node: a.agent.memory
type: qa
step: 4
---
## Q
**百万条记忆 · 召回链路怎么设计**｜追问

面试官：「一个用户积累了上百万条记忆，每次对话怎么快速找到相关的几条？」

## A
**基本回答。** 不能全量比对，要做成多级漏斗。第一步按用户 ID（以及类型、时间）硬过滤，把范围缩到这个用户。第二步向量近邻（ANN，如 HNSW，把「遍历全部」变成沿图找近邻，耗时近似对数增长）和关键词并行召回几十条候选。第三步用 RRF 融合去重，再重排到几条。第四步只把最相关的几条放进上下文，设数量和 Token 上限。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<rect x="10" y="4" width="320" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="25.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">这个用户的上百万条记忆</text>
<rect x="20" y="54" width="300" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="75.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① 按用户 ID（类型、时间）硬过滤</text>
<rect x="40" y="104" width="260" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="120.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② ANN + 关键词并行召回</text>
<text x="170.0" y="135.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">各取几十条候选</text>
<rect x="60" y="160" width="220" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="181.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ RRF 融合去重，再重排</text>
<rect x="80" y="210" width="180" height="36" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="224.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">④ 只放最相关的几条</text>
<text x="170.0" y="239.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">设数量和 Token 上限</text>
<line x1="170" y1="38" x2="170.0" y2="48.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,54.0 167.0,48.0 173.0,48.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="170" y1="88" x2="170.0" y2="98.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,104.0 167.0,98.0 173.0,98.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="170" y1="144" x2="170.0" y2="154.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,160.0 167.0,154.0 173.0,154.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="170" y1="194" x2="170.0" y2="204.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,210.0 167.0,204.0 173.0,204.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
</svg>
每一层都把候选缩小一截：从上百万，到这个用户的，到几十条，到几条。
**容易错。**
- **把全部记忆塞给模型：**上下文被撑爆，关键信息被稀释，也更贵更慢。
- **以为过滤越严越好：**过滤太强会让图的可达路径变少，召回率下降，要在过滤后测召回。
- **以为 ANN 是精确结果：**它是近似的，可能漏掉真正最近的，要实测召回率。
- **不管向量检索的延迟：**它的 P99 会直接加到首包延迟上；浅层偏好（地址、常用设置）开会话时预载入缓存，深度记忆异步召回，并限制候选数。

**业务场景。** 老用户有大量历史对话，新会话开头只取回 3 条：最近地址、常用支付方式、收货时间偏好，其余不进上下文。
