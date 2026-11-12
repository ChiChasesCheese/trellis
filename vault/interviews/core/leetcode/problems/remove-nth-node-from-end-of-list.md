---
slug: remove-nth-node-from-end-of-list
---
## Q
**LC 19 删除链表的倒数第 N 个节点**｜Medium

删除链表的倒数第 `n` 个节点并返回头节点，要求只扫一趟。

## A
**一句话。** 哑节点加快慢指针：快指针先走 `n` 步，再同速前进，快指针到尾时慢指针恰好在待删节点之前。

```python
def remove_nth_from_end(head, n):
    dummy = ListNode(0, head)    # 删头节点也不用特判
    fast = slow = dummy
    for _ in range(n):           # 拉开 n 的间距
        fast = fast.next
    while fast.next:
        fast, slow = fast.next, slow.next
    slow.next = slow.next.next
    return dummy.next
```

**复杂度。** 时间 `O(sz)`，空间 `O(1)`。

**易错点。**
- 没有哑节点：`[1]`、`n=1` 时删的是头，慢指针没有前驱。
- 返回 `head` 而不是 `dummy.next`：头被删后 `head` 已过期。
- 间距、起点、停止条件要配套：从 dummy 出发、走 `n` 步、`while fast.next`，改一个就偏一位。

**追问。**
- 递归怎么写？：回溯时计数，计到 `n` 的那层删除，栈空间 `O(sz)`。
- `n` 大于长度怎么办？：先走的过程中 `fast` 变空就直接返回原链表。

**同模式。** LC 876 链表的中间结点、LC 61 旋转链表、LC 142 环形链表 II、LC 160 相交链表
