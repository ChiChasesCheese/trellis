---
id: tlc-swap-nodes-in-pairs-0-whole
node: a.swap-nodes-in-pairs
type: qa
---
## Q
**LC 24 两两交换链表中的节点**｜Medium · 字节 高频

给一个链表，两两交换其中相邻的节点，返回交换后链表的头节点。不能修改节点内部的值，只能交换节点本身。链表中节点的数目在范围 `[0, 100]` 内，`0 <= Node.val <= 100`。例：`head = [1,2,3,4]` → `[2,1,4,3]`；`head = []` → `[]`；`head = [1]` → `[1]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 用哑节点（dummy node）加三个指针：每次处理 `prev → a → b → rest`，改成 `prev → b → a → rest`，然后把 `prev` 移到 `a`（这一对现在的尾部），重复直到 `prev` 后面不足两个节点。`O(n)` 时间、`O(1)` 空间。

**识别。** 链表指针重连、头节点会变，就用哑节点，让头节点也有“前一个节点”。「成对」意味着每次步进 `2`。「不能改值」意味着只能改 `next` 指针。`n <= 100`，递归也能过，但迭代是 `O(1)` 空间，并且同样的写法能直接推广到 K 个一组翻转（LC 25）。

**推导。** 暴力：把节点值读进数组，交换后再写回，违反要求；或者另建新链表，用了 `O(n)` 空间。洞察：交换一对只涉及三个指针：`prev.next`、`a.next`、`b.next`，且必须先保住 `b.next`（后续链表的入口）才能改。Python 的元组赋值先把右边三项全部求值，再依次赋给左边，一行就能完成重连：`prev.next, a.next, b.next = b, b.next, a`。完成后 `a` 成为这一对的尾部，下一对紧跟在它后面，所以 `prev = a`。

```python
def swap_pairs(head: ListNode | None) -> ListNode | None:
    dummy = ListNode(0, head)              # 哑节点：让头节点也有“前一个节点”
    prev = dummy
    while prev.next and prev.next.next:
        a, b = prev.next, prev.next.next   # 要交换的一对：prev -> a -> b -> rest
        prev.next, a.next, b.next = b, b.next, a   # 右边先整体求值，再依次赋值：prev -> b -> a -> rest
        prev = a                           # a 现在是这一对的尾巴，下一对紧跟在它后面
    return dummy.next
```

运行：`[1,2,3,4]` → `[2, 1, 4, 3]`，`[]` → `[]`，`[1]` → `[1]`，`[1,2,3]` → `[2, 1, 3]`，`[1,2]` → `[2, 1]`；交换前后节点对象是同一批，只改了指针；`10^5` 个节点的链表同样能处理（递归写法在这个规模会抛 `RecursionError`）。

**复杂度。** 时间 `O(n)`，每个节点访问一次；空间 `O(1)`。

**易错点。**
- 交换后把 `prev` 移到 `b` 而不是 `a`：`[1,2,3,4]` 得到 `[2,3,4,1]`，正确是 `[2,1,4,3]`。交换后 `a` 才是这一对的尾部。
- 循环条件只判断 `prev.next`，没有判断 `prev.next.next`：节点数为奇数时，`b = prev.next.next` 是 `None`，后面访问 `b.next` 抛 `AttributeError`，`[1]` 和 `[1,2,3]` 都会出错。两个条件缺一不可，并且顺序不能反。
- 修改节点的值来交换：`a.val, b.val = b.val, a.val` 结果看起来一样，但题目明确禁止，并且节点带有其他状态或被外部引用时是错的。

**追问。**
- K 个一组翻转（LC 25）：先往后数 `k` 个节点，不足就结束；足够时在组内原地反转，再接回前后；`k = 2` 就是两两交换。
- 递归写法：`second = head.next; head.next = swap(second.next); second.next = head; return second`，三行，但栈深 `O(n / 2)`。
- 奇偶位置的节点分别聚集（LC 328）：不是交换，而是拆成两条链再拼接，同样靠哑节点或双指针完成。

**同模式。** LC 25 K 个一组翻转链表、LC 206 反转链表、LC 92 反转链表 II、LC 143 重排链表、LC 328 奇偶链表。
