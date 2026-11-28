---
id: bagu-bplus-tree-1-why-bplus
node: a.mysql.bplus-tree
type: qa
step: 1
---
## Q
**索引结构 · 为什么用 B+ 树，不用哈希、二叉树、红黑树**｜必会

面试官：「订单表两千万行，按用户 ID 查订单。索引为什么用 B+ 树？哈希不是 O(1) 吗，红黑树不也是 O(log N) 吗？」

## A
**基本回答。** 索引存在磁盘上，查一次的成本主要看读了几次磁盘（IO 次数），而不是比较了几次。磁盘一次读固定大小的页（InnoDB 默认 16KB），读 1 字节和读 16KB 代价几乎一样，所以好的索引要让「每次读一整页、树尽量矮」。B+ 树的非叶子节点只存键和指针，数据全放在叶子，叶子之间用双向链表连起来：一页能放上千个键，树只有三层左右。哈希只支持等值查询，没有顺序，不能范围和排序；二叉树可能退化成一条链；红黑树每个节点只有两个孩子，两千万行约 24 层，要二十多次随机 IO；B 树的非叶子也存数据，一页放不下几个键，扇出小。
哈希值无序：不支持范围、排序、最左前缀，非 `=` 只能全表扫；Memory 引擎支持哈希索引，InnoDB 的自适应哈希索引会给热点页自动建哈希，只能整体开关。找到页后靠页目录（page directory）二分，不用逐条比。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 206">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">红黑树：每个节点 2 个孩子</text>
<rect x="30" y="28" width="100" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80.0" y="44.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">第 1 层</text>
<line x1="80" y1="52" x2="80.0" y2="59.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="80.0,66.0 76.8,59.0 83.2,59.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="30" y="66" width="100" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80.0" y="82.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">第 2 层</text>
<line x1="80" y1="90" x2="80.0" y2="91.0" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<polygon points="80.0,98.0 76.8,91.0 83.2,91.0" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<text x="80" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">…</text>
<line x1="80" y1="116" x2="80.0" y2="121.0" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<polygon points="80.0,128.0 76.8,121.0 83.2,121.0" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<rect x="30" y="128" width="100" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80.0" y="144.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">第 24 层</text>
<text x="8" y="176" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">两千万行约 24 层</text>
<text x="8" y="194" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">要 20 多次随机 IO</text>
<text x="178" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">B+ 树：一页一个节点</text>
<rect x="190" y="28" width="130" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="255.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">根页（常驻内存）</text>
<line x1="255" y1="54" x2="255.0" y2="69.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="255.0,76.0 251.8,69.0 258.2,69.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="263" y="70" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">扇出约 1000</text>
<rect x="190" y="76" width="130" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="255.0" y="93.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">第二层（几乎常驻）</text>
<line x1="255" y1="102" x2="255.0" y2="117.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="255.0,124.0 251.8,117.0 258.2,117.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="190" y="124" width="130" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="255.0" y="141.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">叶子页（读 1 次）</text>
<text x="178" y="176" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">3 层，最多 3 次 IO</text>
<text x="178" y="194" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">常常只读 1 次叶子</text>
</svg>
左边红黑树每个节点只有两个孩子，两千万行要 24 层；右边 B+ 树一页一个节点、扇出上千，只要 3 层，而且前两层常驻内存。
**举个例子。** 订单表两千万行，按 `user_id` 查订单：
1. **根页：** 常驻缓冲池（buffer pool，InnoDB 缓存数据页的内存），不用读盘。
2. **第二层：** 页数不多，几乎总在缓冲池里，也基本不读盘。
3. **叶子页：** 读 1 次磁盘，拿到记录。所以最坏 3 次 IO，实际常常只读 1 次叶子页。
4. **红黑树对比：** 同样的数据要沿 24 层往下走，每层都可能是一次随机 IO，二十多次。
5. **范围条件：** 查「最近 7 天订单」，B+ 树找到起点后沿叶子链表往后读；哈希索引没有顺序，完全用不上。
**容易错。**
- **以为哈希 O(1) 一定最快：** 它只赢在等值查询；业务里范围、排序、最左前缀很常见，哈希都做不到。
- **以为红黑树 O(log N) 就够好：** 比较次数少，但内存结构每个节点是单独一块，放到磁盘上每一层都可能是一次 IO，层数才是成本。
- **以为 InnoDB 完全不用哈希：** 它有自适应哈希索引，只是你不能指定，只能整体开关。
- **以为树高只和行数有关：** 还取决于扇出，键越短、一页放得越多，树越矮。
