---
id: uth-storage-lsm-1-write-path
node: storage.lsm
type: qa
step: 1
---
## Q
**LSM 写路径：内存表、SST、分层**｜RocksDB · v10.9

RocksDB 写一条数据时发生了什么？数据怎样从内存一路沉到最底层？

## A
**背景。** 磁盘上顺序写很快，随机写很慢。B+ 树更新一行，要先找到那一页再原地修改，是随机写。LSM 树的办法是不原地改：新数据先攒在内存里，攒够了一次性按顺序写成新文件，旧数据以后再整理。

**结构。** 写先追加到 WAL（预写日志，顺序写，崩溃后靠它恢复），再插入内存表（memtable，一块按 key 排好序的内存结构）。内存表满 64 MB（`write_buffer_size`）就冻结，刷成一个有序、不可变的磁盘文件 SST，放进第 0 层（L0）。文件越攒越多，后台把它们合并（compaction）：多路归并，同一个 key 只留最新的，结果放进下一层。例：依次写 a=1、b=2、a=3，内存表里 a 只剩 a=3，刷出的 SST 是有序的 a=3、b=2。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 192">
<rect x="34" y="18" width="120" height="26" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="94" y="35.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1 WAL 顺序追加</text>
<rect x="166" y="18" width="164" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="248" y="35.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2 memtable 跳表</text>
<line x1="248" y1="44" x2="248" y2="68" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="248,74 245.0,68.0 251.0,68.0" stroke="currentColor" stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<text x="240" y="64" text-anchor="end" font-size="12" font-family="sans-serif" fill="currentColor">满 64 MB 刷盘</text>
<text x="8" y="92" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">L0</text>
<rect x="34" y="74" width="30" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="68" y="74" width="30" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="102" y="74" width="30" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="136" y="74" width="30" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<line x1="100" y1="100" x2="100" y2="112" stroke="currentColor" stroke-width="1.2"/>
<polygon points="100,118 97.0,112.0 103.0,112.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="112" y="113" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">攒够 4 个合并</text>
<text x="8" y="134" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">L1</text>
<rect x="34" y="118" width="170" height="26" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="216" y="135" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">每层 x10</text>
<line x1="100" y1="144" x2="100" y2="154" stroke="currentColor" stroke-width="1.2"/>
<polygon points="100,160 97.0,154.0 103.0,154.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="176" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">L2</text>
<rect x="34" y="160" width="296" height="26" fill="none" stroke="currentColor" stroke-width="1.2"/>
</svg>
```

**细节。**

- L0 的文件之间键范围会重叠；攒够 4 个（`level0_file_num_compaction_trigger`）就合并进 L1。
- 默认 7 层，每层目标大小是上一层的 10 倍（`max_bytes_for_level_multiplier`）。

**为什么。** 随机写变成顺序追加和顺序合并，比 B+ 树原地改页更贴合磁盘的顺序带宽。

**例题：** LC 23 合并 K 个升序链表

给一个链表数组 `lists`，每个链表已按升序排列，把它们合并成一个升序链表。所有链表长度之和不超过 `10^4`。例：`lists = [[1,4,5],[1,3,4],[2,6]]` → `[1,1,2,3,4,4,5,6]`。

```python
import heapq

class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None) -> None:
        self.val = val
        self.next = next

def merge_k_lists(lists: list[ListNode | None]) -> ListNode | None:
    heap = [(node.val, i, node) for i, node in enumerate(lists) if node]  # i 打破 val 相同时的比较
    heapq.heapify(heap)
    dummy = ListNode()
    tail = dummy
    while heap:
        val, i, node = heapq.heappop(heap)
        tail.next = node
        tail = tail.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    return dummy.next
```
