---
id: tlc-tops-reverse-nodes-in-k-group-0-whole
node: linked-list.reverse-nodes-in-k-group
type: qa
---
## Q
**LC 25 K 个一组翻转链表**｜Hard · 全公司热度第 66 名 · NeetCode 150、Hot 100、Top Interview 150

给你链表的头节点 `head`，每 `k` 个节点一组进行翻转，请你返回修改后的链表。`k` 是一个正整数，它的值小于或等于链表的长度。如果节点总数不是 `k` 的整数倍，那么请将最后剩余的节点保持原有顺序。你不能只是单纯地改变节点内部的值，而是需要实际进行节点交换。链表中的节点数目为 `n`，`1 <= k <= n <= 5000`，`0 <= Node.val <= 1000`。进阶：你可以设计一个只用 `O(1)` 额外内存空间的算法解决此问题吗？

例：`head = [1,2,3,4,5]`，`k = 2` → `[2,1,4,3,5]`；`head = [1,2,3,4,5]`，`k = 3` → `[3,2,1,4,5]`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点：** 链表分组反转：先探测够不够 `k` 个，再用「反转链表」子程序反转一段，并与前后两段重新接上。

**一句话。** 每轮先往后数 `k` 个确认够一组，够就把这一段反转并接回前后，不够就原样保留，结束。

**识别。** 「每 `k` 个一组」「不足 `k` 个保持原样」「不能改值」：局部反转加衔接。难点全在衔接：反转前要保存「组前驱」和「组后继」。`n <= 5000`，线性。

**推导。** 整段反转是 LC 206，现在要把它限制在一组内。关键是三个位置：组前驱 `group_prev`（上一组的尾）、本组头 `group_start`（反转后变成本组的尾）、本组尾 `tail`（反转后变成本组的头）。反转本组时把 `prev` 初始化成「下一组的头」，反转完本组的尾巴就自动指向下一组；然后让 `group_prev.next = tail`，并把 `group_prev` 前移到 `group_start`。

```python
def reverse_k_group(head: ListNode | None, k: int) -> ListNode | None:
    dummy = ListNode(0, head)
    group_prev = dummy                  # 上一组的尾；对第一组就是哑结点
    while True:
        # 1. 探测：从 group_prev 往后走 k 步，走不满说明这一组不足 k 个，保持原样
        tail = group_prev
        for _ in range(k):
            tail = tail.next
            if not tail:
                return dummy.next
        group_start, next_group = group_prev.next, tail.next
        # 2. 反转 [group_start, tail]；prev 从 next_group 起步，这一组的尾巴就自动接上下一组
        prev, cur = next_group, group_start
        while cur is not next_group:
            cur.next, prev, cur = prev, cur, cur.next
        # 3. 前驱接上新的组头 tail；group_start 现在是本组的尾，成为下一轮的前驱
        group_prev.next = tail
        group_prev = group_start
```

**运行。** `[1,2,3,4,5]`、`k = 2` → `[2, 1, 4, 3, 5]`；`k = 3` → `[3, 2, 1, 4, 5]`；`[1,2,3]`、`k = 3` → `[3, 2, 1]`；`[1,2,3]`、`k = 1` → `[1, 2, 3]`。

**复杂度。** 时间 `O(n)`（每个结点被探测一次、反转一次），空间 `O(1)`。

**拓展优化。**
- 递归写法：先探测是否够 `k` 个，不够原样返回；够就递归处理后面，再反转本组并接到结果前。栈深度 `n / k`。
```python
def reverse_k_group_recursive(head: ListNode | None, k: int) -> ListNode | None:
    tail = head
    for _ in range(k):                  # tail 走 k 步，成为下一组的头；不足 k 个直接原样返回
        if not tail:
            return head
        tail = tail.next
    prev = reverse_k_group_recursive(tail, k)   # 先把后面的部分处理好，本组反转后接在它前面
    cur = head
    while cur is not tail:
        cur.next, prev, cur = prev, cur, cur.next
    return prev
```
- 末尾不足 `k` 个也要反转的变体：探测失败时改为反转剩余部分。

**易错点。**
- 反转时 `prev` 初始写成 `None`：每组尾巴指向空，`[1,2,3,4,5]`、`k = 2` 只得到 `[2, 1]`，后面的结点丢了。
- 先反转再检查够不够：`[1,2,3,4,5]`、`k = 3` 会把最后的 `[4,5]` 也反转成 `[3, 2, 1, 5, 4]`，正确是 `[3, 2, 1, 4, 5]`。
- 递归版深度是 `n / k`：`k = 2`、`n = 5000` 时深度 2500，超过 CPython 默认约 1000 的递归上限会 `RecursionError`；`k = 1` 更是 5000，所以主解用迭代。

**同模式。** LC 206 反转链表、LC 92 反转链表 II、LC 24 两两交换链表中的节点、LC 61 旋转链表。
