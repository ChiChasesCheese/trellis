---
id: tlc-populating-next-right-pointers-in-each-node-4-followup
node: b.populating-next-right-pointers-in-each-node
type: qa
step: 4
---
## Q
**LC 116 填充每个节点的下一个右侧节点指针**｜追问

面试官接着问：（1）树不是完美二叉树，孩子可能缺失（LC 117），怎么改；（2）用递归怎么写，空间是多少；（3）为什么不直接用 BFS？

## A
1. **一般二叉树**：不能再假设孩子齐全，也不能直接写 `right.next = next.left`。做法：逐层，用一个哑节点串起下一层：遍历本层时，把遇到的每个孩子接到下一层链表的末尾，本层结束后哑节点的 `next` 就是下一层的最左节点。仍然 `O(n)` 时间、`O(1)` 额外空间。

```python
def connect_general(root: 'Node | None') -> 'Node | None':
    head = root                                   # 当前层的最左节点
    while head:
        dummy = tail = Node(0)                    # 下一层链表的哑头
        node = head
        while node:                               # 沿着当前层的 next 走
            for child in (node.left, node.right):
                if child:
                    tail.next = child
                    tail = child
            node = node.next
        head = dummy.next                         # 下一层的最左节点；没有孩子时为 None
    return root
```

2. **递归**：先连好当前节点的两个孩子，再递归处理它们；连线顺序要求先连后递归，因为跨父亲的 `root.next` 在处理父层时已设好。空间 `O(h)` 栈（题目允许）。

```python
def connect_rec(root: 'Node | None') -> 'Node | None':
    if root and root.left:
        root.left.next = root.right
        if root.next:
            root.right.next = root.next.left
        connect_rec(root.left)
        connect_rec(root.right)
    return root
```

3. **BFS**：写法最直观，但队列最宽时存 `n/2` 个节点，`O(n)` 空间；进阶明确要求常量空间，所以先说明 BFS 作为基线，再用 `next` 链替代队列。

两个函数在完美二叉树和随机的一般二叉树上，每层相邻节点都互连、最右节点的 `next` 为 `None`。

**Python 提醒**：`dummy = tail = Node(0)` 链式赋值让两个名字指向同一个对象；`tail = child` 之后 `tail` 重新绑定，`dummy` 不受影响，最后 `dummy.next` 仍是链表头。递归深度等于树高，完美二叉树最多 `12` 层，远低于默认递归上限。
