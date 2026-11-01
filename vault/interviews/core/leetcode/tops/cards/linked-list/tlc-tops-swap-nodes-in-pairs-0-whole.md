---
id: tlc-tops-swap-nodes-in-pairs-0-whole
node: linked-list.swap-nodes-in-pairs
type: qa
---
## Q
**LC 24 两两交换链表中的节点**｜Medium · 全公司热度第 215 名 · Hot 100

给你一个链表，两两交换其中相邻的节点，并返回交换后链表的头节点。你必须在不修改节点内部的值的情况下完成（即只能进行节点交换）。链表中节点的数目在范围 `[0, 100]` 内，`0 <= Node.val <= 100`。

例：`head = [1,2,3,4]` → `[2,1,4,3]`；`head = []` → `[]`；`head = [1]` → `[1]`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点：** 链表局部重连（pointer rewiring）+ 哑结点；`prev → a → b → rest` 改成 `prev → b → a → rest` 的三步指针顺序。

**一句话。** 用 `prev` 指向每一对前面的结点，每轮把后面两个结点 `a, b` 重新接成 `prev → b → a → rest`，然后 `prev` 跳到 `a`。

**识别。** 「相邻两个一组」「不能改值」就是纯指针重连；和 LC 25 同类，`k = 2`。`n <= 100`，线性。

**推导。** 交换值最省事，但题目禁止。要换结点，每一对涉及三条边：前驱指向 `b`、`b` 指向 `a`、`a` 指向后继。写的顺序必须先保存后继信息（`a.next = b.next` 先做），再让 `b.next = a`，最后让 `prev.next = b`。第一对没有前驱，用哑结点补上。

```python
def swap_pairs(head: ListNode | None) -> ListNode | None:
    dummy = ListNode(0, head)       # 哑结点：第一对也有前驱
    prev = dummy
    while prev.next and prev.next.next:     # 后面至少还有两个结点才交换
        a, b = prev.next, prev.next.next
        # prev -> a -> b -> rest  改成  prev -> b -> a -> rest
        a.next = b.next             # 1. a 先接上 rest（此时 b.next 还没动）
        b.next = a                  # 2. b 指回 a
        prev.next = b               # 3. 前驱改指 b
        prev = a                    # a 现在是这一对的尾，下一对从它后面开始
    return dummy.next
```

**运行。** `[1,2,3,4]` → `[2, 1, 4, 3]`；`[]` → `[]`；`[1]` → `[1]`；`[1,2,3]` → `[2, 1, 3]`。

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**拓展优化。**
- 递归写法：交换第一对，第二个结点接回「剩余部分交换后的结果」。深度 `n / 2`。
```python
def swap_pairs_recursive(head: ListNode | None) -> ListNode | None:
    if not head or not head.next:       # 不足一对，原样返回
        return head
    second = head.next
    head.next = swap_pairs_recursive(second.next)   # 第一个结点接上后面已交换好的部分
    second.next = head                              # 第二个结点指回第一个
    return second                                   # second 成为这一对的头
```
- 每 `k` 个一组反转（LC 25）：把「一对」换成「一组 `k` 个」。

**易错点。**
- 步骤 2 先于步骤 1：`b.next = a` 之后再写 `a.next = b.next`，等于 `a.next = a`，`[1,2,3,4]` 变成自环，遍历永远不结束。
- 循环末尾写 `prev = b`：下一轮会把 `1` 和 `3` 再换一次，`[1,2,3,4]` 输出 `[2, 3, 4, 1]`。`a` 才是这一对的新尾。
- 奇数长度的最后一个结点：条件必须是 `prev.next and prev.next.next`，少判一个会对 `[1,2,3]` 的 `3` 读空指针。

**同模式。** LC 25 K 个一组翻转链表、LC 206 反转链表、LC 92 反转链表 II、LC 328 奇偶链表。
