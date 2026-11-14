---
slug: design-linked-list
---
## Q
**LC 707 设计链表**｜Medium

实现链表：`get(index)`、`addAtHead`、`addAtTail`、`addAtIndex(index, val)`（`index` 等于长度时尾插、大于长度不插）、`deleteAtIndex(index)`；下标无效时 `get` 返回 `-1`，其余忽略。

## A
**一句话。** 哨兵头节点加长度计数，所有操作都归结为「找到第 `index` 个节点的前驱」再改指针。

**图解。** 插入前先从哨兵走到前驱 `p`，再改两根指针。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 290 165">
<rect x="14" y="44" width="34" height="26" rx="3" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="31" y="61" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">D</text>
<rect x="72" y="44" width="34" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="89" y="61" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">1</text>
<rect x="130" y="44" width="34" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="147" y="61" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">2</text>
<rect x="188" y="44" width="34" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="205" y="61" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">3</text>
<polyline points="48,57 72,57" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="72.0,57.0 66.0,60.0 66.0,54.0" fill="currentColor"/>
<polyline points="106,57 130,57" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="130.0,57.0 124.0,60.0 124.0,54.0" fill="currentColor"/>
<polyline points="164,57 188,57" fill="none" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<polygon points="188.0,57.0 182.0,60.0 182.0,54.0" style="fill:var(--dim,#6b7280)"/>
<polyline points="222,57 240,57" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="240.0,57.0 234.0,60.0 234.0,54.0" fill="currentColor"/>
<text x="246" y="61" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">∅</text>
<text x="31" y="84" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">dummy</text>
<polyline points="147,28 147,44" fill="none" stroke-width="1.4" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="147.0,44.0 144.0,38.0 150.0,38.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="147" y="24" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">p = _prev(2)</text>
<rect x="160" y="104" width="34" height="26" rx="3" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="177" y="121" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">9</text>
<polyline points="147,70 166,104" fill="none" stroke-width="1.4" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="166.0,104.0 160.5,100.2 165.7,97.3" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="188,104 205,70" fill="none" stroke-width="1.4" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="205.0,70.0 205.0,76.7 199.6,74.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="145" y="156" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">addAtIndex(2, 9)：从 dummy 走 2 步到前驱</text>
</svg>

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
