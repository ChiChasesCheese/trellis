---
id: bank-linear-max-stack
node: bank.structures.linear
type: qa
step: 1
---
## Q
设计支持 `push`、`pop`、`top`、`max` 的栈，`max` 要 O(1)。为什么让每个元素带上「入栈时的最大值」，比另开一个只在出现新最大值时才入栈的辅助栈更不容易出错？

## A
**每个元素带着自己入栈时的最大值**

- **做法**：栈里存 `(值, 此刻栈内最大值)`。`push` 时新的最大值是 `max(x, 栈顶带的最大值)`；`pop` 把整对一起弹走，旧的最大值自动回来，没有第二个结构要同步；
- **辅助栈的坑**：辅助栈只在 `x > 当前最大` 时入栈，弹出时 `x == 辅助栈顶` 才弹。两个 5 先后入栈，辅助栈里只有一个 5；弹出一个 5 后辅助栈空了，`max()` 抛 `IndexError`，而栈里明明还有一个 5。修法是相等也入栈（`>=`）；
- **代价**：每个元素多存一个引用，空间翻倍；换来的是没有重复值之类的边界情况要记；
- **同一个思路**：每个状态带着自己的「前缀聚合」（最小值、和、最大频次），弹出时自然回退，不用重算；
- **`pop_max`（弹出最大值）不是这个结构能做的**：被弹出的最大值可能在栈中间，要换成按值有序的结构（堆加惰性删除，或有序容器）。

```python
class MaxStack:
    def __init__(self): self._s = []                 # 每项 (值, 此刻栈内最大值)
    def push(self, x):
        self._s.append((x, max(x, self._s[-1][1]) if self._s else x))
    def pop(self): return self._s.pop()[0]
    def top(self): return self._s[-1][0]
    def max(self): return self._s[-1][1]             # O(1)，弹出后自动回到旧的最大值

s = MaxStack()
for x in (3, 5, 5, 2): s.push(x)
print(s.max(), s.pop(), s.max(), s.pop(), s.max(), s.pop(), s.max())   # 5 2 5 5 5 5 3
```

<details class="pt"><summary>延伸</summary>

空栈上调用 `pop`、`top`、`max` 时，这里会抛 `IndexError`。面试里要先问清楚：抛异常，还是返回哨兵值。两种合同都合理，写进接口再动手。

</details>

**知识点：**栈、队列、Trie 及变体（Linear & Trie）
