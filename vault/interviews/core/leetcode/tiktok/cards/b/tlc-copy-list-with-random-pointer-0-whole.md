---
id: tlc-copy-list-with-random-pointer-0-whole
node: b.copy-list-with-random-pointer
type: qa
---
## Q
**LC 138 随机链表的复制**｜Medium · LC TikTok 全时段热度 26/100 · 近一年被问：美国 0 次、国内 1 次 · CodeTop 国内累计 27 次 · 最近 2026-09-06（国内 CodeTop）

链表每个节点除了 `next` 外还有一个 `random` 指针，可指向链表中任意节点或 `null`。构造这个链表的**深拷贝**：恰好 `n` 个全新节点，值与原节点相同，新节点的 `next` 和 `random` 都指向新链表中的节点，且不能指向原链表的节点。节点数 `0 <= n <= 1000`，`-10^4 <= Node.val <= 10^4`。输入用 `[val, random_index]` 表示，例：`[[7,null],[13,0],[11,4],[10,2],[1,0]]` → 同样的结构（但是全新的节点）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 用字典记下「原节点 → 新节点」：第一遍只创建所有新节点，第二遍按原链表的 `next` / `random` 关系给新节点连线；查字典时把 `None` 映射到 `None`，省掉空指针判断。`O(n)`。

**识别。** 「深拷贝」+「指针可指向任意节点」：一个指针在被连之前，它指向的节点可能还没创建（`random` 常常指向后面的节点），所以不能边走边建边连。标准解是先建点后连线，需要「旧节点 → 新节点」的映射；进阶是把映射藏在链表里，`O(1)` 额外空间。

**推导。** 暴力：边遍历边复制 `next`，遇到 `random` 再去链表里找下标，`O(n^2)` → 浪费在每次重新查找目标 → 先用一次遍历建立「原节点 → 新节点」的字典，再用一次遍历连线，每个指针 `O(1)` 查表 → 字典里放 `None: None`，`random` 为空时也能直接查到，不用写 `if`。

```python
def copy_random_list(head: Node | None) -> Node | None:
    clone: dict[Node | None, Node | None] = {None: None}     # 原节点 -> 新节点；None 映射到 None，省掉判空
    node = head
    while node:                                              # 第一遍：只造新节点，先不连指针
        clone[node] = Node(node.val)
        node = node.next
    node = head
    while node:                                              # 第二遍：按原链表的结构连 next / random
        clone[node].next = clone[node.next]
        clone[node].random = clone[node.random]
        node = node.next
    return clone[head]
```

运行：`[[7,null],[13,0],[11,4],[10,2],[1,0]]`、`[[1,1],[2,1]]`、`[[3,null],[3,0],[3,null]]` 的拷贝结构与输入完全一致，且新旧链表没有共享节点；空链表 → `None`；原链表没有被修改。

**复杂度。** 时间 `O(n)`，两遍扫描；空间 `O(n)`，字典。

**易错点。**
- 直接复制 `random`：`new.random = node.random` 会让新节点指向原链表里的节点，违反「不能指向原链表」。`[[1,1],[2,1]]` 中新链表第一个节点的 `random is 原链表第二个节点` 为 `True`，正确是 `False`。
- 字典的键是节点对象（按身份哈希），不能用值：`[[3,null],[3,0],[3,null]]` 里三个节点的 `val` 都是 `3`，用值当键会互相覆盖。
- 忘记 `None` 的映射：`clone[node.random]` 在 `random` 为空时抛 `KeyError`。

**追问。**
- `O(1)` 额外空间：把新节点插在每个原节点后面（`A -> A' -> B -> B'`），副本的 `random` 就是原 `random` 的下一个节点，最后把两条链表拆开。
- 一遍扫描：`collections.defaultdict(lambda: Node(0))` 在查询时自动造节点，一次循环里同时给新节点赋值、连 `next` 和 `random`。
- 图的克隆（LC 133）：同一个思想，用字典记录已克隆的节点，遍历时遇到没克隆过的才建。

**同模式。** LC 133 克隆图、LC 1485 克隆含随机指针的二叉树、LC 146 LRU 缓存（哈希表加链表）、LC 430 扁平化多级双向链表。
