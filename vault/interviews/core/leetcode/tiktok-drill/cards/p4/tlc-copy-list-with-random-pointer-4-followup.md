---
id: tlc-copy-list-with-random-pointer-4-followup
node: p4.copy-list-with-random-pointer
type: qa
step: 4
---
## Q
**LC 138 随机链表的复制**｜追问

面试官接着问：（1）能不能做到 `O(1)` 额外空间？（2）能不能一遍扫描完成？（3）如果结构不是链表而是一般的图（LC 133）呢？

## A
1. **`O(1)` 空间（交织法）**：三步。先在每个原节点后面插入它的副本（`A -> A' -> B -> B'`）；再设置副本的 `random`：副本的 `random` 就是原节点 `random` 的下一个节点；最后把两条链表拆开，并且把原链表还原。

```python
def copy_random_list_o1(head: Node | None) -> Node | None:
    if head is None:
        return None
    node = head
    while node:                                # 1. 每个节点后面插入它的副本：A -> A' -> B -> B'
        node.next = Node(node.val, node.next)
        node = node.next.next
    node = head
    while node:                                # 2. 副本的 random 就是原 random 的下一个节点
        if node.random:
            node.next.random = node.random.next
        node = node.next.next
    new_head = head.next
    node = head
    while node:                                # 3. 拆开两条链表，还原原链表
        copy = node.next
        node.next = copy.next
        copy.next = copy.next.next if copy.next else None
        node = node.next
    return new_head
```

三个样例的结果与哈希表版一致，并且调用之后原链表保持不变。
2. **一遍扫描**：`clone = defaultdict(lambda: Node(0))`，再令 `clone[None] = None`；遍历原链表时对每个节点写 `clone[n].val = n.val`、`clone[n].next = clone[n.next]`、`clone[n].random = clone[n.random]`——查到哪个节点就自动创建哪个，不用事先建好。
3. **一般的图（LC 133）**：同一个思路，字典记录已经克隆的节点；遍历（DFS / BFS）时遇到没克隆过的邻居才创建，并把克隆好的邻居放进新节点的邻居列表。

**Python 提醒**：`defaultdict` 在**读取**缺失的键时也会插入新条目，所以 `clone[node.random]` 本身就会创建节点；这是我们想要的，但如果只是想检查键是否存在，要用 `in`，不要用 `[]`。
