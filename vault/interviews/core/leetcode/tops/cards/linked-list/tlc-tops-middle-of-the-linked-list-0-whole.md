---
id: tlc-tops-middle-of-the-linked-list-0-whole
node: linked-list.middle-of-the-linked-list
type: qa
---
## Q
**LC 876 链表的中间结点**｜Easy · 全公司热度第 184 名

给你单链表的头结点 `head`，找出并返回链表的中间结点；如果有两个中间结点，返回**第二个**。链表结点数在 `[1, 100]` 之间，`1 <= Node.val <= 100`。例：`head = [1,2,3,4,5]` → `[3,4,5]`；`head = [1,2,3,4,5,6]` → `[4,5,6]`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 快慢指针（fast-slow pointers）：快指针速度是慢指针的两倍。

**一句话。** 慢指针每次走一步，快指针每次走两步，快指针走到末尾时，慢指针正好在中间。

**识别。** 「单链表」「不知道长度」「找中点 / 找倒数第 k 个 / 判环」= 快慢指针，一趟遍历，`O(1)` 空间。

**推导。** 暴力：先遍历一遍数出长度 `n`，再走 `n // 2` 步，两趟遍历。快指针的速度是慢指针的两倍，所以快指针走完全程时，慢指针恰好走了一半。偶数个结点时，快指针停在末尾之后（`fast` 为 `None`），此时慢指针在第二个中间结点，正是题目要的。

```python
def middle_node(head: ListNode | None) -> ListNode | None:
    slow = fast = head
    while fast and fast.next:  # fast 能再走两步才继续；偶数个结点 fast 先变 None，奇数个 fast 停在最后一个结点
        slow = slow.next
        fast = fast.next.next
    return slow  # 偶数个结点时是第二个中间结点
```

运行：`[1,2,3,4,5]` → `[3,4,5]`；`[1,2,3,4,5,6]` → `[4,5,6]`；`[1]` → `[1]`；`[1,2]` → `[2]`。

**复杂度。** 时间 `O(n)`（一趟，`fast` 走 `n / 2` 次），空间 `O(1)`。

**拓展优化。**
- 偶数个结点要返回**第一个**中间结点（或需要前驱结点来删除中点，LC 2095）：循环条件改为 `while fast.next and fast.next.next`；要前驱就多维护一个 `prev`。

**易错点。**
- 循环条件写成 `while fast.next`：偶数个结点时 `fast` 先变成 `None`，下一次判断 `None.next` 抛 `AttributeError`；必须先判断 `fast` 自己。
- 条件写成 `while fast.next and fast.next.next`：`[1,2,3,4,5,6]` 返回 `[3,4,5,6]`（第一个中点），正确是 `[4,5,6]`。
- 单结点链表 `[1]` 直接返回 `head`，上面的写法自然成立。

**同模式。** LC 141 环形链表、LC 142 环形链表 II、LC 234 回文链表、LC 143 重排链表。
