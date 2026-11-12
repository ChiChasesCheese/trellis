---
slug: sort-list
---
## Q
**LC 148 排序链表**｜Medium

给你链表的头结点 `head`，请将其按升序排列并返回排序后的链表。链表中节点的数目在范围 `[0, 5 * 10^4]` 内，`-10^5 <= Node.val <= 10^5`。进阶：你可以在 `O(n log n)` 时间复杂度和常数级空间复杂度下，对链表进行排序吗？

例：`head = [4,2,1,3]` → `[1,2,3,4]`；`head = [-1,5,3,4,0]` → `[-1,0,3,4,5]`；`head = []` → `[]`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点：** 链表归并排序（merge sort on linked list）：快慢指针二分 + 合并有序链表；链表上最自然的 `O(n log n)` 排序。

**一句话。** 找中点断成两半，递归排序两半，再用「合并两个有序链表」合起来。

**识别。** 「链表 + 排序 + `O(n log n)`」：快排和堆排依赖随机访问，链表上做不了；归并排序只需要顺序访问，且合并在链表上是 `O(1)` 空间。`n` 到 `5 * 10^4`，递归深度 `log n`，安全。

**推导。** 把值拷到数组排序再写回，能过但不是在排结点。要在链表上做，选归并：二分用快慢指针（不需要长度），合并用双指针。每层合计扫描 `n` 个结点，共 `log n` 层，`O(n log n)`。

```python
def sort_list(head: ListNode | None) -> ListNode | None:
    if not head or not head.next:           # 0 或 1 个结点：已有序
        return head
    # 快慢指针找前半段的尾；fast 从 head.next 起步，保证 2 个结点时也能
    # 切成 1 + 1
    slow, fast = head, head.next
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    # 断开：前半段 [head, slow]，后半段从 mid 起
    mid, slow.next = slow.next, None
    return merge_sorted(sort_list(head), sort_list(mid))


def merge_sorted(
        a: ListNode | None,
        b: ListNode | None) -> ListNode | None:
    dummy = tail = ListNode()
    while a and b:
        if a.val <= b.val:                  # 相等取 a，归并排序保持稳定
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b
    return dummy.next
```

**运行。** `[4,2,1,3]` → `[1, 2, 3, 4]`；`[-1,5,3,4,0]` → `[-1, 0, 3, 4, 5]`；`[]` → `[]`；`[2,1]` → `[1, 2]`。

**复杂度。** 时间 `O(n log n)`；空间 `O(log n)`（递归栈）。

**拓展优化。**
- 进阶要求严格常数空间：自底向上归并。先把长度为 1 的段两两合并，再长度 2、4、8……每轮扫一遍，没有递归栈。
```python
def cut(head: ListNode | None, k: int) -> ListNode | None:
    """切下以 head 开头的前 k 个结点，返回剩下部分的头。"""
    while head and k > 1:
        head, k = head.next, k - 1
    if not head:
        return None
    rest, head.next = head.next, None
    return rest


def sort_list_bottom_up(head: ListNode | None) -> ListNode | None:
    length, node = 0, head
    while node:
        length, node = length + 1, node.next
    dummy = ListNode(0, head)
    step = 1
    # 每轮把相邻的两段（各 step 个）合并成一段
    while step < length:
        tail, cur = dummy, dummy.next
        while cur:
            left = cur
            # 切出 left，right 是剩余部分的头
            right = cut(left, step)
            # 再切出 right，cur 是下一对的头
            cur = cut(right, step)
            tail.next = merge_sorted(left, right)
            # 把 tail 推到合并后这一段的末尾
            while tail.next:
                tail = tail.next
        step *= 2
    return dummy.next
```

**易错点。**
- 找中点后不断开 `slow.next`：左半段仍连着右半段，递归永远缩不小，`RecursionError`。
- `fast` 也从 `head` 起步：`[2,1]` 时 `slow` 停在第二个结点，`mid` 为 `None`，左半段还是 `[2,1]`，无限递归。
- 以为递归版是 `O(1)` 空间：它的栈深 `log n`，`5 * 10^4` 个结点仍安全，但进阶要求的严格常数空间要用自底向上版。

**追问。**
- 排序稳定吗？稳定：合并时相等取左段（`<=`），相等元素保持原相对顺序。
- 自底向上版的复杂度？时间仍是 `O(n log n)`（`log n` 轮，每轮扫 `n` 个结点），空间 `O(1)`，满足进阶。
- 为什么不用快排或堆排？快排要随机选枢轴、堆排要下标随机访问，链表都不顺手；链表快排最坏 `O(n²)`，归并稳定地 `O(n log n)`。
- 有多个有序链表要合并（LC 23）：两两归并，或用大小为 `k` 的最小堆，`O(N log k)`。

**同模式。** LC 21 合并两个有序链表、LC 23 合并 K 个升序链表、LC 147 对链表进行插入排序、LC 912 排序数组。
