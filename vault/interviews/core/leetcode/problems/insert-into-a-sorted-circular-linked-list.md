---
slug: insert-into-a-sorted-circular-linked-list
---
## Q
**LC 708 循环有序列表的插入**｜Medium

给循环非降序链表中的任意一个节点 `head`，插入 `insertVal` 使其仍有序，返回原节点（空表则新建）。

## A
**一句话。** 沿环走一圈找插入点：夹在 `cur<=val<=nxt` 中间，或在「最大→最小」的断点处。

```python
def insert(head, insertVal):
    node = Node(insertVal)
    if head is None:
        node.next = node
        return node
    cur = head
    while True:
        nxt = cur.next
        if cur.val <= insertVal <= nxt.val:
            break
        if cur.val > nxt.val and (insertVal >= cur.val
                                  or insertVal <= nxt.val):
            break           # 断点：比最大还大或比最小还小
        cur = nxt
        if cur is head:     # 绕完一圈（全部相等），随便插
            break
    node.next = cur.next
    cur.next = node
    return head
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 只写普通位置：新值比所有值都大或都小时找不到，一直转圈。
- 单节点或全相等的环没有断点：靠 `cur is head` 终止，漏掉会死循环。
- 空链表忘了让新节点指向自己。

**追问。**
- 值相等时插前插后？：任意位置都合法，题目不要求稳定。
- 返回哪个节点？：非空时返回原来的 `head`，不是新节点。

**同模式。** LC 147 对链表进行插入排序、LC 21 合并两个有序链表、LC 141 环形链表、LC 61 旋转链表
