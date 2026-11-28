---
id: bagu-hot-key-3-replicas
node: a.cache.hot-key
type: qa
step: 3
---
## Q
**热 key · 拆成多个副本**｜追问

面试官：「本地缓存还不够，一个 key 要 50 万 QPS。把它拆成多个副本，怎么读写？更新时怎么保持一致？」

## A
**基本回答。** 把一个热 key 复制成 `key#0` 到 `key#N-1` 共 N 份，读的时候随机选一份，请求就被分散到不同的槽和不同的节点上（对整个 key 算 CRC16 再对 16384 取模，后缀不同槽就不同：`room:1001#0` 到 `#7` 落在 8 个不同的槽，原 key 只在槽 10033）；代价是写的时候要写 N 份。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 266">
<rect x="8" y="82" width="90" height="66" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="53.0" y="104.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读</text>
<text x="53.0" y="119.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">随机选</text>
<text x="53.0" y="134.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">一份</text>
<rect x="206" y="14" width="126" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="269.0" y="32.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">room:1001#0</text>
<text x="269.0" y="47.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">槽 2737 分片A</text>
<line x1="98" y1="115" x2="206" y2="36" stroke-width="1.2" stroke="currentColor"/>
<polygon points="206.0,36.0 202.2,42.7 198.5,37.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="206" y="68" width="126" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="269.0" y="86.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">room:1001#1</text>
<text x="269.0" y="101.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">槽 6800 分片B</text>
<line x1="98" y1="115" x2="206" y2="90" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="206.0,90.0 199.9,94.7 198.5,88.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="206" y="122" width="126" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="269.0" y="140.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">room:1001#2</text>
<text x="269.0" y="155.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">槽 10995 分片C</text>
<line x1="98" y1="115" x2="206" y2="144" stroke-width="1.2" stroke="currentColor"/>
<polygon points="206.0,144.0 198.4,145.3 200.1,139.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="206" y="176" width="126" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="269.0" y="194.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">room:1001#3</text>
<text x="269.0" y="209.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">槽 15058 分片C</text>
<line x1="98" y1="115" x2="206" y2="198" stroke-width="1.2" stroke="currentColor"/>
<polygon points="206.0,198.0 198.5,196.3 202.4,191.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="244" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">写：N 份都要写（或都删）</text>
<text x="8" y="262" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">后缀放在花括号外，槽才不同</text>
</svg>
左边是读请求，随机选一份；右边是同一个 key 的副本，x落在不同的槽、不同的分片（图里只画了 8 份中的前 4 份）。写则要写完全部 N 份。
**容易错。**
- **把后缀放进花括号：** hash tag 规则下花括号里的部分才参与哈希，`room:{1001}#0` 和 `#1` 都只算 `1001`，落回同一个槽，等于白拆。
- **只写一份：** 写要写 N 份，否则读到别的副本会拿到旧值或空值。
- **更新没有版本号：** 晚到的旧写入可能覆盖新值。
- **N 开太大不回收：** 副本数要按热度配置，热点消退后回收，否则白白占内存、写放大。
**举个例子。** 礼物榜 `gift:top:1001` 每秒 50 万次读，拆成 `#0` 到 `#7` 共 8 份，每份约 6.25 万 QPS（50 万 ÷ 8），只要落在足够多的分片上就低于单分片 8 到 10 万的上限。榜单更新：先写数据库，再覆盖全部 8 份，值带版本号 v8，晚到的 v7 被拒绝。
