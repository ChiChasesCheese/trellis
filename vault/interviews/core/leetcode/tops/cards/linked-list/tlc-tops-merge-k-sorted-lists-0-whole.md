---
id: tlc-tops-merge-k-sorted-lists-0-whole
node: linked-list.merge-k-sorted-lists
type: qa
---
## Q
**LC 23 合并 K 个升序链表**｜Hard · 全公司热度第 15 名 · Blind 75、NeetCode 150、Hot 100、Top Interview 150

给你一个链表数组，每个链表都已经按升序排列。请将所有链表合并到一个升序链表中，返回合并后的链表。`k == lists.length`，`0 <= k <= 10^4`，`0 <= lists[i].length <= 500`，`-10^4 <= lists[i][j] <= 10^4`，`lists[i]` 按升序排列，所有 `lists[i].length` 的总和不超过 `10^4`。例：`lists = [[1,4,5],[1,3,4],[2,6]]` → `[1,1,2,3,4,4,5,6]`；`lists = []` → `[]`；`lists = [[]]` → `[]`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 多路归并（k-way merge）：小根堆保存各链表当前的头节点。

**一句话。** 堆里始终放每条链表的当前头节点，弹出最小的接到结果链尾，再把它的下一个节点压进堆；重复到堆空。

**识别。** 「多个有序序列合并成一个有序序列」是归并，路数多时用堆挑出当前最小。`k` 路、总共 `N` 个节点：每个节点进出堆一次，`O(N log k)`。`N <= 10^4`。

**推导。** 每次扫描 `k` 个头节点找最小，总共 `O(Nk)`；先把所有节点倒进一个数组排序，`O(N log N)` 且要 `O(N)` 额外空间。堆把「在 `k` 个候选里选最小」降到 `O(log k)`：每个节点弹出后只引入它的后继，堆的大小始终不超过 `k`。

```python
import heapq

def merge_k_lists(lists: list[ListNode | None]) -> ListNode | None:
    # 堆元素 (值, 链表编号, 节点)：值相同时比较编号；每条链表在堆里至多一个节点，编号各不相同，永远比不到节点本身
    heap = [(head.val, i, head) for i, head in enumerate(lists) if head]
    heapq.heapify(heap)
    dummy = tail = ListNode()                      # 哑头节点，省掉对结果链表为空的特判
    while heap:
        _, i, node = heapq.heappop(heap)           # 当前所有头节点里最小的
        tail.next = node
        tail = node
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))   # 补上同一条链表的下一个节点
    return dummy.next
```

运行：`[[1,4,5],[1,3,4],[2,6]]` → `[1,1,2,3,4,4,5,6]`；`[]` → `[]`；`[[]]` → `[]`；`[[1],[0]]` → `[0,1]`。

**复杂度。** 时间 `O(N log k)`；空间 `O(k)`，堆的大小（结果链表复用原节点）。

**拓展优化。**
- 分治两两合并（不用堆）：把 `k` 条链表对半分、递归合并，再用 LC 21 的合并两个有序链表；同样 `O(N log k)`，额外空间只有递归栈 `O(log k)`。
```python
def merge_k_lists_dc(lists: list[ListNode | None]) -> ListNode | None:
    def merge_two(a: ListNode | None, b: ListNode | None) -> ListNode | None:
        dummy = tail = ListNode()
        while a and b:
            if a.val <= b.val:                     # 相等取 a：保持稳定
                tail.next, a = a, a.next
            else:
                tail.next, b = b, b.next
            tail = tail.next
        tail.next = a or b                         # 剩下的一条直接接上
        return dummy.next

    def solve(lo: int, hi: int) -> ListNode | None:   # 合并 lists[lo:hi]
        if hi - lo == 0:
            return None
        if hi - lo == 1:
            return lists[lo]
        mid = (lo + hi) // 2
        return merge_two(solve(lo, mid), solve(mid, hi))

    return solve(0, len(lists))
```

**易错点。**
- 堆元素写成 `(val, node)`：两个节点值相同时 Python 会去比较 `ListNode`，抛 `TypeError: '<' not supported between instances of 'ListNode' and 'ListNode'`。中间必须插入一个互不相同的编号。
- 空链表 `None` 也压进堆：访问 `head.val` 报 `AttributeError`；`lists = [[]]` 和 `lists = []` 都要返回 `None`。

**同模式。** LC 21 合并两个有序链表、LC 378 有序矩阵中第 K 小的元素、LC 373 查找和最小的 K 对数字、LC 264 丑数 II。
