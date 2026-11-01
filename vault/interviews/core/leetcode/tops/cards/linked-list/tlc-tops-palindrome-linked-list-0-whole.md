---
id: tlc-tops-palindrome-linked-list-0-whole
node: linked-list.palindrome-linked-list
type: qa
---
## Q
**LC 234 回文链表**｜Easy · 全公司热度第 161 名 · Hot 100

给你一个单链表的头节点 `head`，判断该链表是否为回文链表。是返回 `true`，否则返回 `false`。链表中节点数目在 `[1, 10^5]` 内，`0 <= Node.val <= 9`。进阶：你能否用 `O(n)` 时间复杂度和 `O(1)` 空间复杂度解决此题？

例：`head = [1,2,2,1]` → `true`；`head = [1,2]` → `false`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点：** 快慢指针找中点 + 原地反转后半段 + 双指针比较；三个链表基本操作的组合。

**一句话。** 找到链表中点，把后半段反转，再让两个指针从两端向中间逐个比较值。

**识别。** 单链表不能从尾巴往前走，所以「首尾对称」要靠反转一半来把尾巴变成可前进的方向；「`O(1)` 空间」排除了复制数组。`n` 到 `10^5`，线性。

**推导。** 把值复制到数组再用双指针比较，最简单，空间 `O(n)`。要 `O(1)` 空间就得在链表上做：把后半段反转，它就从尾巴出发朝中间走；前半段从头出发朝中间走，两个指针同步前进，配对的正好是首尾对称的两个结点。

**简单解法。** 同样的配对思路，用数组代替反转：
```python
def is_palindrome_array(head: ListNode | None) -> bool:
    vals = []
    while head:
        vals.append(head.val)
        head = head.next
    return vals == vals[::-1]
```

**最优解：** 反转后半段。

```python
def is_palindrome(head: ListNode | None) -> bool:
    # 1. 快慢指针：slow 停在前半段的最后一个结点（奇数长时，中间结点归前半段）
    slow = fast = head
    while fast.next and fast.next.next:
        slow, fast = slow.next, fast.next.next
    # 2. 反转后半段，prev 成为后半段的新头
    prev, cur = None, slow.next
    while cur:
        cur.next, prev, cur = prev, cur, cur.next
    # 3. 两段同时前进比较；后半段不长于前半段，所以以它为界，奇数长时中间结点自然被跳过
    p, q = head, prev
    while q:
        if p.val != q.val:
            return False
        p, q = p.next, q.next
    return True
```

**运行。** `[1,2,2,1]` → `True`；`[1,2]` → `False`；`[1]` → `True`；`[1,2,3,2,1]` → `True`；`[1,2,3,1]` → `False`。

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**拓展优化。**
- 面试官常追问「不要破坏输入链表」：比较完再把后半段反转一次并接回 `slow.next`。
- 递归版：用一个外部指针从头往后走，递归回溯时从尾往前走，回溯一次比一次，空间 `O(n)` 栈。

**易错点。**
- 把中点停错一格：若用 `while fast and fast.next` 让 `slow` 停在后半段起点，再从 `slow.next` 反转，`[1,2,3,1]` 的后半段只剩 `[1]`，比较通过，错误返回 `True`（正确答案 `False`）。
- 比较结点对象而不是值：`p == q` 对不同对象恒为假，`[1,2,2,1]` 会返回 `False`。
- 反转时漏存后继：拆成逐行赋值 `cur.next = prev` 之后再取 `cur.next`，后半段只剩一个结点，`[1,2,3,2,1]` 这类奇数长回文会被误判为 `False`。

**同模式。** LC 206 反转链表、LC 876 链表的中间结点、LC 143 重排链表、LC 125 验证回文串。
