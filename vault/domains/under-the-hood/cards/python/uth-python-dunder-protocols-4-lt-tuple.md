---
id: uth-python-dunder-protocols-4-lt-tuple
node: python.dunder-protocols
type: qa
step: 4
---
## Q
**排序和堆只用 <：元组并列会怎样**｜Python · CPython 3.14

堆里放 `(优先级, 任务对象)`，两个任务的优先级相同时，为什么会 `TypeError`？

## A
**背景。** 排序、堆、`min`、`max` 只需要知道「谁更小」。Python 把它约定成只用一个运算 `a < b`：你的类只要有 `__lt__`，就能直接进 `sorted` 和 `heapq`，不必把六个比较都写全。

**结构。** `a < b` 先调 `a.__lt__(b)`；它返回 `NotImplemented`（意思是「我不会比」）时，再试 `b.__gt__(a)`；都不会就 `TypeError`。比较元组时，从左到右用 `==` 找到第一个不相等的位置，再只对这个位置用 `<`。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<g font-size="12" font-family="sans-serif" text-anchor="middle" stroke-width="1.2">
<g fill="none" stroke="currentColor">
<rect x="50" y="36" width="60" height="30" rx="3"/>
<rect x="50" y="86" width="60" height="30" rx="3"/>
<line x1="80" y1="120" x2="80" y2="126"/>
</g>
<g stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))">
<rect x="110" y="36" width="130" height="30" rx="3"/>
<rect x="110" y="86" width="130" height="30" rx="3"/>
</g>
<g fill="currentColor" stroke="currentColor" stroke-width="0.5">
<polygon points="80.0,126.0 77.0,120.0 83.0,120.0"/>
</g>
<g fill="currentColor">
<text x="80" y="55">1</text>
<text x="175" y="55">节点A</text>
<text x="80" y="105">1</text>
<text x="175" y="105">节点B</text>
<text x="80" y="140">1 == 1</text>
</g>
<g style="fill:var(--dim,#6b7280)">
<text x="30" y="54">a</text>
<text x="30" y="104">b</text>
<text x="80" y="156">继续</text>
<text x="175" y="156">没有 __lt__</text>
</g>
<g style="fill:var(--accent,#3b6fd4)">
<text x="175" y="140">节点A &lt; 节点B ?</text>
<text x="175" y="190">=&gt; TypeError</text>
</g>
</g>
</svg>
```

**细节。**

- `list.sort` 和 `heapq` 的 C 实现都只调 `<`（`Py_LT`）。
- 实测：`(1, N(1)) < (1, N(2))` 抛 `'<' not supported between instances of 'N' and 'N'`；`(1, N(1)) < (2, N(0))` 在第一项就分出胜负，不会碰第二项。
- `functools.total_ordering`：只写 `__eq__` 和 `__lt__`，自动补上 `<=`、`>`、`>=`。

**坑。** 并列时的修法：在元组中间放一个不会重复的序号 `(优先级, i, 任务)`，比较永远到不了最后一项。

**例题：** LC 23 合并 K 个升序链表

给一个链表数组 `lists`，每个链表已按升序排好。把它们合并成一个升序链表，`0 <= k <= 10^4`，所有链表长度之和不超过 `10^4`。例：`[[1,4,5],[1,3,4],[2,6]]` 得 `[1,1,2,3,4,4,5,6]`。

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
