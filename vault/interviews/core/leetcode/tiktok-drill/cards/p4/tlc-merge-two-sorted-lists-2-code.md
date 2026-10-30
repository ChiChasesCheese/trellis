---
id: tlc-merge-two-sorted-lists-2-code
node: p4.merge-two-sorted-lists
type: qa
step: 2
---
## Q
**LC 21 合并两个有序链表**｜写出 Python 实现

两个升序链表的头节点 `list1`、`list2`（节点数各在 `[0, 50]`，值在 `[-100, 100]`）。通过拼接原来的节点，合并成一个升序链表并返回头节点。

## A
**思路。** 建一个哑节点，`tail` 指向结果链表的末尾，初始就是哑节点。只要两条链表都非空，就比较队头，把较小的接到 `tail` 后面，该链表前进一格，`tail` 也前进一格。循环结束时至多一条还有节点，直接把它整段挂在 `tail` 后面。返回哑节点的下一个。

```python
def merge_two_lists(list1: ListNode | None, list2: ListNode | None) -> ListNode | None:
    dummy = tail = ListNode()           # 哑节点：省掉"第一个节点怎么接"的特判
    while list1 and list2:
        if list1.val <= list2.val:      # 相等时取 list1，保持稳定
            tail.next, list1 = list1, list1.next
        else:
            tail.next, list2 = list2, list2.next
        tail = tail.next
    tail.next = list1 or list2          # 至多一条还有剩，整段直接挂上
    return dummy.next
```

运行：`[1,2,4]` 与 `[1,3,4]` → `[1, 1, 2, 3, 4, 4]`，`[]` 与 `[]` → `[]`，`[]` 与 `[0]` → `[0]`；结果中的节点都是原来的节点对象，没有新建。

**复杂度。** 时间 `O(m + n)`：每个节点被接一次；空间 `O(1)`：只有哑节点和几个指针。

**写法要点。** `dummy = tail = ListNode()` 链式赋值让两个名字指向同一个哑节点；`tail.next, list1 = list1, list1.next` 是元组赋值，右边先求值为（旧 `list1`，旧 `list1.next`），再依次赋给左边，因此「接上去」和「前进」在一行里完成，不会读到已被修改的值；`list1 or list2` 利用节点对象为真、`None` 为假，直接选出非空的那一条；相等时取 `list1`，对相同值的节点保持原有的先后次序。
