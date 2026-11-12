---
slug: swap-nodes-in-pairs
---
## Q
**LC 24 两两交换链表中的节点**｜Medium

两两交换链表中相邻的节点，不能改节点的值，返回新头节点。

## A
**一句话。** 哑结点加 `prev` 指针，每轮把 `prev→a→b→rest` 改接成 `prev→b→a→rest`。

```python
def swap_pairs(head):
    dummy = ListNode(0, head)
    prev = dummy
    while prev.next and prev.next.next:
        a, b = prev.next, prev.next.next
        a.next = b.next    # 先接 rest，再动 b
        b.next = a
        prev.next = b
        prev = a           # a 是这一对的新尾
    return dummy.next
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 先 `b.next = a` 再 `a.next = b.next`：变成 `a.next = a`，`[1,2,3,4]` 成自环。
- 末尾写 `prev = b`：下一轮把 `1`、`3` 又换一次，输出 `[2,3,4,1]`。
- 条件少判 `prev.next.next`：`[1,2,3]` 的 `3` 读空指针。

**追问。**
- 递归怎么写？：`swap(head)` 交换前两个，第二个的 `next` 指向 `swap(rest)`，栈深 `O(n)`。
- 推广到每 `k` 个一组？：就是 LC 25，用同样的 `prev` 加翻转子段。

**同模式。** LC 25 K 个一组翻转链表、LC 206 反转链表、LC 92 反转链表 II、LC 328 奇偶链表
