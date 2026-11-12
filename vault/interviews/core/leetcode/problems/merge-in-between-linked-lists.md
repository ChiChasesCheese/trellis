---
slug: merge-in-between-linked-lists
---
## Q
**LC 1669 合并两个链表**｜Medium

删除链表 `list1` 中下标 `a` 到 `b`（含）的节点，把 `list2` 接在被删的位置，返回结果链表头。

## A
**一句话。** 链表手术：找到下标 `a-1` 的 `before` 和下标 `b+1` 的 `after`，中间接上 `list2` 的头尾。

```python
def merge_in_between(list1, a, b, list2):
    dummy = ListNode(0, list1)
    before = dummy
    for _ in range(a):              # 停在下标 a-1
        before = before.next
    after = before
    for _ in range(b - a + 2):      # 停在下标 b+1
        after = after.next
    before.next = list2
    tail = list2
    while tail.next:                # 找 list2 的尾
        tail = tail.next
    tail.next = after
    return dummy.next
```

**复杂度。** 时间 `O(n + m)`，空间 `O(1)`。

**易错点。**
- 第二段少走一步（`b - a + 1`）：停在下标 `b`，被删的那个节点又接了回来。
- 没找 `list2` 的尾就接 `after`：`list2` 后面的节点全丢了。

**追问。**
- 要返回被删下来的那一段？：在 `b` 处断开（`node.next = None`），保存头指针。
- `a` 可以是 `0` 吗？：哑节点已经覆盖，不用改。

**同模式。** LC 92 反转链表 II、LC 24 两两交换链表中的节点、LC 25 K 个一组翻转链表、LC 86 分隔链表
