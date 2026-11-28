---
id: bagu-redo-undo-binlog-6-buffer-pool
node: a.mysql.redo-undo-binlog
type: qa
step: 6
---
## Q
**Buffer Pool · 脏页刷盘怎么和几类日志配合**｜追问

面试官：「Buffer Pool 是什么？脏页什么时候刷盘？脏页没刷数据库崩溃了为什么不丢？」

## A
**基本回答。** Buffer Pool（缓冲池）是 InnoDB 在内存里缓存数据页和索引页的区域，默认 128MB，生产环境常设成物理内存的一半到四分之三。读数据先找缓冲池，没有才读磁盘；写数据直接改缓冲池里的页，这个页就变成了脏页（和磁盘上的内容不一样），同时写 redo，不立即写盘。崩溃时脏页会丢，但重启后从检查点起用 redo 重做，所以数据不丢。刷脏页的时机：redo 空间快满了，要推进检查点；脏页比例超过 `innodb_max_dirty_pages_pct`（默认 90）；空闲页不够用；后台空闲时；正常关闭时。
LRU 分 young（热）和 old（新读入，约占 37%）区，防全表扫描冲垮热数据：新页先进 old，超过 `innodb_old_blocks_time`（默认 1000 毫秒）后再被访问才升入 young。变更缓冲（change buffer）：二级索引页不在内存时修改先记在这里，页被读入时合并，省一次随机读。双写缓冲（8.0.46 默认 ON）：写页前先完整写一份到专门区域，防页写到一半断电而损坏。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 230">
<rect x="8" y="8" width="100" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58" y="29" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读写请求</text>
<rect x="124" y="8" width="100" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="174" y="21.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Buffer Pool</text>
<text x="174" y="36.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">内存缓存数据页</text>
<rect x="240" y="8" width="92" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="286" y="29" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">磁盘数据页</text>
<line x1="108" y1="25" x2="118" y2="25" stroke-width="1.2" stroke="currentColor"/>
<polygon points="124.0,25.0 117.0,28.2 117.0,21.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="224" y1="25" x2="234" y2="25" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<polygon points="240.0,25.0 233.0,28.2 233.0,21.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="232" y="56" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">后台慢慢刷脏页</text>
<rect x="124" y="70" width="100" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="174" y="87" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">redo（顺序写）</text>
<line x1="174" y1="42" x2="174" y2="64" stroke-width="1.2" stroke="currentColor"/>
<polygon points="174.0,70.0 170.8,63.0 177.2,63.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="126" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">LRU 链表：young 区在左（热），old 区在右（新来）</text>
<rect x="8" y="134" width="205" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="110.5" y="153" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">young 区（约 63%）</text>
<rect x="213" y="134" width="119" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="272.5" y="153" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">old 区约 37%</text>
<text x="8" y="186" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">新页先进 old 区；超过 1 秒再被访问</text>
<text x="8" y="204" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">才晋升 young（innodb_old_blocks_time）</text>
<text x="8" y="222" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">一次性全表扫描的页挤不掉热数据</text>
</svg>
上半是读写路径：请求只和 Buffer Pool 打交道，改页的同时顺序写 redo，脏页由后台慢慢刷回磁盘。下半是 LRU 链表（最近最少使用淘汰）的 young、old 两个区。
**举个例子。** 大促订单库，写入高峰：
1. **提交很快：** 每次提交只顺序追加 redo，延迟 2 毫秒左右。
2. **脏页越攒越多：** 后台刷盘速度被 `innodb_io_capacity` 限制，跟不上写入。
3. **redo 快写满：** 要推进检查点，必须先把对应的脏页刷出去。
4. **强制刷脏：** InnoDB 不得不同步刷脏页，写入暂停，提交延迟飙到几百毫秒。
5. **调参后恢复：** 调大 redo 容量，并按 SSD 能力调大 `innodb_io_capacity`，刷得更快，抖动消失。
6. **LRU 的场景：** 夜里跑一次全表扫描报表，页先进 old 区；扫完不会再被访问，也就不会晋升，白天的热点页还留在 young 区。
**容易错。**
- **以为脏页没刷盘就丢数据：** 脏页丢了没关系，redo 已落盘，重启重做就恢复。
- **以为 Buffer Pool 越大越好：** 要给操作系统和其他内存留空间，所以通常设到物理内存的一半到四分之三。
- **以为全表扫描不影响缓存：** 没有 young/old 分区的话会挤掉热数据；有分区，新页要超过 1 秒再次被访问才晋升。
- **以为刷脏只由后台决定：** redo 将满时是强制同步刷，用户请求会被阻塞。
