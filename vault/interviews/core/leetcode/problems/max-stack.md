---
slug: max-stack
---
## Q
**LC 716 Max Stack**｜Hard

设计栈，支持 `push`、`pop`、`top`、`peekMax`、`popMax`；`popMax` 移除最大元素，有多个时只移除最靠近栈顶的那个。

## A
**一句话。** 每个元素带唯一编号，栈和最大堆（存 `(值, 编号)`）各自惰性删除，被另一边删掉的等浮到顶再丢。

```python
class MaxStack:
    def __init__(self):
        self.stack = []          # (值, 编号)，栈顶在末尾
        self.heap = []           # (-值, -编号)：同值时越新越先出
        self.removed = set()     # 已被任一边删除的编号
        self.nid = 0

    def push(self, x):
        self.stack.append((x, self.nid))
        heapq.heappush(self.heap, (-x, -self.nid))
        self.nid += 1

    def _trim_stack(self):       # 栈顶若已被 popMax 删掉，丢弃
        while self.stack[-1][1] in self.removed:
            self.stack.pop()

    def _trim_heap(self):        # 堆顶若已被 pop 删掉，丢弃
        while -self.heap[0][1] in self.removed:
            heapq.heappop(self.heap)

    def pop(self):
        self._trim_stack()
        x, i = self.stack.pop()
        self.removed.add(i)
        return x

    def top(self):
        self._trim_stack()
        return self.stack[-1][0]

    def peekMax(self):
        self._trim_heap()
        return -self.heap[0][0]

    def popMax(self):
        self._trim_heap()
        nx, ni = heapq.heappop(self.heap)
        self.removed.add(-ni)
        return -nx
```

**复杂度。** `push`、`popMax`、`peekMax` 摊还 `O(log n)`，`pop`、`top` 摊还 `O(1)`，空间 `O(n)`。

**易错点。**
- 堆只存值不存编号：`popMax` 时没法告诉栈删哪一个。
- 堆键写成 `(-值, 编号)`：同值时先出的是更深的那个，`push 5,1,5` 后 `popMax` 栈变 `[1,5]`，应为 `[5,1]`。
- `top`、`pop` 忘了先清理栈顶：会返回已被 `popMax` 删掉的值。

**追问。**
- 还要 `popMin`、`peekMin`？：再加一个最小堆，三个结构共用同一个 `removed`。
- 想严格 `O(log n)` 不要摊还？：改用有序结构加双向链表，`TreeMap` 存「值→节点栈」。

**同模式。** LC 155 最小栈、LC 895 最大频率栈、LC 146 LRU 缓存、LC 239 滑动窗口最大值
