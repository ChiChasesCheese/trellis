---
id: tlc-insert-into-a-sorted-circular-linked-list-0-whole
node: c.insert-into-a-sorted-circular-linked-list
type: qa
---
## Q
**LC 708 循环有序列表的插入**｜Medium · LC TikTok 全时段热度 26/100

给定循环单调非递减链表中的任意一个节点 `head`（不一定是最小值节点），向其中插入新值 `insertVal`，使链表仍然是循环非降序的。有多个合适位置时可以选任意一个。如果链表为空（`head` 为 `null`），创建一个只含新值的循环链表并返回该节点；否则返回原来给定的节点。节点数 `0..5 * 10^4`，`-10^6 <= Node.val, insertVal <= 10^6`。例：`head = [3,4,1]`，`insertVal = 2` → 插在 `1` 和 `3` 之间，返回值为 `3` 的节点；`head = []`，`insertVal = 1` → `[1]`；`head = [1]`，`insertVal = 0` → `[1,0]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 沿环走一圈找插入点：找到相邻的 `cur <= insertVal <= nxt`，或者找到「最大 → 最小」的断点且新值比最大的还大或比最小的还小；走完一圈没找到（全部相等）就插在任意位置。

**识别。** 「环形有序结构上的插入」：关键是识别环里唯一的「下降点」（最大值指向最小值），新值要么夹在两个相邻节点之间，要么位于下降点两端之外。

**推导。** 把环拆开成有序链表要先找到最小节点，再从那里线性扫描，两步。一趟扫描就可以：对每一对 `(cur, nxt)` 判断两种合法位置——普通位置 `cur.val <= insertVal <= nxt.val`；下降点 `cur.val > nxt.val`，此时 `insertVal >= cur.val`（比最大还大）或 `insertVal <= nxt.val`（比最小还小）都应插在这里。绕回 `head` 仍没找到，说明所有值相同，插在哪里都合法。

```python
class Node:
    def __init__(self, val: int = 0, next: "Node | None" = None) -> None:
        self.val = val
        self.next = next


def insert(head: Node | None, insertVal: int) -> Node:
    node = Node(insertVal)
    if head is None:                             # 空链表：自己指向自己
        node.next = node
        return node
    cur = head
    while True:
        nxt = cur.next
        if cur.val <= insertVal <= nxt.val:      # 普通位置：夹在中间
            break
        if cur.val > nxt.val and (insertVal >= cur.val or insertVal <= nxt.val):
            break                                # 下降点（最大 -> 最小）：比最大还大或比最小还小
        cur = nxt
        if cur is head:                          # 绕了一圈没有合适位置：所有值相同，随便插
            break
    node.next = cur.next                         # 插在 cur 之后
    cur.next = node
    return head
```

运行：`[3,4,1]` 插入 `2` → 环为 `3,4,1,2`，`[3,4,1]` 插入 `5` → `3,4,5,1`，`[]` 插入 `1` → `[1]`（自环），`[1]` 插入 `0` → `1,0`，`[2,2,2]` 插入 `1` → 在环中任意位置插入后环仍合法（含 4 个节点）。

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**拓展优化。**
- 需要频繁插入：保持一个指向最小节点（或最大节点）的指针，找到起点后线性扫描；仍然是 `O(n)`，想 `O(log n)` 需要换成跳表或平衡树。
- 先找到最大节点 `tail`（`tail.val > tail.next.val` 的位置），则 `tail.next` 是最小节点，可以把环当作有序链表处理，逻辑更直观但多一趟。

**易错点。**
- 只写普通位置：新值比所有值都大或都小时永远找不到，死循环或一直转圈。
- 下降点条件写成 `insertVal > cur.val and insertVal < nxt.val`：反了，这里是「大于等于最大」或「小于等于最小」。
- 单节点环、全相等环没有下降点：靠 `cur is head` 终止，漏掉会无限循环。

**追问。**
- 插入重复值时是否插在已有值之前或之后：任意位置都合法，题目不要求稳定。
- 返回值是否一定是 `head`：是，非空时返回原节点，不是新节点也不是最小节点。

**同模式。** LC 147 对链表进行插入排序、LC 21 合并两个有序链表、LC 141 环形链表、LC 142 环形链表 II、LC 61 旋转链表。
