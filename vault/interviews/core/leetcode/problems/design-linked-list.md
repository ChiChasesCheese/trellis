---
slug: design-linked-list
---
## Q
**LC 707 设计链表**｜Medium

实现链表：`get(index)`、`addAtHead`、`addAtTail`、`addAtIndex(index, val)`（`index` 等于长度时尾插、大于长度不插）、`deleteAtIndex(index)`；下标无效时 `get` 返回 `-1`，其余忽略。

## A
**一句话。** 哨兵头节点加长度计数，所有操作都归结为「找到第 `index` 个节点的前驱」再改指针。

```python
class Node:
    def __init__(self, val=0, nxt=None):
        self.val, self.next = val, nxt

class MyLinkedList:
    def __init__(self):
        self.dummy = Node()   # 哨兵：头插、删头不用特判
        self.size = 0

    def _prev(self, index):   # 第 index 个节点的前驱
        p = self.dummy
        for _ in range(index):
            p = p.next
        return p

    def get(self, index):
        if not 0 <= index < self.size:
            return -1
        return self._prev(index).next.val

    def addAtHead(self, val):
        self.addAtIndex(0, val)

    def addAtTail(self, val):
        self.addAtIndex(self.size, val)

    def addAtIndex(self, index, val):
        if index > self.size:  # 等于 size 是尾插，合法
            return
        p = self._prev(max(index, 0))
        p.next = Node(val, p.next)
        self.size += 1

    def deleteAtIndex(self, index):
        if not 0 <= index < self.size:
            return
        p = self._prev(index)
        p.next = p.next.next
        self.size -= 1
```

**复杂度。** `get`、`addAtIndex`、`deleteAtIndex` 为 `O(index)`，头插 `O(1)`，尾插 `O(n)`；空间 `O(n)`。

**易错点。**
- `addAtIndex` 边界：`index == size` 要插到尾部，只有 `index > size` 才忽略。
- 忘了维护 `size`：插入、删除都要改，否则下标检查全错。
- 没有哨兵：删头、往空表插入都要单独处理，容易漏。

**追问。**
- 尾插要 `O(1)`？：再维护尾指针；删除最后一个节点时要把尾指针移回前驱，所以常改成带头尾哨兵的双向链表。
- 双向链表有什么好处？：知道节点本身就能 `O(1)` 删除，按下标查找可以从离得近的一端走，最多走 `n/2` 步。
- 为什么用哨兵？：保证每个真实节点都有前驱，插入和删除只剩一种写法。

**同模式。** LC 206 反转链表、LC 146 LRU 缓存、LC 641 设计循环双端队列
