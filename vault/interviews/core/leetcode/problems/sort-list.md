---
slug: sort-list
---
## Q
**LC 148 排序链表**｜Medium

把链表按升序排序，要求 `O(n log n)` 时间。

## A
**一句话。** 归并排序：快慢指针找中点断开，递归排两半，再合并两个有序链表。

```python
def sort_list(head):
    if not head or not head.next:
        return head
    slow, fast = head, head.next      # fast 多走一步，两个节点也能切开
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    mid, slow.next = slow.next, None  # 必须断开
    return merge(sort_list(head), sort_list(mid))

def merge(a, b):
    dummy = tail = ListNode()
    while a and b:
        if a.val <= b.val:            # 相等取 a，保持稳定
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b
    return dummy.next
```

**复杂度。** 时间 `O(n log n)`，空间 `O(log n)`（递归栈）。

**易错点。**
- 找中点后没断开 `slow.next`：左半段仍连着右半段，无限递归。
- `fast` 也从 `head` 起步：`[2,1]` 时 `mid` 为空，左半段还是 `[2,1]`，无限递归。

**追问。**
- 怎么做到 `O(1)` 空间？：自底向上归并，按 1、2、4… 的步长切段合并，不用递归。
- 为什么不用快排？：链表无法随机访问，选枢轴和划分都别扭，最坏 `O(n^2)`；归并稳定 `O(n log n)`。

**同模式。** LC 21 合并两个有序链表、LC 23 合并 K 个升序链表、LC 147 对链表进行插入排序、LC 912 排序数组
