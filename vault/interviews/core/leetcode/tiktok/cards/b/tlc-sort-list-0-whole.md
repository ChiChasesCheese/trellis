---
id: tlc-sort-list-0-whole
node: b.sort-list
type: qa
---
## Q
**LC 148 排序链表**｜Medium · LC TikTok 全时段热度 38/100 · 近一年被问：美国 0 次、国内 1 次 · CodeTop 国内累计 70 次 · 最近 2026-09-27（国内 CodeTop）

给链表的头结点 `head`，将其按升序排列并返回排序后的链表。链表中节点的数目在 `[0, 5 * 10^4]` 内，`-10^5 <= Node.val <= 10^5`。例：`head = [4,2,1,3]` → `[1,2,3,4]`；`head = [-1,5,3,4,0]` → `[-1,0,3,4,5]`；`head = []` → `[]`。进阶：能否在 `O(n log n)` 时间和常数级空间复杂度下完成。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 归并排序：用快慢指针找到中点并断开，递归排序左右两半，再用「合并两个有序链表」把它们合并。`O(n log n)` 时间，递归栈 `O(log n)`；进阶的 `O(1)` 空间用自底向上的归并。

**识别。** 「链表排序」首选归并排序：链表没有随机访问，快速排序的划分和堆排序的下标运算都不方便；而合并两个有序链表只改指针，是 `O(1)` 空间、稳定的。`n` 到 `5 * 10^4`，`O(n log n)` 约 `8 * 10^5` 次操作；`O(n^2)` 约 `2.5 * 10^9`，超时。

**推导。** 暴力一：把值取出来用 `sorted` 排序再写回，`O(n log n)` 时间但 `O(n)` 空间，面试官一般要求真的重排节点。暴力二：对链表做插入排序或冒泡，`O(n^2)`，超时。洞察：归并的两个部件在链表上都很便宜：用快慢指针找中点 `O(n)`；合并两段有序链表 `O(n)`。递归每层把链表对半分，深度 `log n`，每层总共处理 `n` 个节点 → `O(n log n)`。`5 * 10^4` 个节点的递归深度只有约 `16`，不会触到 Python 的递归上限。

```python
def sort_list(head: ListNode | None) -> ListNode | None:
    def merge(a: ListNode | None, b: ListNode | None) -> ListNode | None:
        dummy = tail = ListNode()
        while a and b:
            if a.val <= b.val:
                tail.next, a = a, a.next
            else:
                tail.next, b = b, b.next
            tail = tail.next
        tail.next = a or b
        return dummy.next

    if not head or not head.next:
        return head
    slow, fast = head, head.next        # fast 先走一步：偶数长度时 slow 停在前半段末尾
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    mid, slow.next = slow.next, None    # 断开成两半
    return merge(sort_list(head), sort_list(mid))
```

运行：`[4,2,1,3]` → `[1, 2, 3, 4]`，`[-1,5,3,4,0]` → `[-1, 0, 3, 4, 5]`，`[]` → `[]`，`[1]` → `[1]`，`5 * 10^4` 个随机数、逆序数、全相同的数都能正确排序；值相同的节点保持原来的先后顺序（稳定）。

**复杂度。** 时间 `O(n log n)`；空间 `O(log n)`（递归栈）。

**易错点。**
- 找中点时 `fast` 也从 `head` 出发：`[2,1]` 里 `slow` 会走到第二个节点，`mid` 是 `None`，左半段仍是完整的两个节点，递归永远缩不小，抛 `RecursionError`。让 `fast` 从 `head.next` 出发，偶数长度时 `slow` 才停在前半段末尾。
- 不断开 `slow.next`：左半段仍连着右半段，递归处理的就是整条链表，同样无限递归。
- 合并后忘了挂剩余部分（`tail.next = a or b`）：其中一段的尾部节点会丢掉。
- 用 `sorted(nodes)` 直接排节点：`ListNode` 没有 `<`，抛 `TypeError`；要给 `key=lambda n: n.val`。

**追问。**
- 进阶 `O(1)` 空间：自底向上，段长 `size` 从 `1` 开始翻倍；每轮把链表切成长度 `size` 的小段，两两合并，不需要递归。
- 稳定性：合并时相等取左边（`<=`），值相同的节点保持原来的顺序。
- 为什么不用快速排序：链表无法 `O(1)` 随机选基准，基准选得不好最坏 `O(n^2)`；归并的复杂度与数据分布无关。

**同模式。** LC 21 合并两个有序链表、LC 23 合并 K 个升序链表、LC 147 对链表进行插入排序、LC 876 链表的中间结点、LC 912 排序数组。
