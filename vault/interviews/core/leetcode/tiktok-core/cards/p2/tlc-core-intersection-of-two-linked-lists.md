---
id: tlc-core-intersection-of-two-linked-lists
node: p2.intersection-of-two-linked-lists
type: qa
---
## Q
**LC 160 相交链表**｜Easy · LC TikTok 近 6 个月热度 53/100（全时段 50） · 近一年被问：美国 0 次、国内 1 次 · CodeTop 国内累计 116 次 · 最近 2026-09-17（国内 CodeTop） · 也在：LeetCode Hot 100

给两个单链表的头节点 `headA` 和 `headB`，找出并返回两个链表相交的起始节点；不相交则返回 `null`。数据保证整个链式结构中不存在环，函数返回后链表必须保持原结构。`listA` 有 `m` 个节点，`listB` 有 `n` 个节点，`1 <= m, n <= 3 * 10^4`，`1 <= Node.val <= 10^5`。相交指的是**同一个节点对象**（内存里的同一个位置），不是值相同。例：`listA = [4,1,8,4,5]`，`listB = [5,6,1,8,4,5]`，从 A 的第 3 个节点（值 `8`）起相交 → 返回值为 `8` 的那个节点；`listA = [2,6,4]`，`listB = [1,5]` 不相交 → `null`。进阶：`O(m + n)` 时间、`O(1)` 额外内存。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 两个指针分别从两个表头出发，走到末尾就改走**另一条**链表的表头；两个指针各自走完「自己的链表 + 对方的链表」，路程相同，所以相交时会在交点同时到达，不相交时同时走到 `None`。`O(m + n)` 时间，`O(1)` 空间。

**识别。** 「两条单链表」「相交」「`O(1)` 空间」→ 双指针对齐。难点是两条链表长度不同：交点前各自独有的部分长度不同，没法同步前进；交点之后是共享的尾部，长度相同。

**推导。** 暴力一：A 的每个节点和 B 的每个节点比较地址，`O(m · n)`。暴力二：把 A 的所有节点放进集合，再扫描 B，第一个在集合里的节点就是交点，`O(m + n)` 时间但 `O(m)` 空间，不满足进阶。洞察：设 A 独有 `x` 个节点，B 独有 `y` 个，共享 `c` 个。指针 `a` 走完 A 的 `x + c` 个节点，越过末尾一步，再走 B 的 `y` 个独有节点才到交点，共 `x + c + 1 + y` 步；指针 `b` 走完 B 的 `y + c` 个节点，越过末尾一步，再走 A 的 `x` 个独有节点，共 `y + c + 1 + x` 步。两者相等，所以它们同时站在交点上。不相交时 `c = 0`，两者走了 `m + n + 1` 步后同时变成 `None`，循环自然结束。

**简单解法。** 把 A 的所有节点放进集合，再顺着 B 走，第一个在集合里的节点就是交点。

```python
def get_intersection_node(head_a: ListNode | None, head_b: ListNode | None) -> ListNode | None:
    in_a: set[ListNode] = set()
    node = head_a
    while node:
        in_a.add(node)                              # 按对象身份存，不是按值
        node = node.next
    node = head_b
    while node:
        if node in in_a:
            return node                             # B 上第一个也在 A 里的节点
        node = node.next
    return None
```

时间 `O(m + n)`，空间 `O(m)`；够用，只是不满足进阶的 `O(1)` 额外内存。

最优解：

```python
def get_intersection_node(head_a: ListNode | None, head_b: ListNode | None) -> ListNode | None:
    a, b = head_a, head_b
    while a is not b:                   # 比的是节点本身（地址），不是值
        a = a.next if a else head_b     # 走到头就换到另一条链表的表头
        b = b.next if b else head_a
    return a                            # 相交节点；不相交时 a、b 同时为 None
```

运行：`[4,1,8,4,5]` 与 `[5,6,1,8,4,5]`（共享后三个节点）→ 值为 `8` 的节点，`[1,9,1,2,4]` 与 `[3,2,4]` → 值为 `2` 的节点，`[2,6,4]` 与 `[1,5]` → `None`，两条等长且不相交的链表 → `None`。

**复杂度。** 时间 `O(m + n)`：每个指针至多走 `m + n` 步；空间 `O(1)`：两个指针。

**拓展优化。**
- 先量长度，让长的链表先走 `|m - n|` 步，再齐头并进到第一个相同节点；同样 `O(m + n)` / `O(1)`，比换表头的写法直观：
```python
def get_intersection_node_by_length(head_a: ListNode | None, head_b: ListNode | None) -> ListNode | None:
    def length(node: ListNode | None) -> int:
        n = 0
        while node:
            n += 1
            node = node.next
        return n

    a, b = head_a, head_b
    la, lb = length(a), length(b)
    for _ in range(la - lb):                        # A 更长：A 先走掉多出来的部分
        a = a.next
    for _ in range(lb - la):
        b = b.next
    while a is not b:                               # 剩余长度相同：同步前进，必在交点相遇或同时走到 None
        a, b = a.next, b.next
    return a
```

**易错点。**
- 比较值而不是节点：把 `a is not b` 换成 `a.val != b.val`，示例一会在值为 `1` 的另一个节点上停下，返回值为 `1` 的节点，正确答案是值为 `8` 的节点。必须比较节点本身。
- 走到末尾不换表头，直接置 `None` 结束：长度不同的两个指针永远对不齐，示例一返回 `None`。
- 换表头的判断写成 `a.next is None`（走到最后一个节点就换）：指针永远不会变成 `None`，不相交时两个指针一直循环，永不停止。要等指针真的走到 `None`（越过末尾）再换。

**追问。**
- 只想判断是否相交、不要交点：比较两条链表的**最后一个节点**是否同一个对象。
- 链表可能有环：先分别判环（LC 141 / 142）；一个有环一个无环必不相交；都有环则看入环点是否在同一个环上。

**同模式。** LC 141 环形链表、LC 142 环形链表 II、LC 234 回文链表、LC 236 二叉树的最近公共祖先（用父指针时与相交链表同构）。
