---
id: bagu-es-inverted-index-1-index-write-query
node: b.search.es-inverted-index
type: qa
step: 1
---
## Q
**Elasticsearch · 倒排索引、mapping 与读写流程**｜追问

面试官：「ES 的倒排索引是什么，为什么搜索快？一条数据写进去多久能搜到？一次搜索是怎么执行的？」

## A
**基本回答。** 倒排索引是「词到文档列表」的映射：写入时分词，每个词记录出现在哪些文档；搜索时查词典拿列表，多个词取交集或并集，不用扫全部文档。写入路径：协调节点按路由（默认 `_id` 哈希）转给主分片，主分片写完同步副本才返回；先写内存 buffer 和 translog，每 1 秒（`index.refresh_interval`）refresh 成新 segment，进入操作系统缓存后才可搜，所以是准实时（长时间无搜索的分片默认 30 秒后跳过后台 refresh）。translog 默认每请求 fsync（`durability=request`），断电不丢已确认写入；flush 时提交 segment 并清空 translog。搜索分两阶段：query 每个分片返回匹配的文档 ID 和排序值，协调节点合并；fetch 再按 ID 取完整文档；深分页每个分片要多取很多，成本高。mapping：`text` 分词用于全文检索，`keyword` 不分词用于精确过滤、排序、聚合；两种都要用 `text` 加 `keyword` 子字段，不要照搬 MySQL 类型。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 232">
<text x="6" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">文档（已分词）</text>
<text x="176" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">倒排索引：词 → 文档列表</text>
<rect x="6" y="24" width="130" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="71" y="41" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">D1：红色 连衣裙</text>
<rect x="6" y="56" width="130" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="71" y="73" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">D2：红色 T恤</text>
<rect x="6" y="88" width="130" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="71" y="105" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">D3：蓝色 连衣裙</text>
<line x1="138" y1="74" x2="163.0" y2="74.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,74 163.0,77.2 163.0,70.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="176" y="24" width="64" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="208" y="41" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">红色</text>
<line x1="240" y1="37" x2="243.0" y2="37.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="250,37 243.0,40.2 243.0,33.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="250" y="24" width="84" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="292" y="41" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">D1, D2</text>
<rect x="176" y="56" width="64" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="208" y="73" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">蓝色</text>
<line x1="240" y1="69" x2="243.0" y2="69.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="250,69 243.0,72.2 243.0,65.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="250" y="56" width="84" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="292" y="73" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">D3</text>
<rect x="176" y="88" width="64" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="208" y="105" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">连衣裙</text>
<line x1="240" y1="101" x2="243.0" y2="101.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="250,101 243.0,104.2 243.0,97.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="250" y="88" width="84" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="292" y="105" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">D1, D3</text>
<rect x="176" y="120" width="64" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="208" y="137" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">T恤</text>
<line x1="240" y1="133" x2="243.0" y2="133.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="250,133 243.0,136.2 243.0,129.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="250" y="120" width="84" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="292" y="137" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">D2</text>
<text x="6" y="172" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">搜「红色 连衣裙」：</text>
<text x="6" y="190" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">取两个词的文档列表交集 → D1</text>
<text x="6" y="214" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不用扫描全部文档，只查词典拿列表</text>
</svg>
左边是三篇文档，右边是倒过来的词典；搜两个词就是取两条列表的交集。
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="6" y="6" width="328" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="21.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">协调节点收到写请求</text>
<text x="170" y="36.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">按路由（默认 _id 哈希）找主分片</text>
<line x1="170" y1="44" x2="170.0" y2="49.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,56 166.8,49.0 173.2,49.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="56" width="328" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="71.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">主分片写内存 buffer 和 translog</text>
<text x="170" y="86.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">translog 默认每请求 fsync</text>
<line x1="170" y1="94" x2="170.0" y2="99.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,106 166.8,99.0 173.2,99.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="106" width="328" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="121.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">同步给副本分片</text>
<text x="170" y="136.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">都完成才返回成功</text>
<line x1="170" y1="144" x2="170.0" y2="149.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,156 166.8,149.0 173.2,149.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="156" width="328" height="38" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="171.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">每 1 秒 refresh</text>
<text x="170" y="186.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">buffer 变成新 segment，进 OS 缓存，才可搜</text>
<line x1="170" y1="194" x2="170.0" y2="199.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,206 166.8,199.0 173.2,199.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="206" width="328" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="221.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">flush：提交 segment，清空 translog</text>
<text x="170" y="236.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">后台还会合并小 segment</text>
</svg>
一次写入从上到下走：蓝色那一步之后，新写的数据才能被搜到，所以是准实时。
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 178">
<rect x="100" y="6" width="140" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="23" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">协调节点</text>
<rect x="6" y="76" width="100" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="56" y="93" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">分片 1</text>
<line x1="170" y1="32" x2="62.5" y2="73.5" stroke-width="1.2" stroke="currentColor"/>
<polygon points="56,76 61.4,70.5 63.7,76.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="120" y="76" width="100" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="93" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">分片 2</text>
<line x1="170" y1="32" x2="170.0" y2="69.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,76 166.8,69.0 173.2,69.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="234" y="76" width="100" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="284" y="93" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">分片 3</text>
<line x1="170" y1="32" x2="277.5" y2="73.5" stroke-width="1.2" stroke="currentColor"/>
<polygon points="284,76 276.3,76.5 278.6,70.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="6" y="126" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">① query：各分片返回匹配的文档 ID 和排序值</text>
<text x="6" y="144" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">② 协调节点合并排序，选出最终的那几个 ID</text>
<text x="6" y="162" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">③ fetch：按 ID 去分片取完整文档</text>
</svg>
一次搜索分两阶段：先拿 ID 和排序值，合并后再取完整文档。
**举个例子。** D1「红色 连衣裙」、D2「红色 T恤」、D3「蓝色 连衣裙」：红色 → D1、D2，连衣裙 → D1、D3，搜「红色 连衣裙」取交集得 D1，没碰 D2、D3 的内容。mapping 坑：品牌「Air Jordan」映射成 `text` 存成 air、jordan，按整个品牌名精确过滤匹配不到，改 `keyword` 才行。深分页：`from` 9990、`size` 10，每个分片都要返回自己的前 10000 条 ID 和排序值，协调节点合并后丢掉大部分。
**容易错。**
- **以为写入成功就立刻能搜到：** 要等 refresh。
- **用 text 字段做精确过滤：** 存的是分词后的词。
