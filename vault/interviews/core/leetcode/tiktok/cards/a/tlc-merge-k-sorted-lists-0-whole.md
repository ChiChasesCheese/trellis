---
id: tlc-merge-k-sorted-lists-0-whole
node: a.merge-k-sorted-lists
type: qa
---
## Q
**LC 23 合并 K 个升序链表**｜Hard · TikTok·字节 高频

给一个链表数组 `lists`，每个链表都已按升序排列。把所有链表合并成一个升序链表，返回合并后的链表。`k == lists.length`，`0 <= k <= 10^4`，`0 <= lists[i].length <= 500`，`-10^4 <= lists[i][j] <= 10^4`，所有链表长度之和不超过 `10^4`。例：`lists = [[1,4,5],[1,3,4],[2,6]]` → `[1,1,2,3,4,4,5,6]`；`lists = []` → `[]`；`lists = [[]]` → `[]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 用最小堆（`heapq`）装着每条链表当前的队头；每次弹出最小的接到结果链表后面，再把它的后继换进堆。`N` 为总节点数，`O(N log k)`。

**识别。** 「`k` 路有序合并」：每一步都是从 `k` 个候选里取最小的那个，正是堆的用途，也是外部排序的核心。每条链表内部已经有序，所以全局最小一定在某条链表的队头。

**推导。** 暴力一：每次扫描 `k` 个队头找最小，`O(N · k)`，最坏 `10^4 × 10^4 = 10^8` 次比较。暴力二：把所有值收集起来整体排序，`O(N log N)`，还要 `O(N)` 额外空间，并且没用上「每条链表已经有序」。洞察：堆把「取最小」从 `O(k)` 降到 `O(log k)`；堆里始终只有 `k` 个队头，总共 `N` 次弹出 → `O(N log k)`，空间 `O(k)`，节点原地复用。堆元素写成 `(值, 链表编号, 节点)`：值相同时元组会继续比较下一项，`ListNode` 不能比较大小，必须有一个唯一的编号挡在前面。

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

运行：`[[1,4,5],[1,3,4],[2,6]]` → `[1, 1, 2, 3, 4, 4, 5, 6]`，`[]` → `[]`，`[[]]` → `[]`，`10^4` 条各含一个节点的链表也能正确合并。

**复杂度。** 时间 `O(N log k)`：`N` 次堆操作，每次 `O(log k)`；空间 `O(k)`（堆），不新建节点。

**易错点。**
- 堆里只放 `(node.val, node)`：两个队头的值相同，比较会落到 `ListNode` 上，抛 `TypeError: '<' not supported between instances of 'ListNode' and 'ListNode'`。`[[1,4],[1,3]]` 就会触发。多放一个唯一编号 `i`。
- 把空链表也放进堆：`lists = [[]]` 里的元素是 `None`，`None.val` 会抛 `AttributeError`；建堆时用 `if node` 过滤。
- 弹出后忘记把后继放回堆：`[[1,4,5],[1,3,4],[2,6]]` 只会得到 `[1, 1, 2]`。

**追问。**
- 分治：相邻两两合并，`log k` 轮，同样 `O(N log k)`，额外空间 `O(1)`，直接复用合并两个链表。
- 逐个顺序合并 `ans = merge(ans, lists[i])` 是 `O(N · k)` 级别：`10^4` 条单节点链表要访问约 `5 × 10^7` 个节点，而堆和分治只要约 `1.4 × 10^5`。
- 输入是 `k` 个有序文件或迭代器：用 `heapq.merge(*iterables)`，惰性产生，内存只与 `k` 有关。

**同模式。** LC 21 合并两个有序链表、LC 378 有序矩阵中第 K 小的元素、LC 373 查找和最小的 K 对数字、LC 264 丑数 II、LC 632 最小区间。
