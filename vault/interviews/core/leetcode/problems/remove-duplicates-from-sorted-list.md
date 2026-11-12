---
slug: remove-duplicates-from-sorted-list
---
## Q
**LC 83 删除排序链表中的重复元素**｜Easy

给升序链表 `head`，删除重复元素，让每个值只出现一次，返回链表。

## A
**一句话。** 有序则重复值相邻：`cur.next` 与 `cur` 同值就摘掉它，否则 `cur` 前进。

```python
def delete_duplicates(head):
    cur = head
    while cur and cur.next:
        if cur.val == cur.next.val:
            cur.next = cur.next.next   # 摘掉，cur 不动
        else:
            cur = cur.next
    return head
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 摘掉后还前进：`[1,1,1]` 得 `[1,1]`，应为 `[1]`；摘除时 `cur` 要原地不动。
- 循环条件漏掉 `cur`：空链表会对 `None` 取 `.next`。

**追问。**
- 重复的值一个都不留（LC 82）？：加哨兵和 `prev`，遇到一段重复就整段摘掉。
- 无序链表怎么去重？：用 `set` 记录见过的值，`O(n)` 空间。

**同模式。** LC 82 删除排序链表中的重复元素 II、LC 26 删除有序数组中的重复项、LC 203 移除链表元素、LC 1836 从未排序的链表中移除重复元素
