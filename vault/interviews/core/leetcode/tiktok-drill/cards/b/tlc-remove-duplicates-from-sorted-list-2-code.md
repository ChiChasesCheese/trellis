---
id: tlc-remove-duplicates-from-sorted-list-2-code
node: b.remove-duplicates-from-sorted-list
type: qa
step: 2
---
## Q
**LC 83 删除排序链表中的重复元素**｜写出 Python 实现

升序链表节点数在 `[0, 300]`，值在 `[-100, 100]`。原地删除重复值，使每个值只出现一次，返回链表头。

## A
**思路。** 用 `cur` 从头走。当 `cur` 和 `cur.next` 值相同，把 `cur.next` 摘掉并留在原地继续比较；不同才前进。头节点不会被删，直接返回 `head`。

```python
def delete_duplicates(head: ListNode | None) -> ListNode | None:
    cur = head
    while cur and cur.next:
        if cur.val == cur.next.val:
            cur.next = cur.next.next       # 跳过重复节点，cur 原地不动，继续和新的下一个比
        else:
            cur = cur.next
    return head
```

运行：`[1,1,2]` → `[1,2]`，`[1,1,2,3,3]` → `[1,2,3]`，`[]` → `[]`，`[1,1,1]` → `[1]`，`[1,1,1,2]` → `[1,2]`。

**复杂度。** 时间 `O(n)`；空间 `O(1)`。

**写法要点。** `while cur and cur.next` 同时处理空链表和最后一个节点；`if / else` 分支让「删除」与「前进」互斥，避免连续重复漏删；只改 `next` 指针，不创建新节点，被摘掉的节点由垃圾回收处理；没有哨兵节点，因为头节点必保留。`itertools.groupby` 可以写出「每组取第一个」的列表版，但需要先把链表转成列表，空间 `O(n)`。
