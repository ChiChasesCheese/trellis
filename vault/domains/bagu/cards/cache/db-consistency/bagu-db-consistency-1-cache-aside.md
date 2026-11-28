---
id: bagu-db-consistency-1-cache-aside
node: a.cache.db-consistency
type: qa
step: 1
---
## Q
**缓存一致性 · 旁路缓存的读写流程**｜必会

面试官：「商品详情用了 Redis，说说旁路缓存（cache-aside）的读写流程。写的时候为什么删缓存，而不是更新缓存？」

## A
**基本回答。** 旁路缓存（cache-aside）由应用自己管缓存。读：先读缓存，命中直接返回；没有再读数据库，把结果回填到缓存并设置 TTL（过期时间）。写：先更新数据库，再删除缓存，让下一次读时重新构建。写的时候删缓存而不是更新缓存，原因有两个：缓存里的值常常由多张表算出来，每写一次就重算很浪费，写完也可能根本没人读，删除是惰性的；更重要的是，两个并发更新在缓存上的执行顺序可能和在数据库上相反，更新缓存会留下旧值，删除没有这个问题。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 244">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">读</text>
<text x="182" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">写</text>
<rect x="8" y="18" width="150" height="36" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="83" y="32.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读缓存</text>
<text x="83" y="47.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">命中就返回</text>
<rect x="8" y="76" width="150" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83" y="94" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">未命中：读数据库</text>
<rect x="8" y="130" width="150" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83" y="148" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">回填缓存，设 TTL</text>
<line x1="83" y1="54" x2="83" y2="70" stroke-width="1.2" stroke="currentColor"/>
<polygon points="83.0,76.0 79.8,69.0 86.2,69.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="83" y1="104" x2="83" y2="124" stroke-width="1.2" stroke="currentColor"/>
<polygon points="83.0,130.0 79.8,123.0 86.2,123.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="88" y="68" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">没有</text>
<rect x="182" y="22" width="150" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="257" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① 先更新数据库</text>
<rect x="182" y="76" width="150" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="257" y="94" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② 再删除缓存</text>
<line x1="257" y1="50" x2="257" y2="70" stroke-width="1.2" stroke="currentColor"/>
<polygon points="257.0,76.0 253.8,69.0 260.2,69.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="182" y="130" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">下次读未命中</text>
<text x="182" y="148" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">时重建缓存</text>
<text x="8" y="186" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">删除是惰性的：用到时才重建</text>
<text x="8" y="204" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">更新缓存会因并发顺序错留下旧值</text>
<text x="8" y="222" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">写回、读穿、写穿是其他模式</text>
</svg>
左边是读路径：缓存命中就返回，未命中读库后回填。右边是写路径，只有两步：先更新库，再删缓存，之后由下一次读负责把缓存重建出来。
**容易错。**
- **以为写时应该更新缓存：** 缓存值常由多表计算，重算浪费，而且并发下更新缓存会留下旧值，删除才安全。
- **回填时不设 TTL：** TTL 是最后的兜底，没有它，一次漏删的旧值会一直留着。
- **把写回当通用方案：** 写回会丢未落库的数据，只适合计数、浏览量这类能容忍丢失的数据。
- **以为删了就强一致：** 更新库和删缓存是两步，中间仍有窗口，读者可能读到旧缓存；两步中途失败也会留下旧值，要靠重试和 TTL 兜底。
- **其他读写模式：** 读穿（read-through）和写穿（write-through）把逻辑放进缓存层，应用只和缓存打交道；写回（write-behind）先写缓存、再异步落库，吞吐高，但缓存节点在落库前宕机，这部分未落库的数据就丢了。互联网业务以 cache-aside 为主。

