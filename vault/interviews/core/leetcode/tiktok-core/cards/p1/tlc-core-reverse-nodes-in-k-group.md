---
id: tlc-core-reverse-nodes-in-k-group
node: p1.reverse-nodes-in-k-group
type: qa
---
## Q
**LC 25 K 个一组翻转链表**｜Hard · LC TikTok 近 30 天热度 100/100（全时段 58） · 近一年被问：美国 7 次、国内 12 次 · CodeTop 国内累计 305 次 · 最近 2026-10-27（国内面试记录） · 也在：Amazon、LeetCode Hot 100、NeetCode 150、Top Interview 150

给链表的头节点 `head`，每 `k` 个节点一组进行翻转，返回修改后的链表。`k` 是正整数，小于或等于链表的长度；如果节点总数不是 `k` 的整数倍，最后剩余的节点保持原有顺序。不能只是改变节点内部的值，需要实际进行节点交换。链表中的节点数目为 `n`，`1 <= k <= n <= 5000`，`0 <= Node.val <= 1000`。例：`head = [1,2,3,4,5], k = 2` → `[2,1,4,3,5]`；`head = [1,2,3,4,5], k = 3` → `[3,2,1,4,5]`。进阶：能否设计一个只用 `O(1)` 额外内存空间的算法？

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 哑节点（dummy）加迭代：每轮先往后数 `k` 个节点确认这一组完整；完整就用标准的链表反转翻这一段，并让 `prev` 初值取「下一组的头」，使翻完后的组尾自动连上后面；再把上一组的尾接到新的组头。不足 `k` 个就停，原样保留。`O(n)` 时间、`O(1)` 空间。

**识别。** 「分段处理链表 + 段内反转」：把 LC 206（反转链表）当子程序，外层负责分组与接线。「不足 `k` 个保持原样」要求**先检查够不够再反转**，否则会错翻最后一组。哑节点让第一组与其他组的接线逻辑一致。`O(1)` 空间排除递归（深度 `n/k`）和用栈。

**推导。** 暴力：把所有节点值读入数组，按组反转后写回 → 违反「不能只改值」，且 `O(n)` 额外空间 → 原地：先数够 `k` 个确认是完整一组，再用 LC 206 的反转翻这一段；反转的 `prev` 初值取下一组的头，翻完组尾自动连上后面。

**简单解法。** 把节点按顺序放进列表，对每个完整的 `k` 段切片反转，再按新顺序重新接线。

```python
def reverse_k_group(head: ListNode | None, k: int) -> ListNode | None:
    nodes: list[ListNode] = []
    while head:
        nodes.append(head)
        head = head.next
    for i in range(0, len(nodes) - k + 1, k):          # 只处理完整的一组
        nodes[i:i + k] = nodes[i:i + k][::-1]          # 切片反转：换的是节点本身
    dummy = cur = ListNode(0)
    for node in nodes:
        cur.next = node                                # 按新顺序重新接线
        cur = node
    cur.next = None                                    # 新的尾巴必须断开，否则会成环
    return dummy.next
```

时间 `O(n)`、空间 `O(n)`；题面进阶要 `O(1)` 额外空间，所以只能当开场答案，再写指针原地版。

最优解：

```python
def reverse_k_group(head: ListNode | None, k: int) -> ListNode | None:
    dummy = ListNode(0, head)
    group_prev = dummy                       # 本组前一个节点（上一组翻转后的尾）
    while True:
        kth: ListNode | None = group_prev
        for _ in range(k):                   # 往后数 k 个；不够 k 个就结束，余下原样保留
            kth = kth.next
            if kth is None:
                return dummy.next
        group_next = kth.next                # 下一组的头
        prev, cur = group_next, group_prev.next      # prev 先指向下一组：翻完后本组尾巴自动接上
        while cur is not group_next:
            nxt = cur.next
            cur.next = prev
            prev, cur = cur, nxt
        tail = group_prev.next               # 翻转前的头，现在是本组的尾
        group_prev.next = kth                # 前一段接上新的头（kth）
        group_prev = tail
```

运行：`([1,2,3,4,5], 2)` → `[2, 1, 4, 3, 5]`，`([1,2,3,4,5], 3)` → `[3, 2, 1, 4, 5]`，`([1], 1)` → `[1]`，`([1,2,3], 3)` → `[3, 2, 1]`，`([1,2,3,4,5], 5)` → `[5, 4, 3, 2, 1]`，`([1,2,3,4,5], 1)` → `[1, 2, 3, 4, 5]`，`([1,2,3,4,5,6,7], 3)` → `[3, 2, 1, 6, 5, 4, 7]`。

**复杂度。** 时间 `O(n)`：每个节点被「数」一次、被「翻」一次；空间 `O(1)`。

**拓展优化。**
- 递归版：代码短，但递归深度 `n/k`；`k = 2`、`5000` 个节点深度 2500，超过 CPython 默认递归上限。

```python
def reverse_k_group(head: ListNode | None, k: int) -> ListNode | None:
    tail = head
    for _ in range(k):                                 # 数 k 个，不够就保持原样
        if tail is None:
            return head
        tail = tail.next
    prev, cur = reverse_k_group(tail, k), head         # prev 初值 = 后面已处理好的部分
    for _ in range(k):
        cur.next, prev, cur = prev, cur, cur.next      # 经典反转，组尾自动接上后半部分
    return prev
```

**易错点。**
- 先数够 `k` 个再翻：不先检查时，最后不足的一组也被翻掉，`[1,2,3,4,5]`、`k = 3` 会得到 `[3,2,1,5,4]`，正确是 `[3,2,1,4,5]`。
- 反转的 `prev` 初值要是 `group_next`（下一组的头）：写成 `None` 时，翻完的组尾指向 `None`，后面所有节点丢失，`[1,2,3,4,5]`、`k = 2` 只剩 `[2,1]`，正确是 `[2,1,4,3,5]`。
- 接线前要先记下本组原来的头（它翻完是组尾，`tail`），否则下一轮不知道从哪里继续。

**追问。**
- 从尾部开始分组（不足的在头部）：先反转整条链表，做一遍，再反转回来；或先求长度，对头部多出的 `n % k` 个跳过。
- 放宽到 `O(k)` 额外空间：把 `k` 个节点压入栈，弹出时顺次连接，代码更直观。

**同模式。** LC 206 反转链表、LC 92 反转链表 II、LC 24 两两交换链表中的节点、LC 61 旋转链表。
