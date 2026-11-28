---
id: hi-sdx-prox-index-swap-fallback
node: sd.problem-breakdowns.yelp.more
type: qa
step: 3
---
## Q
**索引重建失败时怎么降级**｜补充 · 商户点评（Yelp） · 追问

面试官：「内存里的空间索引定期重建，并用双缓冲换入。某次重建失败了，你是返回错误，是直接扫商户数据库，还是继续用旧索引？为什么？」

## A
**结论。** 继续用上一份已加载成功的快照。双缓冲下，旧快照在新快照构建、校验完成并原子换入之前不会被丢弃，重建失败只是换入没有发生，搜索照常、全速服务，数据只是旧了几分钟。

**要点。**
- **返回错误最差：** 内存里明明有可用的旧快照，却让整个搜索停服。
- **直接扫库也不行：** 把内存里的毫秒级查找换成对千万行的无保护扫描，会拖垮数据库，连带影响商户写入和索引构建器自己，形成级联故障。
- **换入的流程：** 后台构建新索引，校验（条数、抽样查询），通过后原子地切换指针，旧快照在没有请求引用后才释放。
- **要有监控：** 对重建失败次数和快照年龄告警，年龄超过几个重建周期就要人工介入，否则数据会悄悄一直旧下去。

**为什么。** 邻近搜索本来就容忍几分钟的陈旧：商户信息变化很慢。所以用可用性换一点新鲜度是划算的，而用数据库兜底把容量问题转嫁给了不该承担它的存储。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<rect x="20" y="16" width="130" height="56" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="85" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">当前快照 v41</text>
<text x="85" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">服务中</text>
<rect x="190" y="16" width="130" height="56" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="255" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">新快照 v42</text>
<text x="255" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">后台构建</text>
<rect x="190" y="100" width="130" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="255" y="116.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">校验</text>
<text x="255" y="131.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">条数、抽样查询</text>
<polyline points="255,72 255,100" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="255,100 251.8,93.0 258.2,93.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<polyline points="190,120 85,120 85,72" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="85,72 88.2,79.0 81.8,79.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="96" y="112" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">通过后换指针</text>
<text x="8" y="170" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">失败：不换入，v41 继续服务</text>
<text x="8" y="188" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">数据只旧几分钟，并对快照年龄告警</text>
</svg>

**面试里这样说。** 「重建失败我不换入，继续用上一份已验证的快照，搜索不受影响，只是数据旧几分钟。不会返回错误，也不会回退到扫库，那会把数据库压垮。同时对快照年龄告警，超过几个周期就报警。」

**易错。**
- **换入前不校验：** 一份坏索引被原子换上线，比重建失败更糟。
- **只降级不告警：** 快照一直不更新，没人知道。
