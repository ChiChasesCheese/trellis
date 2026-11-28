---
id: hi-sdx-news-incremental-cluster
node: sd.problem-breakdowns.google-news.more
type: qa
step: 2
---
## Q
**增量归簇还是定期重聚类**｜补充 · 新闻聚合（Google News） · 追问

面试官：「同一条突发新闻，几十家媒体几分钟内先后发稿。聚类是定期对全部活跃文章重新跑一遍，还是每篇新文章到达时增量归簇？各有什么代价？」

## A
**结论。** 增量归簇。每篇文章到达时，用它的指纹去近似重复索引里查一次，命中就并入已有的簇，没有命中就新建簇。批量重聚类会让同一事件的多家报道，在整个批窗口里一直是互不相干的故事，而这恰恰是突发新闻流量最高的时刻。代价是两个早期各自建立的簇，之后才发现是同一事件，会暂时分开，由后台任务定期合并。

**要点。**
- **批量的问题：** 两家媒体在同一个批窗口内报道同一事件，要等到下一次重聚类才合并，期间信息流里是两个故事。
- **增量归簇：** 一次索引查找就完成归簇，故事马上开始被佐证、被排名。
- **暂时的不一致：** 两篇几乎同时到达的文章，可能各自建了新簇，彼此还没看到对方。
- **后台合并：** 定期扫描相互靠近的簇，把小簇并入大簇，更新文章的簇 ID，重算佐证数，并保留旧簇 ID 到新簇的重定向，避免缓存里的链接失效。
- **取舍：** 接受有界、可便宜修复的短暂分裂，换取不用等整批结果确认。

**为什么。** 突发事件对延迟最敏感，而聚类的少量暂时错误能事后修正。把「立刻可见」放在「绝对一致」之前是合理的。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 210">
<rect x="20" y="10" width="300" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="26.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">文章 A 到达</text>
<text x="170" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">索引无匹配，新建簇 C1</text>
<rect x="20" y="76" width="300" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="92.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">文章 B 到达（A 的指纹尚未可查）</text>
<text x="170" y="107.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">也新建簇 C2</text>
<rect x="20" y="142" width="300" height="56" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="159" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">后台合并任务</text>
<text x="170" y="174" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">发现 C1、C2 是同一事件</text>
<text x="170" y="189" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">合并，保留 C2 → C1 的重定向</text>
<polyline points="170,50 170,76" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="170,76 166.8,69.0 173.2,69.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="170,116 170,142" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,142 166.8,135.0 173.2,135.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
</svg>

**面试里这样说。** 「我做增量归簇：文章一到就查指纹索引，命中并入，没命中新建。两个早期簇可能暂时没合并，我用后台任务定期合并，并保留旧簇 ID 的重定向。这样突发新闻不用等下一次批量重聚类。」

**易错。**
- **只靠批量重聚类：** 突发新闻要等一个完整批窗口才合并。
- **合并时丢了佐证数：** 合并后要重新计算，否则分数偏低。
