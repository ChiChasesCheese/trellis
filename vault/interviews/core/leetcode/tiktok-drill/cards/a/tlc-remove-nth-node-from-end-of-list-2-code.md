---
id: tlc-remove-nth-node-from-end-of-list-2-code
node: a.remove-nth-node-from-end-of-list
type: qa
step: 2
---
## Q
**LC 19 删除链表的倒数第 N 个节点**｜写出 Python 实现

给单链表头结点 `head`（结点数 `sz`，`1 <= sz <= 30`，值在 `0` 到 `100`）和整数 `n`（`1 <= n <= sz`），删除倒数第 `n` 个结点并返回头结点。要求一趟扫描，`O(1)` 额外空间。

## A
**思路。** 哑结点 `dummy` 接在头结点前。`fast` 先走 `n` 步，之后 `fast`、`slow` 同速走，直到 `fast.next` 为空；此时 `slow.next` 就是待删结点，跳过它。

```python
def remove_nth_from_end(head: ListNode | None, n: int) -> ListNode | None:
    dummy = ListNode(0, head)               # 哑结点：删头结点时不用特判
    fast = slow = dummy
    for _ in range(n):                      # fast 先走 n 步，和 slow 拉开 n 的间距
        fast = fast.next
    while fast.next:                        # fast 停在最后一个结点时，slow 正好在待删结点的前一个
        fast, slow = fast.next, slow.next
    slow.next = slow.next.next
    return dummy.next
```

运行：`[1,2,3,4,5]`、`n = 2` → `[1, 2, 3, 5]`；`[1]`、`n = 1` → `[]`；`[1,2]`、`n = 1` → `[1]`；`[1,2]`、`n = 2` → `[2]`。

**复杂度。** 时间 `O(sz)`：两个指针合起来最多走 `2 * sz` 步，一趟；空间 `O(1)`。

**写法要点。**
- `ListNode(0, head)` 一行建出哑结点并接上原链表。
- `fast = slow = dummy` 让两个名字先指向同一个结点，之后各自重新绑定，互不影响。
- `fast, slow = fast.next, slow.next` 元组赋值同步前进两个指针。
- `while fast.next:` 直接用结点的真值（非空为真）做循环条件，读起来就是“还没到最后一个结点”。
- Python 有垃圾回收，被跳过的结点不用手动释放。
