---
id: hi-sdx-sg-mutual-friends
node: more.social-graph
type: qa
step: 2
---
## Q
**共同好友要碰几个分片**｜补充 · 社交图谱与好友搜索 · 必会

面试官：「边按用户 ID 哈希分片，一个人的 300 个好友散落在很多分片上。查 A 和 B 的共同好友要访问多少个分片？如果 B 是一个有几万个连接的公众账号呢？」

## A
**结论。** 只访问两个分片：A 的完整邻接表在 A 所在分片，B 的在 B 所在分片，各读一次，在本地求交集。公众账号的邻接表太大时，别把它整个拉过来，拿 A 的短列表去它的索引里逐个探测。

**要点。**
- **为什么是两个：** 边按源点分片，一个用户的全部边都在自己那一个分片上，查询涉及几个用户就碰几个分片。
- **与分片总数无关：** 好友们散落在多少个分片都无所谓，我们不需要去读好友的邻接表。
- **本地求交：** 两个约 300 条的有序列表，几百次比较。
- **对比：** 好友的好友候选要读 300 个好友各自的邻接表，扇出到几乎所有分片。
- **高度数节点：** 公众账号有几万条边，整表读取很贵；遍历较短的列表，对大账号的（类型, 源点, 目标）做点查，成本随短列表长度走。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="10" y="8" width="150" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="85.0" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A 的邻接表</text>
<text x="85.0" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">分片 3 一次读取</text>
<rect x="180" y="8" width="150" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="255.0" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B 的邻接表</text>
<text x="255.0" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">分片 7 一次读取</text>
<polyline points="85,48 144.0,82.5" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="150,86 142.3,85.2 145.6,79.7" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="255,48 196.0,82.5" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="190,86 194.4,79.7 197.7,85.2" style="fill:var(--accent,#3b6fd4)"/>
<rect x="90" y="86" width="160" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="102.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">本地求交</text>
<text x="170.0" y="117.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">约 300 × 2 次比较</text>
<polyline points="170,126 170.0,141.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,148 166.8,141.0 173.2,141.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="90" y="148" width="160" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="169.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">共同好友</text>
<text x="10" y="210" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只涉及 2 个用户，所以只碰 2 个分片，</text>
<text x="10" y="228" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">与总分片数无关。</text>
<text x="10" y="248" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">好友的好友候选则要扇出到很多分片。</text>
</svg>

**为什么。** 单分片查询的代价取决于查询里点名了几个用户，不取决于关系网有多大。

**面试里这样说。** 「共同好友是读 A 和 B 各自的邻接表再本地求交，只碰两个分片，与总分片数无关。如果其中一个是几万连接的公众账号，我遍历 A 的短列表，对它的边做点查，不整表拉取。」

**易错。**
- **以为要扫所有好友的分片：** 那是好友的好友，不是共同好友。
- **对高度数账号整表读取：** 单次请求成本比普通用户高出许多倍，还集中在同一个分片。
- **没分页没上限：** 大账号的边列表要分页读取，必要时限制展示上限。
