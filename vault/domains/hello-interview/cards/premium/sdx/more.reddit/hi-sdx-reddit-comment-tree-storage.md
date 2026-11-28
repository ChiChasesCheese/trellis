---
id: hi-sdx-reddit-comment-tree-storage
node: more.reddit
type: qa
step: 2
---
## Q
**楼中楼评论：邻接表还是闭包表**｜补充 · 论坛与楼中楼评论（Reddit） · 必会

面试官：「论坛评论是一棵很深的树，最常见的读取是『取某条评论下按分数排序的一页子评论』。你用只存父指针的邻接表，还是存下所有祖先后代对的闭包表？」

## A
**结论。** 用邻接表：每行一个 parentId，加 (parentId, score) 的复合索引。闭包表让整棵子树查询很快，但插入要写祖先数那么多行，而这个负载里很少需要整棵子树。

**要点。**
- **邻接表的主查询：** (parentId, score) 索引按分数取一页直接子评论，代价约为 O(log N + K)，K 是页大小。
- **闭包表的写放大：** 每插入一条评论，要为它的每个祖先各写一行；50000 条评论、平均深度 6，约 30 万行，是邻接表 5 万行的 6 倍。
- **闭包表的收益：** 一次查询取出整棵子树，但这个读取模式在这里很少用。
- **深层折叠怎么办：** 「继续查看这个讨论」按需用递归查询限深度取一层，不为它长期付写成本。
- **移动子树：** 评论树很少需要移动，邻接表也只改一行。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<text x="10" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">插入一条深度为 3 的新评论 C：</text>
<rect x="10" y="28" width="60" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="40.0" y="47.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">根</text>
<polyline points="70,43 83.0,43.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="90,43 83.0,46.2 83.0,39.8" style="fill:var(--accent,#3b6fd4)"/>
<rect x="90" y="28" width="60" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="120.0" y="47.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B</text>
<polyline points="150,43 163.0,43.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,43 163.0,46.2 163.0,39.8" style="fill:var(--accent,#3b6fd4)"/>
<rect x="170" y="28" width="60" height="30" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="200.0" y="47.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C 新</text>
<rect x="10" y="84" width="150" height="70" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="85.0" y="100.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">邻接表</text>
<text x="85.0" y="115.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">写 1 行</text>
<text x="85.0" y="130.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">(C, parentId=B)</text>
<text x="85.0" y="145.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">索引取一页子评论</text>
<rect x="180" y="84" width="150" height="70" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="255.0" y="100.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">闭包表</text>
<text x="255.0" y="115.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">写 3 行</text>
<text x="255.0" y="130.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">(根,C) (B,C) (C,C)</text>
<text x="255.0" y="145.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">行数随深度放大</text>
<text x="10" y="184" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">50000 条评论、平均深度 6：</text>
<text x="10" y="202" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">邻接表 5 万行，闭包表约 30 万行</text>
<text x="10" y="226" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">常用查询是「某条评论的一页子评论」，</text>
<text x="10" y="244" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">整棵子树很少需要，不值得为它多写 6 倍</text>
</svg>

**为什么。** 表结构应该为最常见的读取优化：闭包表把成本移到每次写入，只有整棵子树查询占主导时才值得。

**面试里这样说。** 「评论树我用邻接表，parentId 加 (parentId, score) 索引，一页子评论走索引范围扫描。闭包表一条评论要写深度那么多行，50000 条深度 6 就是 30 万行，换来的整棵子树查询在这里很少用，所以不选。」

**易错。**
- **只看读复杂度：** 闭包表读子树是常数，但写放大 6 倍，对写多的论坛不划算。
- **邻接表不建复合索引：** 取一页排序的子评论要全表扫描。
- **一次递归取完整棵树：** 热帖有几万条评论，应分页、折叠、限深度。
