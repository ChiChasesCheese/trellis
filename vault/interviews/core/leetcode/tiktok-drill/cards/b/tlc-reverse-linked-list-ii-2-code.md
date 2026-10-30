---
id: tlc-reverse-linked-list-ii-2-code
node: b.reverse-linked-list-ii
type: qa
step: 2
---
## Q
**LC 92 反转链表 II**｜写出 Python 实现

单链表头指针 `head`（节点数 `n` 在 `[1, 500]`）和整数 `left`、`right`（`1 <= left <= right <= n`）。反转位置 `left` 到 `right` 的节点（位置从 `1` 开始），返回新的头节点，要求一趟扫描。

## A
**思路。** 哑节点 `dummy` 指向 `head`。`pre` 前进 `left - 1` 步，停在区间前一个节点。`cur = pre.next` 是区间里原来的第一个节点。接着做 `right - left` 次：取出 `cur` 后面的节点 `nxt`，让 `cur` 跳过它，再把 `nxt` 插到 `pre` 的后面。结束时区间已经反转，`cur` 在区间末尾，后面自然接着原来区间之后的节点。

```python
def reverse_between(head: ListNode | None, left: int, right: int) -> ListNode | None:
    dummy = ListNode(0, head)           # 哑节点：left = 1 时也有"前一个节点"
    pre = dummy
    for _ in range(left - 1):           # pre 停在第 left - 1 个节点
        pre = pre.next
    cur = pre.next                      # cur 始终是区间里原来的第一个节点，会被一步步挤到后面
    for _ in range(right - left):       # 头插法：把 cur 后面的节点依次插到 pre 后面
        nxt = cur.next
        cur.next = nxt.next
        nxt.next = pre.next
        pre.next = nxt
    return dummy.next
```

运行：`[1,2,3,4,5]`，`left = 2`，`right = 4` → `[1, 4, 3, 2, 5]`，`[5]`，`1`，`1` → `[5]`，`[1,2,3,4,5]`，`1`，`5` → `[5, 4, 3, 2, 1]`，`[1,2]`，`1`，`2` → `[2, 1]`，`[1,2,3]`，`2`，`2` → `[1, 2, 3]`。

**复杂度。** 时间 `O(n)`：至多走 `right` 步；空间 `O(1)`。

**写法要点。** `ListNode(0, head)` 一行造出哑节点并指向 `head`，返回 `dummy.next` 就是新的头；`for _ in range(k)` 表示只重复 `k` 次，不使用循环变量；头插的四行赋值每行只改一个指针，顺序不能换：`cur.next = nxt.next` 先让 `cur` 绕过 `nxt`，`nxt.next = pre.next` 把 `nxt` 接到区间现有的头上，最后 `pre.next = nxt` 让 `nxt` 成为新头；`left == right` 时第二个循环一次都不执行，原样返回。
