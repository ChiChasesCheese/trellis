---
slug: remove-duplicates-from-sorted-list-ii
---
## Q
**LC 82 删除排序链表中的重复元素 II**｜Medium

升序链表，删除所有出现重复的数字，一个都不留，返回新链表。

## A
**一句话。** 哑结点加 `prev`（最后保留的结点）：遇到重复段就整段跳过，`prev.next` 接到段后。

```python
def delete_duplicates(head):
    dummy = ListNode(0, head)
    prev, cur = dummy, head
    while cur:
        if cur.next and cur.next.val == cur.val:
            dup = cur.val
            while cur and cur.val == dup:   # 整段一个不留
                cur = cur.next
            prev.next = cur    # prev 不前进
        else:
            prev, cur = cur, cur.next
    return dummy.next
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 留一个（LC 83 的做法）：`[1,2,3,3,4,4,5]` 得 `[1,2,3,4,5]`，应为 `[1,2,5]`。
- 跳段后让 `prev` 前进：下一段重复值被误保留，`[1,1,2,2,3]` 应为 `[3]`。
- 没有哑结点：头结点属于重复段时无 `prev` 可接，`[1,1,2]` 应为 `[2]`。

**追问。**
- 链表无序呢？：先 `Counter` 统计，再扫一遍删掉计数不为 `1` 的结点。
- 递归怎么写？：头与下一个不同则 `head.next = f(head.next)`，相同则跳过整段返回 `f(段后)`。

**同模式。** LC 83 删除排序链表中的重复元素、LC 80 删除有序数组中的重复项 II、LC 203 移除链表元素、LC 19 删除链表的倒数第 N 个结点
