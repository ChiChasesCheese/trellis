---
id: tlc-min-stack-4-followup
node: a.min-stack
type: qa
step: 4
---
## Q
**LC 155 最小栈**｜追问

面试官接着问：（1）能不能把额外空间降到 `O(1)`，不给每个元素都多存一个整数？（2）改成最大栈，还要支持 `popMax`？（3）C++ / Java 里要注意什么？

## A
1. **差值法。** 栈里存 `val - 压入前的最小值`，另用一个变量 `low` 记当前最小值。差值为负，说明这个元素成了新的最小值：

```python
class MinStackDiff:
    def __init__(self) -> None:
        self.diffs: list[int] = []               # 存 val - 压入前的最小值
        self.low = 0                             # 当前最小值（栈非空时有效）

    def push(self, val: int) -> None:
        if not self.diffs:
            self.diffs.append(0)
            self.low = val
            return
        self.diffs.append(val - self.low)
        if val < self.low:                       # 差值为负：val 成为新的最小值
            self.low = val

    def pop(self) -> None:
        diff = self.diffs.pop()
        if diff < 0:                             # 弹出的正是当前最小值：还原旧最小值
            self.low -= diff

    def top(self) -> int:
        diff = self.diffs[-1]
        return self.low if diff < 0 else self.low + diff

    def getMin(self) -> int:
        return self.low
```

2. **最大栈（LC 716）。** `popMax` 要删除栈中间的元素：用最大堆加懒删除（给每个元素一个递增编号，弹出时跳过已删除的编号），或者双向链表加按值排序的有序结构。
3. **溢出。** 差值法里 `val - low` 可能超出 32 位范围（`-2^31` 与 `2^31 - 1` 相减），要用 64 位整数；Python 没有这个问题。

**Python 提醒**：`self.stack[-1]` 在空栈上抛 `IndexError`；题目保证非空，但自己写测试时 `pop` / `top` 前要确认非空。
