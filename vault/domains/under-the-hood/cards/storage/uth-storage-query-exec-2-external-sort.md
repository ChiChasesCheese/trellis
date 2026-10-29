---
id: uth-storage-query-exec-2-external-sort
node: storage.query-exec
type: qa
step: 2
---
## Q
**外部排序：切段排序，再 k 路归并**｜PostgreSQL · 18

`ORDER BY` 的数据远大于 `work_mem` 时，PostgreSQL 怎么排序？一次最多同时归并几路？

## A
**背景。** 数据比内存大，没法一次在内存里排完。

**结构。** 外部排序（external sort）：每攒满 `work_mem`（默认 4 MB）的元组，就在内存里快排成一段有序的 run，写进临时文件；最后把所有 run 做 k 路归并，也就是同时从 k 段里各取最小的那个往外输出。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 140">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每攒满 work_mem 排成一个 run</text>
<rect x="8" y="22" width="100" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="58" y="39.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1 5 9</text>
<line x1="108" y1="35" x2="139.698" y2="65.8175" stroke="currentColor" stroke-width="1.2"/>
<polygon points="144,70 137.6,68.0 141.8,63.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="54" width="100" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="58" y="71.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2 6 7</text>
<line x1="108" y1="67" x2="138.021" y2="69.5017" stroke="currentColor" stroke-width="1.2"/>
<polygon points="144,70 137.8,72.5 138.3,66.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="86" width="100" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="58" y="103.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3 4 8</text>
<line x1="108" y1="99" x2="139.327" y2="73.764" stroke="currentColor" stroke-width="1.2"/>
<polygon points="144,70 141.2,76.1 137.4,71.4" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="146" y="48" width="84" height="44" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="188" y="66" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k 路归并</text>
<text x="188" y="82" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">默认 15 路</text>
<line x1="230" y1="70" x2="244" y2="70" stroke="currentColor" stroke-width="1.2"/>
<polygon points="250,70 244.0,73.0 244.0,67.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="250" y="54" width="82" height="32" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="291" y="74.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">有序输出</text>
<text x="170" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">临时文件里的 run 一路读一路归并</text>
</svg>
```

**细节。** 归并路数 = `work_mem / (2 × 8 KB + 256 KB)`，下限 6、上限 500；默认 4 MB 得 15 路。

**坑。** 路数封顶 500：路数太高，CPU 缓存效应更差，多付一趟 I/O 反而更快。

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
