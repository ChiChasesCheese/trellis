---
id: tlc-copy-list-with-random-pointer-2-code
node: a.copy-list-with-random-pointer
type: qa
step: 2
---
## Q
**LC 138 随机链表的复制**｜写出 Python 实现

链表节点有 `val`、`next`、`random` 三个字段，`random` 指向链表中任意节点或 `None`；`0 <= n <= 1000`，`-10^4 <= Node.val <= 10^4`。返回深拷贝的头节点：全新节点，所有指针都指向新链表。

## A
**思路。** 两遍扫描。第一遍为每个原节点创建新节点并存进字典；第二遍用原节点的 `next` 和 `random` 去字典里查到对应的新节点，连到新节点上。字典里预置 `None -> None`，空指针不需要特判。

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

运行：三个样例 `[[7,null],[13,0],[11,4],[10,2],[1,0]]`、`[[1,1],[2,1]]`、`[[3,null],[3,0],[3,null]]` 拷贝后的 `[val, random 下标]` 与输入一致，新旧链表没有共享的节点，原链表不变；空链表 → `None`。

**复杂度。** 时间 `O(n)`；空间 `O(n)`。

**写法要点。** 字典的键是节点对象，按身份哈希，值相同的节点也互不冲突；`{None: None}` 让 `clone[node.random]` 对空指针也成立；`clone[head]` 当 `head` 为 `None` 时直接得到 `None`，空链表无需特判；类型标注 `dict[Node | None, Node | None]` 说明键和值都可能是空。LeetCode 的 `Node` 构造函数是 `Node(x, next=None, random=None)`。
