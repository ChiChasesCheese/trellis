---
slug: partition-list
---
## Q
**LC 86 分隔链表**｜Medium

把链表分隔，使所有 `< x` 的节点排在 `>= x` 的节点之前，两部分内部保持原相对顺序。

## A
**一句话。** 拆成小链和大链两条（各用哑结点），遍历一遍按值分发，断开大链尾巴后把小链接到大链头。

```python
def partition(head, x):
    sd, bd = ListNode(), ListNode()
    s, b = sd, bd                  # 两条链的尾指针
    while head:
        if head.val < x:
            s.next = head
            s = head
        else:
            b.next = head
            b = head
        head = head.next
    b.next = None                  # 断开，防止成环
    s.next = bd.next
    return sd.next
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 忘了 `b.next = None`：`[3,1]`、`x = 3` 中 `3.next` 还指着 `1`，成环。
- 把 `== x` 放进小链：`x = 3` 的节点 `3` 必须在大链，否则得 `[1,3,2,2,4,5]`。

**追问。**
- 三路划分呢？：多一条链，三个哑结点。
- 数组上怎么做？：荷兰国旗或快排 partition，但不稳定。

**同模式。** LC 328 奇偶链表、LC 725 分隔链表、LC 21 合并两个有序链表、LC 75 颜色分类
