---
slug: merge-two-sorted-lists
---
## Q
**LC 21 合并两个有序链表**｜Easy

把两个升序链表拼接成一个新的升序链表并返回。

## A
**一句话。** 哑节点加双指针，每次把较小的队头接到结果尾，一方走空后整段接上另一方。

```python
def merge_two_lists(list1, list2):
    dummy = tail = ListNode()    # 哑节点，免去头节点特判
    while list1 and list2:
        if list1.val <= list2.val:   # 相等取 list1，保持稳定
            tail.next, list1 = list1, list1.next
        else:
            tail.next, list2 = list2, list2.next
        tail = tail.next
    tail.next = list1 or list2   # 剩下的本来有序
    return dummy.next
```

**复杂度。** 时间 `O(m+n)`，空间 `O(1)`。

**易错点。**
- 循环后忘了接剩余部分：`[1,2,4]` 与 `[1,3,4]` 输出 `[1,1,2,3,4]`，丢了最后的 `4`。
- 不用哑节点：每步多一个「是不是第一个」的分支，容易空指针。

**追问。**
- 合并 `k` 条链（LC 23）？：分治两两合并，`O(N log k)`；逐条往前并会退化成 `O(kN)`。
- 怎么用它排序链表（LC 148）？：快慢指针找中点断开，两半递归排序再合并。

**同模式。** LC 23 合并 K 个升序链表、LC 148 排序链表、LC 88 合并两个有序数组、LC 86 分隔链表
