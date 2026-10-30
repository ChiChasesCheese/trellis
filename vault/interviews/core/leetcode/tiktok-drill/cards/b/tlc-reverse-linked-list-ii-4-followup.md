---
id: tlc-reverse-linked-list-ii-4-followup
node: b.reverse-linked-list-ii
type: qa
step: 4
---
## Q
**LC 92 反转链表 II**｜追问

面试官接着问：（1）不用头插法，用常规的三段式（反转区间再接回两端）怎么写？（2）每 `k` 个节点一组反转（LC 25）怎么复用？（3）链表很长、`left`、`right` 离得很远，一趟扫描和两趟扫描有区别吗？

## A
1. **三段式**：`pre` 走到第 `left - 1` 个，然后对区间做普通的 `prev / cur` 反转，循环 `right - left + 1` 次。结束时 `prev` 是反转后的头，`cur` 是 `right` 后面的第一个节点。接回：`pre.next.next = cur`（区间原来的头，现在是尾，指向后面），`pre.next = prev`。

```python
def reverse_between_3seg(head: ListNode | None, left: int, right: int) -> ListNode | None:
    dummy = ListNode(0, head)
    pre = dummy
    for _ in range(left - 1):
        pre = pre.next
    prev, cur = None, pre.next
    for _ in range(right - left + 1):
        cur.next, prev, cur = prev, cur, cur.next
    pre.next.next = cur                 # 区间的新尾巴接回后面
    pre.next = prev                     # 区间的新头接到前面
    return dummy.next
```

2. **K 个一组（LC 25）**：先确认后面还有 `k` 个节点，有就对这一段做头插法（或三段式），`pre` 移到这一段的尾，继续下一组；不足 `k` 个就停。每个节点被处理一次，`O(n)` 时间，`O(1)` 空间。
3. **一趟与两趟**：渐近复杂度相同。头插法在走到 `right` 时就结束，只走 `right` 步，后面的节点不用碰，常数最小；两趟（先找右端点）多走一遍，但逻辑更直白。

**Python 提醒**：`cur.next, prev, cur = prev, cur, cur.next` 右边先求值，三个值都是旧的，再从左到右赋值：先 `cur.next = prev`（此时 `cur` 还是旧的），再 `prev = cur`，最后 `cur = 旧的 cur.next`。左边的顺序不能换：如果把 `cur` 放在第一个，`cur.next` 会作用到新的 `cur` 上，把链表搞坏。
