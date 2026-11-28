---
id: hi-sdx-clustered-vs-heap
node: sd.core-concepts.db-indexing.more
type: qa
step: 1
---
## Q
**聚簇存储与堆表：索引各指向哪里**｜补充 · 数据库索引 · 追问

面试官：「InnoDB 把整行放在主键 B+ 树的叶子里，Postgres 把行放在堆文件里、所有索引都指向它。这两种布局在读和写上各赢在哪里、输在哪里？」

## A
**结论。** 聚簇布局（InnoDB）主键查找和主键范围扫描最快，代价是二级索引要查两棵树。堆表（Postgres）所有索引地位平等，没有二次下钻，代价是每次命中都要多一次回堆，更新时每个索引都可能要改。

**要点。**
- **聚簇的赢面：** 叶子就是行，主键相邻的行在磁盘上也相邻，主键点查和范围扫描只走一棵树。
- **聚簇的代价：** 二级索引存的是主键值，二级索引查询要先下钻二级索引、再用主键下钻主键树（回表）；主键越长，每个二级索引都越胖；随机主键（如 UUIDv4）让插入散落在各个叶子页，页分裂多。
- **堆表的赢面：** 索引条目指向行的物理位置（页号加页内偏移，即 TID），主键不特殊，二级索引一次到位。
- **堆表的代价：** 每次索引命中要随机读一次堆页，除非走仅索引扫描（还要借助可见性映射）；更新会在新位置写一个新版本，每个索引都要加一条指向新位置的条目。
- **缓解：** Postgres 的堆内元组更新（HOT）在被索引的列没变、新版本能放进同一页时，不用改任何索引。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 300">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">InnoDB（聚簇）</text>
<text x="178" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Postgres（堆表）</text>
<rect x="8" y="26" width="152" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="84.0" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">二级索引</text>
<text x="84.0" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">email → 主键值</text>
<rect x="8" y="110" width="152" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="84.0" y="128.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">主键 B+ 树</text>
<text x="84.0" y="143.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">叶子就是整行</text>
<polyline points="84,70 84.0,103.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="84,110 80.8,103.0 87.2,103.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="92" y="94" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">①→②</text>
<rect x="178" y="26" width="152" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="254.0" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">任一索引</text>
<text x="254.0" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">email → TID(页,偏移)</text>
<rect x="178" y="110" width="152" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="254.0" y="128.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">堆文件</text>
<text x="254.0" y="143.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">行按写入位置存放</text>
<polyline points="254,70 254.0,103.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="254,110 250.8,103.0 257.2,103.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="262" y="94" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">①→②</text>
<text x="8" y="184" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">二级索引查两棵树；</text>
<text x="8" y="202" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">主键范围扫描最快</text>
<text x="178" y="184" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每次命中回堆一次；</text>
<text x="178" y="202" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">更新写新版本，</text>
<text x="178" y="220" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">除非 HOT，每个索引都加条目</text>
<text x="8" y="262" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">聚簇：主键要短，且尽量单调</text>
<text x="8" y="280" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">堆表：别给热更新列建索引</text>
</svg>

**面试里这样说。** 「InnoDB 是聚簇索引，主键范围扫描最优，但二级索引多一次回表，主键要短且尽量单调。Postgres 是堆表，索引都指向堆位置，更新如果动了被索引的列就要改所有索引，所以不要给频繁更新的列建索引。」

**易错。**
- **用 UUIDv4 做 InnoDB 主键：** 插入随机落点，页分裂和碎片严重，所有二级索引条目都要带上 16 字节的主键。
- **给热更新列建索引：** Postgres 里 HOT 失效，每次更新写放大到所有索引。
