---
id: uth-storage-lsm-2-skiplist-memtable
node: storage.lsm
type: qa
step: 2
---
## Q
**内存表为什么是跳表**｜RocksDB · v10.9

RocksDB 的内存表默认用什么数据结构？为什么不用红黑树？

## A
**背景。** 内存表要同时做到三件事：随时插入新 key，按 key 有序遍历（刷盘时要有序写出），多个线程一起写。

**结构。** 默认 `SkipListFactory`：跳表（skip list）。底层是一条有序链表，上面叠几层“快车道”：每个元素以 1/4 的概率长到上一层（`branching_factor = 4`），最多 12 层，平均每个元素约 1.33 个指针。查找从最高层出发，大步往前，走过头了就下一层，像图里找 40。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 174">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每层以 1/4 的概率再长高一层</text>
<text x="2" y="140" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">L1</text>
<rect x="26" y="124" width="28" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="40" y="139.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">头</text>
<rect x="69" y="124" width="30" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="84" y="139.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10</text>
<rect x="113" y="124" width="30" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="128" y="139.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">20</text>
<rect x="157" y="124" width="30" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="172" y="139.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">30</text>
<rect x="201" y="124" width="30" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="216" y="139.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">40</text>
<rect x="245" y="124" width="30" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="260" y="139.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">50</text>
<rect x="289" y="124" width="30" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="304" y="139.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">60</text>
<line x1="54" y1="135" x2="64" y2="135" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="69,135 64.0,137.5 64.0,132.5" stroke="currentColor" stroke-width="0.5" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)"/>
<line x1="99" y1="135" x2="108" y2="135" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="113,135 108.0,137.5 108.0,132.5" stroke="currentColor" stroke-width="0.5" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)"/>
<line x1="143" y1="135" x2="152" y2="135" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="157,135 152.0,137.5 152.0,132.5" stroke="currentColor" stroke-width="0.5" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)"/>
<line x1="187" y1="135" x2="196" y2="135" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="201,135 196.0,137.5 196.0,132.5" stroke="currentColor" stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<line x1="231" y1="135" x2="240" y2="135" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="245,135 240.0,137.5 240.0,132.5" stroke="currentColor" stroke-width="0.5" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)"/>
<line x1="275" y1="135" x2="284" y2="135" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="289,135 284.0,137.5 284.0,132.5" stroke="currentColor" stroke-width="0.5" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)"/>
<text x="2" y="102" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">L2</text>
<rect x="26" y="86" width="28" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="40" y="101.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">头</text>
<rect x="69" y="86" width="30" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="84" y="101.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10</text>
<rect x="157" y="86" width="30" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="172" y="101.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">30</text>
<rect x="245" y="86" width="30" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="260" y="101.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">50</text>
<line x1="54" y1="97" x2="64" y2="97" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="69,97 64.0,99.5 64.0,94.5" stroke="currentColor" stroke-width="0.5" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)"/>
<line x1="99" y1="97" x2="152" y2="97" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="157,97 152.0,99.5 152.0,94.5" stroke="currentColor" stroke-width="0.5" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)"/>
<line x1="187" y1="97" x2="240" y2="97" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="245,97 240.0,99.5 240.0,94.5" stroke="currentColor" stroke-width="0.5" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)"/>
<text x="2" y="64" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">L3</text>
<rect x="26" y="48" width="28" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="40" y="63.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">头</text>
<rect x="157" y="48" width="30" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="172" y="63.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">30</text>
<line x1="54" y1="59" x2="152" y2="59" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="157,59 152.0,61.5 152.0,56.5" stroke="currentColor" stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<line x1="172" y1="70" x2="172" y2="81" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="172,86 169.5,81.0 174.5,81.0" stroke="currentColor" stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<line x1="172" y1="108" x2="172" y2="119" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="172,124 169.5,119.0 174.5,119.0" stroke="currentColor" stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="168" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">查 40: 高层大步走, 逐层下降</text>
</svg>
```

**细节。**

- 多线程可以并发插入（`allow_concurrent_memtable_write`，默认开启），但只有跳表实现支持。
- 有序遍历就是顺着最底层链表走，刷成 SST 时按序直接写出，不用再排序。

**为什么。** 跳表插入只改局部的几个指针，容易做成无锁并发；平衡树（如红黑树）的旋转要同时改好几个节点，并发实现麻烦得多。

**对应 LeetCode：** 无直接对应的题
