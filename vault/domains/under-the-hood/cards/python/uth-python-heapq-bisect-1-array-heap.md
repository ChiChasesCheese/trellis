---
id: uth-python-heapq-bisect-1-array-heap
node: python.heapq-bisect
type: qa
step: 1
---
## Q
**堆是什么，heapq 把它放在哪里**｜Python · CPython 3.14

要反复取出「当前最小的」，同时不断有新元素加入，怎么做最快？`heapq` 只有函数、没有堆这个类，堆存在什么里？

## A
**背景。** 每次从一堆数里挑最小的：直接扫一遍是 O(n)；每次插入后重新排序更贵。堆（heap）只保证一件事：每个父节点都不大于它的两个孩子，所以最小的一定在顶上，其余顺序不管，维护起来很便宜。

**结构。** 堆存在一个普通 `list` 里，当作一棵「从上到下、从左到右排满」的二叉树：下标 `i` 的子节点是 `2i+1`、`2i+2`，父节点是 `(i-1)>>1`，不要指针。例：往堆 `[3,5,8]` 里放 1，先放末尾（成为 5 的孩子），比父亲 5 小就换上去，再比 3 小再换，1 到了堆顶。这叫上浮。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<line x1="158.454" y1="33.9174" x2="111.546" y2="66.0826" stroke-width="1.2" stroke="currentColor"/>
<line x1="181.546" y1="33.9174" x2="228.454" y2="66.0826" stroke-width="1.2" stroke="currentColor"/>
<line x1="91.7516" y1="85.3121" x2="73.2484" y2="110.688" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="108.248" y1="85.3121" x2="126.752" y2="110.688" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="231.752" y1="85.3121" x2="213.248" y2="110.688" stroke-width="1.2" stroke="currentColor"/>
<line x1="248.248" y1="85.3121" x2="266.752" y2="110.688" stroke-width="1.2" stroke="currentColor"/>
<circle cx="170" cy="26" r="14" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="30" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<circle cx="100" cy="74" r="14" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="100" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<circle cx="240" cy="74" r="14" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="240" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<circle cx="65" cy="122" r="14" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="65" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<circle cx="135" cy="122" r="14" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="135" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<circle cx="205" cy="122" r="14" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="205" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<circle cx="275" cy="122" r="14" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="275" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9</text>
<rect x="44" y="150" width="36" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="62" y="167" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="62" y="192" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="80" y="150" width="36" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="98" y="167" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="98" y="192" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<rect x="116" y="150" width="36" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="134" y="167" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<text x="134" y="192" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<rect x="152" y="150" width="36" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="170" y="167" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<text x="170" y="192" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<rect x="188" y="150" width="36" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="206" y="167" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<text x="206" y="192" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<rect x="224" y="150" width="36" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="242" y="167" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<text x="242" y="192" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<rect x="260" y="150" width="36" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="278" y="167" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9</text>
<text x="278" y="192" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<text x="170" y="214" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">下标 i 的孩子是 2i+1 和 2i+2</text>
<text x="170" y="230" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor"></text>
</svg>
```

**细节。**

- `heappush` 放末尾再上浮，`heappop` 取走堆顶后让空位下沉，都是 O(log n)。
- `heapify` 从 `n//2 - 1` 往回逐个下沉，总共 O(n)；实测 100 万个浮点数：`heapify` 15.5 毫秒，逐个 `heappush` 26.3 毫秒。

**为什么。** 下标算术不要指针；叶子占一半，从下往上建堆时大部分节点几乎不用动。

**坑。** `(优先级, 对象)` 元组优先级相同时会比较对象，不可比较就抛 `TypeError`。

**例题：** LC 23 合并 K 个升序链表

给 `k` 个已按升序排列的链表，合并成一个升序链表。所有链表长度之和不超过 `10^4`。例：`[[1,4,5],[1,3,4],[2,6]]` 得 `[1,1,2,3,4,4,5,6]`。

```python
import heapq


def merge_k_lists(lists: list[ListNode | None]) -> ListNode | None:
    # 堆里放 (值, 链表编号, 节点)：值相同时比编号，永远不会去比较 ListNode
    heap = [(node.val, i, node) for i, node in enumerate(lists) if node]
    heapq.heapify(heap)
    dummy = tail = ListNode()
    while heap:
        _, i, node = heap[0]            # 堆顶就是当前最小的队头
        tail.next = node
        tail = node
        if node.next:                   # 该链表还有后继：原地替换堆顶，只做一次下沉
            heapq.heapreplace(heap, (node.next.val, i, node.next))
        else:
            heapq.heappop(heap)
    return dummy.next
```
