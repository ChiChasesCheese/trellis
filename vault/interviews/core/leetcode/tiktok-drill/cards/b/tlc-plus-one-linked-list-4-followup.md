---
id: tlc-plus-one-linked-list-4-followup
node: b.plus-one-linked-list
type: qa
step: 4
---
## Q
**LC 369 给单链表加一**｜追问

面试官接着问：（1）数字改成**低位在头**（逆序存储）怎么办？（2）要加的不是 `1`，而是另一个链表表示的数？（3）能用递归写吗？

## A
1. **低位在前。** 进位方向与遍历方向一致，从头走：`9` 变 `0` 继续，遇到非 `9` 加一结束；走到尾仍有进位就补一个 `1`：

```python
def plus_one_reversed(head: ListNode) -> ListNode:
    node = head
    while True:
        if node.val < 9:
            node.val += 1                      # 不再进位，结束
            return head
        node.val = 0                           # 9 + 1 = 10：写 0，进位给下一位
        if node.next is None:
            node.next = ListNode(1)            # 最高位也进位：在尾部补一个 1
            return head
        node = node.next
```

2. **加另一个链表。** 单链表对不齐低位：用两个栈压入各自的数字再弹出逐位相加（LC 445），或者各自反转后做 LC 2 的加法再反转回来；`O(n + m)` 时间。
3. **递归。** 递归到尾部，回溯时带回进位：`carry = helper(node.next)`；最外层还有进位就新建头节点。链表节点数是 `100` 时没有问题，但递归深度等于链表长度，长度到 `10^4` 就会触到 Python 的默认递归上限（`1000`），所以生产里用迭代。

**Python 提醒**：`while True` 里用 `return` 退出比设置标志位更清晰；`node.val < 9` 比 `node.val != 9` 更能表达「还能再加一」的含义，两者对 `0..9` 的值等价。
