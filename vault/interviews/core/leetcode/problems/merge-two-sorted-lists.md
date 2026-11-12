---
slug: merge-two-sorted-lists
---
## Q
**LC 21 合并两个有序链表**｜Easy

将两个升序链表合并为一个新的升序链表并返回。新链表是通过拼接给定的两个链表的所有节点组成的。两个链表的节点数目范围是 `[0, 50]`，`-100 <= Node.val <= 100`，`l1` 和 `l2` 均按非递减顺序排列。

例：`l1 = [1,2,4]`，`l2 = [1,3,4]` → `[1,1,2,3,4,4]`；`l1 = []`，`l2 = []` → `[]`；`l1 = []`，`l2 = [0]` → `[0]`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点：** 双指针归并（two-pointer merge）加哑结点（dummy node）；归并排序的 `merge` 步骤，也是 LC 23、148 的子程序。

**一句话。** 两个指针各指一条链的队头，每次把较小的那个接到结果链尾，一方走空后把另一方整段接上。

**识别。** 「两个有序序列合成一个有序序列」就是归并；「拼接节点」说明不新建节点，只改 `next`。`n <= 50`，线性即可。

**推导。** 把两条链的值倒进数组再排序，是 `O((m+n) log(m+n))`，也浪费了「已有序」这个条件。已有序时，合并后的最小值只可能是两个队头之一，所以每步比较两个队头、取小者，总共 `m+n` 步。结果链头不固定，用一个哑结点当起点，循环里不必区分「第一个结点」。

```python
def merge_two_lists(
    list1: ListNode | None, list2: ListNode | None
) -> ListNode | None:
    # 哑结点：结果链从 dummy.next 开始，不用特判头
    dummy = tail = ListNode()
    while list1 and list2:
        # 两个队头里较小的那个接到结果尾；相等时取 list1，保持稳定
        if list1.val <= list2.val:
            tail.next, list1 = list1, list1.next
        else:
            tail.next, list2 = list2, list2.next
        tail = tail.next
    # 至多一条还有剩，剩下的本来有序，整段接上
    tail.next = list1 or list2
    return dummy.next
```

**运行。** `[1,2,4]` + `[1,3,4]` → `[1, 1, 2, 3, 4, 4]`；`[]` + `[]` → `[]`；`[]` + `[0]` → `[0]`；`[5]` + `[1,2]` → `[1, 2, 5]`。

**复杂度。** 时间 `O(m+n)`，空间 `O(1)`（只改指针，哑结点是常数）。

**拓展优化。**
- 递归写法：谁的头小，谁就是结果的头，它的 `next` 是「剩下部分的合并」。深度最多 `m+n`。
```python
def merge_two_lists_recursive(
    list1: ListNode | None, list2: ListNode | None
) -> ListNode | None:
    if not list1 or not list2:           # 一方为空：另一方就是结果
        return list1 or list2
    if list1.val <= list2.val:
        list1.next = merge_two_lists_recursive(list1.next, list2)
        return list1
    list2.next = merge_two_lists_recursive(list1, list2.next)
    return list2
```
- 合并 `k` 条链（LC 23）：用大小为 `k` 的最小堆存各链队头，`O(N log k)`；或两两归并。

**易错点。**
- 循环后忘了接剩余部分：`[1,2,4]` 与 `[1,3,4]` 会输出 `[1, 1, 2, 3, 4]`，丢掉最后的 `4`。
- 不用哑结点、直接 `head = None` 再判断：每一步都要多一个「是不是第一个」的分支，容易写出空指针。
- 递归版深度等于 `m+n`：题目上限是 100，安全；换成万级长度的链就会触到 CPython 约 1000 的递归上限，要改迭代。

**追问。**
- 合并后去重（相同的值只留一个）：接结点前先和 `tail.val` 比较，相同就跳过，仍是 `O(m+n)`。
- 不能改原链表（要新建结点）：每次 `tail.next = ListNode(值)`，时间不变，空间变成 `O(m+n)`。
- 用它排序链表（LC 148）：快慢指针找中点断开，两半递归排序再用本题合并，`O(n log n)` 时间；递归栈 `O(log n)`。
- 合并 `k` 条链（LC 23）：分治两两合并，共 `log k` 轮，每轮总长 `N`，`O(N log k)`；一条一条往前并会退化成 `O(kN)`。

**同模式。** LC 23 合并 K 个升序链表、LC 148 排序链表、LC 88 合并两个有序数组、LC 86 分隔链表。
