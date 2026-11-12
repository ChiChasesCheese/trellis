---
slug: copy-list-with-random-pointer
---
## Q
**LC 138 随机链表的复制**｜Medium

链表每个节点除 `next` 外还有指向任意节点或空的 `random`，深拷贝整条链表，新指针都指向新节点。

## A
**一句话。** 第一遍给每个旧节点造新节点存进字典，第二遍用字典把 `next` 和 `random` 翻译过去。

```python
def copy_random_list(head):
    clone = {None: None}         # None 映射到 None，免判空
    cur = head
    while cur:                   # 第一遍：只造节点
        clone[cur] = Node(cur.val)
        cur = cur.next
    cur = head
    while cur:                   # 第二遍：连 next 和 random
        clone[cur].next = clone[cur.next]
        clone[cur].random = clone[cur.random]
        cur = cur.next
    return clone[head]
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 用 `val` 当键：`[3,3,3]` 键冲突，`random` 指错；键必须是节点对象。
- 一遍同时造节点和连 `random`：`random` 指向还没造出的后面节点，字典抛 `KeyError`。
- 写成 `clone[cur].random = cur.random`：新节点指回旧链，不是深拷贝。

**追问。**
- 不用字典，`O(1)` 额外空间？：把副本插在每个原节点后面，副本的 `random` 是 `cur.random.next`，最后拆成两条链。
- 不许改原链表？：只能用字典；穿插法拆链前原链已被改过。

**同模式。** LC 133 克隆图、LC 1485 克隆含随机指针的二叉树、LC 138 的穿插解法、LC 148 排序链表
