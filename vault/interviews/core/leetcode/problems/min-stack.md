---
slug: min-stack
---
## Q
**LC 155 最小栈**｜Easy

设计栈，支持 `push`、`pop`、`top`，并能在常数时间内取到栈中最小元素 `getMin`。

## A
**一句话。** 每个元素入栈时同时记下「压入它之后栈内的最小值」，二者作为二元组同进同出。

```python
class MinStack:
    def __init__(self):
        self.st = []                 # (值, 此时的栈内最小值)

    def push(self, val):
        low = min(val, self.st[-1][1]) if self.st else val
        self.st.append((val, low))

    def pop(self):
        self.st.pop()

    def top(self):
        return self.st[-1][0]

    def getMin(self):
        return self.st[-1][1]
```

**复杂度。** 时间 每个操作 `O(1)`，空间 `O(n)`。

**易错点。**
- 只用一个变量记最小值：弹出最小值后无法恢复，`push(-2), push(0), push(-3), pop()` 后 `getMin()` 仍是 `-3`。
- 辅助栈只在 `val < 当前最小` 时才压：重复最小值会少压，条件要写 `<=`。

**追问。**
- 只用 `O(1)` 额外空间？：栈里存 `val - min` 的差值，差值为负说明它是新最小值，弹出时据此还原旧最小值。
- 最大栈 `popMax`（LC 716）？：堆加懒删除，或双向链表加有序结构。

**同模式。** LC 716 最大栈、LC 232 用栈实现队列、LC 239 滑动窗口最大值、LC 895 最大频率栈
