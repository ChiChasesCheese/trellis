---
id: tlc-remove-duplicates-from-sorted-list-4-followup
node: a.remove-duplicates-from-sorted-list
type: qa
step: 4
---
## Q
**LC 83 删除排序链表中的重复元素**｜追问

面试官接着问：（1）重复出现的值一个都不留（LC 82）怎么写？（2）链表无序时怎么去重？（3）要保留最后一次出现的节点而不是第一次？

## A
1. **整段删光（LC 82）**：头节点也可能被删，所以加哨兵节点 `dummy`；用 `prev` 指向最后一个确定保留的节点，遇到重复段就走到段尾，让 `prev.next` 越过整段。

```python
def delete_duplicates_all(head: ListNode | None) -> ListNode | None:
    dummy = ListNode(0, head)              # 哨兵：头节点也可能被删掉
    prev = dummy
    while prev.next:
        cur = prev.next
        if cur.next and cur.val == cur.next.val:
            while cur.next and cur.val == cur.next.val:
                cur = cur.next             # 走到这一段重复值的最后一个
            prev.next = cur.next           # 整段都不要
        else:
            prev = cur
    return dummy.next
```

`[1,1,2]` → `[2]`，`[1,1,2,3,3]` → `[2]`，`[1,1,1]` → `[]`。
2. **无序链表**：用 `seen = set()` 记录已经出现的值，遇到见过的就摘掉，保留第一次出现，`O(n)` 时间、`O(n)` 空间；不允许额外空间时，先对链表做归并排序（`O(n log n)`）再用上面的解法。
3. **保留最后一次**：用 `prev` 追踪前驱，`cur.val == cur.next.val` 时删除 `cur` 本身（`prev.next = cur.next`），否则 `prev = cur`；头节点可能被删，所以要哨兵节点。

**Python 提醒**：`ListNode(0, head)` 利用构造函数的第二个参数一次建好哨兵并接上原链表，不用先建空节点再判断头。
