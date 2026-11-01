---
id: tlc-tops-intersection-of-two-linked-lists-0-whole
node: linked-list.intersection-of-two-linked-lists
type: qa
---
## Q
**LC 160 相交链表**｜Easy · 全公司热度第 277 名 · Hot 100

给你两个单链表的头节点 `headA` 和 `headB`，找出并返回两个单链表相交的起始节点；不相交则返回 `null`。题目数据保证整个链式结构中不存在环，函数返回后链表必须保持原始结构。`listA` 有 `m` 个节点，`listB` 有 `n` 个节点，`1 <= m, n <= 3 * 10^4`，`1 <= Node.val <= 10^5`。相交指两条链从某个节点起共用同一段内存（是同一个节点对象，不是值相等）。进阶：设计 `O(m + n)` 时间、`O(1)` 内存的解法。

例：`listA = [4,1,8,4,5]`，`listB = [5,6,1,8,4,5]`，两链从值为 `8` 的节点起共用 → 返回该节点（A 中它前面有 2 个节点，B 中有 3 个）；`listA = [2,6,4]`，`listB = [1,5]` 不相交 → `null`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点：** 双指针「换道相接」（two pointers switching heads）；用路程相等对齐长度不同的两条链。

**一句话。** 指针 `a` 走完 A 就去走 B，指针 `b` 走完 B 就去走 A；两者各走 `m + n` 步后一定同时到达交点，不相交则同时到达 `None`。

**识别。** 「找两条链的第一个公共结点」「`O(1)` 内存」「不能改结构」。`m, n` 到 `3 * 10^4`，线性即可。

**推导。** 把 A 的结点放进集合，再扫 B 找第一个在集合里的，`O(m + n)` 时间、`O(m)` 空间。要省空间，关键是交点后的尾巴等长，只是交点前的部分不等长（设 A 有 `x` 个独有结点，B 有 `y` 个，公共段 `c` 个）。让每个指针走完自己的链后接着走对方的链：`a` 走 `x + c + y`，`b` 走 `y + c + x`，同样长，正好在交点同时到达。

**简单解法。** 同一思路，用集合存 A 的结点对象：
```python
def get_intersection_node_set(headA: ListNode | None, headB: ListNode | None) -> ListNode | None:
    seen = set()
    while headA:
        seen.add(headA)
        headA = headA.next
    while headB:
        if headB in seen:       # 同一个结点对象才算相交
            return headB
        headB = headB.next
    return None
```

**最优解：** 换道相接。

```python
def get_intersection_node(headA: ListNode | None, headB: ListNode | None) -> ListNode | None:
    a, b = headA, headB
    while a is not b:                   # 相交：同时落在交点；不相交：同时落在 None，也会退出
        a = a.next if a else headB      # 走到尽头（None）的那一步也要计入，然后换到对方链头
        b = b.next if b else headA
    return a
```

**运行。** 例 1 → 返回值为 `8` 的节点（且是 A、B 共用的那个）；例 2（`[1,9,1,2,4]` 与 `[3,2,4]`，在值为 `2` 的节点相交）→ 值为 `2` 的节点；`[2,6,4]` 与 `[1,5]` 不相交 → `None`。

**复杂度。** 时间 `O(m + n)`（每个指针至多走 `m + n + 1` 步），空间 `O(1)`。

**拓展优化。**
- 另一种等价写法：先各走一遍量出长度，让长的先走 `|m - n|` 步，再同步前进。思想相同，代码更长。
- 如果链表可能有环（LC 142 配合使用）：先用快慢指针判环，再分别处理；题目已保证无环。

**易错点。**
- 比较值而不是结点：A `[4,1,8,4,5]`、B `[5,6,1,8,4,5]` 中，值为 `1` 的两个结点是不同对象，按值比较会错误地返回 `1` 那个结点。
- 写成 `a = a.next if a.next else headB`：两链不相交时 `a`、`b` 永远走不到 `None`，在两条链上无限循环。
- 用「先把 A 的尾接到 A 的头成环」等改结构的办法：题目要求返回后保持原结构，必须还原，容易漏。

**同模式。** LC 141 环形链表、LC 142 环形链表 II、LC 19 删除链表的倒数第 N 个结点、LC 234 回文链表。
