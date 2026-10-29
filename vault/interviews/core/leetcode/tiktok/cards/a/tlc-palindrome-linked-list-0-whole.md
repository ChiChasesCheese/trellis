---
id: tlc-palindrome-linked-list-0-whole
node: a.palindrome-linked-list
type: qa
---
## Q
**LC 234 回文链表**｜Easy · CodeTop 国内累计 26 次 · 最近 2026-09-09（CodeTop）

给单链表的头节点 `head`，判断它是否是回文链表（从前往后读和从后往前读一样）。节点数在 `[1, 10^5]`，`0 <= Node.val <= 9`。例：`[1,2,2,1]` → `true`；`[1,2]` → `false`。进阶：`O(n)` 时间、`O(1)` 空间。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 用快慢指针找到链表中点，把后半段原地反转，再和前半段逐个比较；比较完把后半段再反转回去还原。`O(n)` 时间，`O(1)` 空间。

**识别。** 回文要求「从两端向中间」比较，数组可以双指针；单链表只能向后走，所以必须让后半段也能「从尾向前」读——这正是链表反转的用途。「找中点」的信号是「快指针一次两步、慢指针一次一步」。`O(1)` 空间的进阶排除了递归（栈深 `n`）和复制到数组。

**推导。** 暴力：把值复制到数组，`vals == vals[::-1]`，`O(n)` 时间 `O(n)` 空间 → 浪费在额外数组，链表本身可以被改造 → 找到中点后，把后半段反转，使它从尾部向中间可读 → 两个指针一个从 `head` 出发，一个从反转后的尾部出发，同时前进比较 → 最后再把后半段反转回来，不留下副作用。

```python
def is_palindrome(head: ListNode | None) -> bool:
    def reverse(node: ListNode | None) -> ListNode | None:
        prev = None
        while node:
            nxt = node.next
            node.next = prev
            prev, node = node, nxt
        return prev

    slow = fast = head
    while fast and fast.next:          # 快指针走两步，慢指针走一步
        slow, fast = slow.next, fast.next.next
    tail = reverse(slow)               # slow 是后半段的起点：偶数长度时是第 n/2+1 个，奇数长度时是正中间
    left, right = head, tail
    result = True
    while right:                       # 后半段不长于前半段，以它为准
        if left.val != right.val:
            result = False
            break
        left, right = left.next, right.next
    reverse(tail)                      # 还原链表，不改动调用方的数据
    return result
```

运行：`[1,2,2,1]` → `True`，`[1,2]` → `False`，`[1]` → `True`，`[1,2,3,2,1]` → `True`，`[1,2,3,1]` → `False`；调用后链表保持原样；`10^5` 个节点的回文 → `True`。

**复杂度。** 时间 `O(n)`：找中点 `n/2` 步，反转两次共 `n`，比较 `n/2`；空间 `O(1)`。

**易错点。**
- 偶数长度时 `slow` 停在后半段第一个节点；如果误从 `slow.next` 开始反转，`[1,2,3,1]` 的后半段只剩 `[1]`，只比较一对 `1 == 1`，输出 `True`，正确是 `False`。
- 循环条件要同时检查 `fast` 和 `fast.next`，否则奇数、偶数长度会有一边空指针报错。
- 反转后前半段最后一个节点的 `next` 仍然指向中点，所以比较要以后半段（`right`）走完为准，而不是以前半段走完为准。

**追问。**
- 不允许修改链表：复制成数组再双指针，`O(n)` 空间；或者递归，`O(n)` 栈。
- 为什么要还原：并发读取或后续还要使用这条链表；反转两次是 `O(n)`，成本很小。
- 值域不是 `0..9`、而是任意可比较的对象：本解只用 `!=` 比较，不受影响；若是双向链表，直接头尾双指针，不需要反转。

**同模式。** LC 876 链表的中间结点、LC 206 反转链表、LC 143 重排链表、LC 125 验证回文串。
