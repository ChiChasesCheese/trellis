---
id: bagu-bplus-tree-5-leaf-list
node: a.mysql.bplus-tree
type: qa
step: 5
---
## Q
**叶子链表 · 范围查询和排序怎么用上它**｜追问

面试官：「B+ 树的叶子链表在范围查询和 ORDER BY 里起什么作用？」

## A
**基本回答。** 叶子页按键有序排列，并且用双向链表连在一起。范围查询先从根 O(log N) 找到第一条满足条件的记录，再沿链表顺序往后读，读到越界为止。`ORDER BY` 的列正好是索引的顺序时，读出来本身就是有序的，不需要额外排序（filesort）；`ORDER BY ... DESC` 就沿链表反向走。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 206">
<rect x="110" y="8" width="120" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="25.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">根 / 非叶子页</text>
<rect x="8" y="78" width="70" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="43.0" y="95.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1~9</text>
<rect x="92" y="78" width="70" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="127.0" y="95.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10~19</text>
<rect x="176" y="78" width="70" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="211.0" y="95.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">20~29</text>
<rect x="260" y="78" width="70" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="295.0" y="95.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">30~39</text>
<line x1="78" y1="87" x2="85.0" y2="87.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="92.0,87.0 85.0,90.2 85.0,83.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="92" y1="95" x2="85.0" y2="95.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="78.0,95.0 85.0,91.8 85.0,98.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="162" y1="87" x2="169.0" y2="87.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="176.0,87.0 169.0,90.2 169.0,83.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="176" y1="95" x2="169.0" y2="95.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="162.0,95.0 169.0,91.8 169.0,98.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="246" y1="87" x2="253.0" y2="87.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="260.0,87.0 253.0,90.2 253.0,83.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="260" y1="95" x2="253.0" y2="95.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="246.0,95.0 253.0,91.8 253.0,98.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="150" y1="34" x2="130.24277946540582" y2="71.79642189226715" stroke-width="1.2" stroke="currentColor"/>
<polygon points="127.0,78.0 127.4,70.3 133.1,73.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="158" y="62" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">O(log N) 找到起点</text>
<text x="8" y="132" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">WHERE id BETWEEN 15 AND 32</text>
<text x="8" y="152" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1. 从根往下找到第一条 ≥15 的记录</text>
<text x="8" y="172" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">2. 沿链表往后读，读到 &gt;32 就停</text>
<text x="8" y="192" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ORDER BY 与索引同序：免 filesort</text>
</svg>
图顶部是根页，用 O(log N) 找到起点所在的叶子页（10~19）；然后沿着叶子之间的双向箭头往右读，一直读到越界（>32）为止，不需要再回到根。
**举个例子。** 订单按 `id` 范围查 `BETWEEN 15 AND 32`，叶子页依次是 `1~9`、`10~19`、`20~29`、`30~39`：
1. **找起点：** 从根往下，O(log N) 找到第一条 ≥ 15 的记录，落在 `10~19` 这页。
2. **顺着读：** 读完这页里 15 到 19 的记录，沿链表到下一页 `20~29`，整页都满足，全部取走。
3. **到边界：** 再到 `30~39`，读到 32 之后发现下一条 33 超出范围，停下。没有再回到根重新查。
4. **倒序：** 若加 `ORDER BY id DESC`，从 32 开始沿链表反向读到 15，同样不需要排序。
5. **联合索引的例子：** `(user_id, status, created_at)` 里 `user_id=5 AND status=1` 的记录按 `created_at` 排好，`DESC` 就是从最新一条往回读。
**容易错。**
- **以为 B+ 树范围查询每条都要从根查：** 只要查一次起点，之后全靠叶子链表。
- **以为有索引就一定走索引：** 命中行太多时，优化器会选全表扫描，因为回表的随机访问比顺读全表贵。
- **以为倒序一定要降序索引：** 升序索引沿链表反向走就行（Extra 为 `Backward index scan`）。
- **忘了回表的代价：** 二级索引查整行要回聚簇索引；覆盖索引才能只读叶子。
