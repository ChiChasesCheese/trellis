---
id: tlc-odd-even-linked-list-2-code
node: a.odd-even-linked-list
type: qa
step: 2
---
## Q
**LC 328 奇偶链表**｜写出 Python 实现

单链表头节点 `head`（节点数 `0 <= n <= 10^4`），把下标为奇数的节点按原顺序排在前，下标为偶数的节点按原顺序接在后，返回新链表头。要求 `O(1)` 额外空间、`O(n)` 时间。

## A
**思路。** `odd` 从第 1 个节点出发、`even` 从第 2 个出发，两个指针各自隔一个节点串链；先保存偶链头，拆完后把偶链接在奇链尾。

```python
def odd_even_list(head: ListNode | None) -> ListNode | None:
    if head is None:
        return None
    odd, even = head, head.next
    even_head = even                   # 偶数链表的头：最后要接在奇数链表后面
    while even and even.next:
        odd.next = even.next           # 奇数节点跳过一个偶数节点
        odd = odd.next
        even.next = odd.next           # 偶数节点跳过刚摘下的奇数节点
        even = even.next
    odd.next = even_head
    return head
```

运行：`[1,2,3,4,5]` → `[1,3,5,2,4]`，`[2,1,3,5,6,4,7]` → `[2,3,6,7,1,5,4]`，`[]` → `[]`，`[1]` → `[1]`，`[1,2,3,4]` → `[1,3,2,4]`。

**复杂度。** 时间 `O(n)`：每个节点被访问一次；空间 `O(1)`：三个指针。

**写法要点。** `while even and even.next` 利用短路求值，同时覆盖奇数长度（`even.next` 为空）和偶数长度（`even` 为空）的结尾；`odd, even = head, head.next` 元组赋值把两个起点一行写清；不用哑头节点，因为头节点永远是奇链的头，不会变；类型写 `ListNode | None`，空链表是合法输入。
