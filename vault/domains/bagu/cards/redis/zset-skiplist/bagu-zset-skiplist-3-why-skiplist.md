---
id: bagu-zset-skiplist-3-why-skiplist
node: a.redis.zset-skiplist
type: qa
step: 3
---
## Q
**ZSet · 为什么用跳表，而不是红黑树或 B+ 树**｜必会

面试官：「平衡树也是 O(log N)，ZSet 为什么选跳表，不选红黑树，也不选 MySQL 用的 B+ 树？」

## A
**基本回答。** 平衡树和跳表查找都是 O(log N)，复杂度打平时 Redis 选跳表是因为它在 ZSet 要做的事上更顺手：范围查询定位后沿最底层有序链表一路往右，红黑树要中序遍历、上下回溯；实现简单，插入只改相邻几个指针，没有旋转；内存省，p=1/4 时每节点平均约 1.33 个 forward 指针，二叉树固定 2 个；每个指针记着跨度，沿路径累加就是名次，`ZRANK` 是 O(log N)，红黑树要给每个节点额外维护子树大小。不选 B+ 树：它为磁盘页的高扇出设计，数据全在内存时没有收益，页分裂合并还更复杂。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 176">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">跳表最底层：按分数排好的双向链表</text>
<rect x="14" y="30" width="40" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="34.0" y="47.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<line x1="54" y1="43" x2="62" y2="43" stroke-width="1.2" stroke="currentColor"/>
<polygon points="62.0,43.0 55.0,46.2 55.0,39.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="62" y="30" width="40" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="82.0" y="47.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<line x1="102" y1="43" x2="110" y2="43" stroke-width="1.2" stroke="currentColor"/>
<polygon points="110.0,43.0 103.0,46.2 103.0,39.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="110" y="30" width="40" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="130.0" y="47.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">12</text>
<line x1="150" y1="43" x2="158" y2="43" stroke-width="1.2" stroke="currentColor"/>
<polygon points="158.0,43.0 151.0,46.2 151.0,39.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="158" y="30" width="40" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="178.0" y="47.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">17</text>
<line x1="198" y1="43" x2="206" y2="43" stroke-width="1.2" stroke="currentColor"/>
<polygon points="206.0,43.0 199.0,46.2 199.0,39.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="206" y="30" width="40" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="226.0" y="47.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">21</text>
<line x1="246" y1="43" x2="254" y2="43" stroke-width="1.2" stroke="currentColor"/>
<polygon points="254.0,43.0 247.0,46.2 247.0,39.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="254" y="30" width="40" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="274.0" y="47.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">26</text>
<line x1="130" y1="98" x2="130" y2="60" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="130.0,60.0 133.2,67.0 126.8,67.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="130" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">① 定位到 ≥12 的第一个</text>
<text x="130" y="130" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">O(log N)</text>
<line x1="130" y1="66" x2="130" y2="66" stroke-width="1.2" stroke="currentColor"/>
<line x1="170" y1="72" x2="226" y2="72" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="226.0,72.0 219.0,75.2 219.0,68.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="240" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">② 往右走 M 步</text>
<text x="8" y="156" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">红黑树：中序遍历要上下回溯，没有现成的横向链</text>
</svg>
先定位一次（O(log N)），之后范围查询就是沿着最底层的链表往右走 M 步；红黑树里相邻的两个值可能在不同的子树，要上下来回走。
**业务场景。** 打赏榜两个操作：Top 100 是范围遍历，主播名次是跨度求和，都是跳表最顺手的；插入一笔打赏只改几个指针，不用旋转。
**容易错。**
- **以为跳表渐近更快：** 同样 O(log N)；而且层数随机，是期望 O(log N)，最坏 O(N)，概率可忽略。短板是指针追逐、缓存局部性差。
- **以为 Redis 选跳表是为了并发：** Redis 单线程；无锁是 Java `ConcurrentSkipListMap` 的理由（只改局部指针，容易做成无锁）。
