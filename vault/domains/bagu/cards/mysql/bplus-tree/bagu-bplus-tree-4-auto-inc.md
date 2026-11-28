---
id: bagu-bplus-tree-4-auto-inc
node: a.mysql.bplus-tree
type: qa
step: 4
---
## Q
**主键自增 · 页分裂是怎么回事**｜追问

面试官：「主键为什么建议自增而不是 UUID？页分裂是什么，有什么问题？」

## A
**基本回答。** 自增主键总是追加在最右边那个叶子页的末尾，写满了就新开一页，不移动已有数据，页的填充率约 15/16。UUID 是随机的，新行要插进中间某个页，如果那页已满就发生页分裂（page split）：分配一个新页，把旧页的一半记录搬过去，父节点加一条指针，父节点满了还要往上继续分裂。所以主键建议用自增（或趋势递增）的短整数，而不是 UUID。
主键越短越好：二级索引叶子存主键值，bigint 比 36 字符串小得多。要时间有序又不想要发号器可用 UUIDv7（RFC 9562，高 48 位毫秒时间戳，插入集中在最右叶子，PostgreSQL 18 内置 `uuidv7()`）；MySQL 里存 `BINARY(16)`，别存 36 字符串；代价是 ID 暴露创建时间。
**2026 亮点。** 要时间有序又不想要发号器，可用 UUIDv7（RFC 9562）：高 48 位是毫秒时间戳，插入集中在最右叶子、页分裂少，PostgreSQL 18 已内置 `uuidv7()`。MySQL 里存成 `BINARY(16)`，别存 36 字符串；代价是 ID 暴露创建时间，跨节点只是大体有序。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 222">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">自增主键：只往最右追加</text>
<rect x="8" y="24" width="130" height="26" rx="3" fill="none" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="73.0" y="41.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">… 30 40（满页）</text>
<line x1="138" y1="37" x2="163.0" y2="37.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,37.0 163.0,40.2 163.0,33.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="170" y="24" width="100" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="220.0" y="41.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">50（新页）</text>
<text x="8" y="70" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不搬数据，页填充率约 15/16</text>
<text x="8" y="104" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">UUID 主键：插进中间 → 页分裂</text>
<rect x="8" y="114" width="110" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="63.0" y="131.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10 20 30 40</text>
<text x="8" y="156" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">要插入 25，页已满</text>
<line x1="118" y1="127" x2="141.0" y2="127.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="148.0,127.0 141.0,130.2 141.0,123.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="148" y="114" width="86" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="191.0" y="131.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10 20 25</text>
<rect x="244" y="114" width="88" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="288.0" y="131.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">30 40</text>
<text x="148" y="156" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">各约半满</text>
<text x="8" y="188" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">搬走一半记录，父节点加一条指针</text>
<text x="8" y="208" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">多了搬移和日志；页在磁盘上不再相邻</text>
</svg>
上半部分是自增：满页不动，新数据落到新开的最右页；下半部分是 UUID：要往已满的页插 25，页被撕成两个各约半满的页，父节点还要多记一条指针。
**举个例子。** 一个页最多放 4 条记录，看两种插入：
1. **自增：** 现有页 `10 20 30 40` 已满，来了 50，直接新开一页放 50，旧页不动，填满的旧页就留在那里。
2. **UUID：** 同样的满页 `10 20 30 40`，现在要插入 25，必须放在 20 和 30 之间。
3. **分裂：** 分配新页，把旧页分成 `10 20 25` 和 `30 40` 两页，各自只有一半左右的空间被用。
4. **父节点加指针：** 父节点要新增一条指向 `30 40` 这页的指针；父节点若也满了，继续分裂。
5. **长期后果：** 磁盘上这两页不一定挨着，范围扫描时要跳着读；整张表也因为很多半满的页而比预期大。
**容易错。**
- **以为自增就没有任何问题：** 分库分表会冲突、最右页会成为写入热点、ID 会暴露业务量；分布式用雪花这类趋势递增 ID。
- **以为页分裂只是慢一点：** 它还让页半满、磁盘上不相邻，空间和范围扫描都受影响，而且二级索引也因主键长而变大。
- **以为趋势递增和严格自增一样：** 雪花 ID 大体递增，插入大体在右侧；但要处理时钟回拨，否则会重复。
- **以为只有主键索引受影响：** 二级索引存主键值，主键长，所有二级索引一起变大。
