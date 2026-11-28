---
id: bagu-hot-key-4-cluster-slot
node: a.cache.hot-key
type: qa
step: 4
---
## Q
**热 key · Cluster 单槽、读从库与限流**｜追问

面试官：「Cluster 里这个槽已经是单点瓶颈，读从库和代理层探测分别起什么作用？还有什么兜底？」

## A
**基本回答。** 三层配合：读写分离，热 key 的读走从库副本，分摊主节点的压力；代理层统计访问，自动识别热 key，再触发本地缓存或副本；最后用限流与降级兜底，保护节点不被拖垮。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 256">
<rect x="8" y="12" width="324" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="31.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">代理层：看得到全部流量，按 key 计数</text>
<line x1="58" y1="42" x2="58" y2="96" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="58.0,96.0 54.8,89.0 61.2,89.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="66" y="76" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">写</text>
<line x1="170" y1="42" x2="170" y2="96" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,96.0 166.8,89.0 173.2,89.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="178" y="76" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">读</text>
<line x1="282" y1="42" x2="282" y2="96" stroke-width="1.2" stroke="currentColor"/>
<polygon points="282.0,96.0 278.8,89.0 285.2,89.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="290" y="76" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">读</text>
<rect x="8" y="98" width="100" height="50" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="58.0" y="119.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">主节点</text>
<text x="58.0" y="134.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读 + 写</text>
<rect x="120" y="98" width="100" height="50" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="119.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">从库 1</text>
<text x="170.0" y="134.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只读</text>
<rect x="232" y="98" width="100" height="50" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="282.0" y="119.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">从库 2</text>
<text x="282.0" y="134.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只读</text>
<line x1="108" y1="123" x2="120" y2="123" stroke-width="1.2" stroke-dasharray="4 3" stroke="currentColor"/>
<polygon points="120.0,123.0 113.0,126.2 113.0,119.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="170" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同一个槽的副本数据相同，读可以摊开</text>
<text x="8" y="188" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">写只能落在主节点，写热点要另想办法</text>
<rect x="8" y="204" width="324" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="170.0" y="218.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">最后一道：限流 + 降级</text>
<text x="170.0" y="233.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">宁可返回旧数据或默认值</text>
</svg>
代理在最前面看全部流量；写只能走主节点（粗箭头），读可以分给两个从库；整个槽扛不住时，最底下这道限流加降级兜底。
**容易错。**
- **以为读写分离能解决所有热点：** 它只能分摊读；写热点不行，一主两从只是把读摊成三份，一份仍超过单节点 8 到 10 万 QPS 就还要配本地缓存或副本。
- **忽略复制延迟：** 从库读到的值可能是旧的，一致性要求高的字段要读主。
- **每个客户端各自统计热 key：** 重复劳动且名单不一致；代理统一统计再推送更省事。
- **没有最后一道防线：** 没有限流降级，突发流量会把主节点和同一分片的其他 key 一起拖垮。

**举个例子。** 热点直播间 key 每秒 50 万次读，一主两从平分每个约 16.7 万，仍高于单节点 8 到 10 万；代理发现突增后通知所有实例开几秒 TTL 的本地缓存，大部分读被吸收；仍超出的部分对该 key 限流，直接返回缓存快照或默认值，主节点和邻居 key 保持正常。
