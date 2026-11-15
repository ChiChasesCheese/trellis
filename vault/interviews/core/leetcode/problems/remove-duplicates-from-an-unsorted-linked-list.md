---
slug: remove-duplicates-from-an-unsorted-linked-list
---
## Q
**LC 1836 从未排序的链表中移除重复元素**｜Medium

给未排序的链表头节点 `head`。找出所有值出现超过一次的节点，把这些值对应的**所有**节点都删掉，返回链表。

## A
**一句话。** 先遍历一次数每个值出现的次数，再用哑节点遍历第二次，只保留出现一次的节点。

```python
def delete_duplicates_unsorted(head):
    cnt = Counter()
    cur = head
    while cur:
        cnt[cur.val] += 1
        cur = cur.next
    dummy = ListNode(0, head)
    pre = dummy
    while pre.next:
        if cnt[pre.next.val] > 1:
            pre.next = pre.next.next     # 删掉，pre 不动
        else:
            pre = pre.next
    return dummy.next
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 删除后还让 `pre` 前进：会跳过紧接着的下一个节点。
- 值第一次出现就保留：要求出现多次的值**全部**删除，包括第一个。

**追问。**
- 如果只保留每个值的第一个呢？：用 `seen` 集合，遇到已见过的才删。

**同模式。** LC 82 删除排序链表中的重复元素 II、LC 83 删除排序链表中的重复元素、LC 203 移除链表元素、LC 26 删除有序数组中的重复项
