---
slug: copy-list-with-random-pointer
---
## Q
**LC 138 随机链表的复制**｜Medium

给你一个长度为 `n` 的链表，每个节点包含一个额外增加的随机指针 `random`，该指针可以指向链表中的任何节点或空节点。构造这个链表的深拷贝：由 `n` 个全新节点组成，每个新节点的值等于对应原节点的值；新节点的 `next` 和 `random` 都指向复制链表中的新节点，使原链表和复制链表能表示相同的链表状态，复制链表中的指针都不应指向原链表中的节点。你的代码只接受原链表的头节点 `head` 作为参数，返回复制链表的头节点。`0 <= n <= 1000`，`-10^4 <= Node.val <= 10^4`，`Node.random` 为 `null` 或指向链表中的节点。

输入/输出里每个节点用 `[val, random_index]` 表示（`random_index` 为指针指向的节点下标，`null` 表示不指向任何节点）。例：`head = [[7,null],[13,0],[11,4],[10,2],[1,0]]` → 同样的结构；`head = [[1,1],[2,1]]` → `[[1,1],[2,1]]`；`head = [[3,null],[3,0],[3,null]]` → `[[3,null],[3,0],[3,null]]`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点：** 深拷贝（deep copy）带「旧结点 → 新结点」映射表；图的拷贝在链表上的最小形态（同 LC 133 克隆图）。

**一句话。** 第一遍给每个旧结点造一个新结点并记进字典，第二遍用字典把 `next` 和 `random` 翻译成新结点。

**识别。** `random` 可以指向后面还没造出来的结点，一遍扫不完；「深拷贝」「不能指回旧链」就是要有旧到新的映射。`n <= 1000`，线性。

**推导。** 一边走一边造并连 `next` 很容易，但碰到 `random` 指向的结点可能还没有对应新结点。把过程拆成两遍：先全部造出来（此时所有新结点都存在），再连指针，翻译就变成一次字典查询。给 `None` 也配一个映射 `None → None`，连指针时就不需要判空。

```python
def copy_random_list(head: Node | None) -> Node | None:
    # 旧结点 -> 新结点；None 映射到 None，连指针时不用判空
    clone = {None: None}
    cur = head
    while cur:                      # 第一遍：只造结点，不连指针
        clone[cur] = Node(cur.val)
        cur = cur.next
    cur = head
    while cur:                      # 第二遍：经字典把旧指针翻译成新结点
        clone[cur].next = clone[cur.next]
        clone[cur].random = clone[cur.random]
        cur = cur.next
    return clone[head]
```

**运行。** 例 1 `[[7,null],[13,0],[11,4],[10,2],[1,0]]` → `[[7,null],[13,0],[11,4],[10,2],[1,0]]`；例 2 → `[[1,1],[2,1]]`；例 3 → `[[3,null],[3,0],[3,null]]`；空链表 → `None`。复制出的每个结点都不是原结点对象。

**复杂度。** 时间 `O(n)`，空间 `O(n)`（字典）。

**拓展优化。**
- `O(1)` 额外空间：把副本直接插在原结点后面（`A → A' → B → B'`），副本的 `random` 就是原 `random` 的下一个，最后拆成两条链。
```python
def copy_random_list_o1(head: Node | None) -> Node | None:
    cur = head
    # 1. 每个旧结点后面插入它的副本：A -> A' -> B -> B'
    while cur:
        copy = Node(cur.val)
        copy.next = cur.next
        cur.next = copy
        cur = copy.next
    cur = head
    # 2. 副本的 random = 原结点 random 的副本（紧跟在它后面）
    while cur:
        cur.next.random = cur.random.next if cur.random else None
        cur = cur.next.next
    dummy = tail = Node(0)
    cur = head
    while cur:                      # 3. 拆开：旧链还原，副本串成新链
        copy = cur.next
        cur.next = copy.next
        tail.next = copy
        tail = copy
        cur = cur.next
    return dummy.next
```
- 递归 + 记忆化：`copy(node)` 先查字典，没有就造新结点并递归复制 `next`、`random`，写法短但深度可达 `n`。

**易错点。**
- 用 `val` 当字典键：例 3 的三个结点值都是 `3`，键冲突，后一个覆盖前一个，`random` 指错结点。键必须是结点对象。
- 一遍同时造结点和连 `random`：`[[7,null],[13,0],[11,4],...]` 中结点 `11` 的 `random` 指向还没造出的下标 4，字典查询抛 `KeyError`。
- 第二遍写成 `clone[cur].random = cur.random`：新结点的 `random` 指回旧链，违反「不指向原链表」，判题时被检出。

**追问。**
- 为什么映射表里要放 `None → None`？`next`、`random` 可能为空，有这一项就不必每次判空；否则要写成 `clone.get(cur.random)`。
- 想省掉字典怎么办？用拓展优化里的「副本插在原结点后面」：副本的 `random` 就是 `cur.random.next`，最后拆链，空间 `O(1)`，时间仍 `O(n)`；代价是中途会临时改动原链表，必须拆回去。
- 面试官要求不许修改原链表呢？那只能用字典（`O(n)` 空间）；穿插法在拆链之前原链是被改过的。

**同模式。** LC 133 克隆图、LC 1485 克隆含随机指针的二叉树、LC 2 两数相加、LC 148 排序链表。
