---
id: tlc-tops-min-stack-0-whole
node: stack.min-stack
type: qa
---
## Q
**LC 155 最小栈**｜Medium · 全公司热度第 44 名 · NeetCode 150、Hot 100、Top Interview 150

设计一个支持 `push`、`pop`、`top` 操作，并能在常数时间内检索到最小元素的栈。实现 `MinStack` 类：`MinStack()` 初始化栈；`push(val)` 将元素入栈；`pop()` 删除栈顶；`top()` 获取栈顶；`getMin()` 获取栈中最小元素。`-2^31 <= val <= 2^31 - 1`，`pop`、`top`、`getMin` 总是在非空栈上调用，各操作最多被调用 `3 * 10^4` 次。例：`push(-2)`、`push(0)`、`push(-3)`、`getMin()` 得 `-3`、`pop()`、`top()` 得 `0`、`getMin()` 得 `-2`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 辅助状态随栈同步（augmented stack）：每个栈位置记录「到此为止的最小值」。

**一句话。** 每次入栈时把「当前值」和「入栈后栈内最小值」成对压入；弹出时最小值自然回到前一个状态。

**识别。** 「栈 + `O(1)` 取最小」：栈只在栈顶变化，所以栈内某个前缀的最小值是不变的，可以随元素一起记下来。

**推导。** 暴力：`getMin` 时扫描整个栈，`O(n)`。只维护一个 `min` 变量的问题是弹出最小值之后，不知道新的最小值是谁。因为栈是后进先出，进入某个位置时栈内的最小值就是这个位置以下所有元素的最小值，之后不会再变，所以把它和元素存在一起即可，四个操作都是 `O(1)`。

```python
class MinStack:
    def __init__(self) -> None:
        self.stack: list[tuple[int, int]] = []  # 每项是 (值, 这一项入栈后栈内的最小值)

    def push(self, val: int) -> None:
        cur_min = min(val, self.stack[-1][1]) if self.stack else val
        self.stack.append((val, cur_min))  # 最小值随元素一起入栈，弹出时自然回到上一个最小值

    def pop(self) -> None:
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1][0]

    def getMin(self) -> int:
        return self.stack[-1][1]
```

运行：题面序列的输出是 `[None, None, None, None, -3, None, 0, -2]`（依次对应 `MinStack`、三次 `push`、`getMin`、`pop`、`top`、`getMin`）。

**复杂度。** 所有操作 `O(1)`，空间 `O(n)`（每个元素多存一个整数）。

**拓展优化。**
- 省空间的写法：用第二个栈只记录最小值，仅当 `val <= 当前最小值` 时才入辅助栈，弹出时若栈顶等于辅助栈顶则一起弹出。等号必须有：重复的最小值要记录多次。
- 只用一个栈：存「值 − 当前最小值」的差，差为负说明这个值本身是新最小值，弹出时再还原；需要注意整数范围，Python 没有溢出问题，但在 Java / C++ 中要用 `long`。

**易错点。**
- 只用一个 `min` 变量：`push(-2)`、`push(0)`、`push(-3)`、`pop()` 之后 `getMin()` 应为 `-2`，而 `min` 变量仍是 `-3`。
- 辅助栈只在 `val < min` 时入栈会漏掉重复最小值：`push(1)`、`push(1)`、`pop()` 之后辅助栈空了，`getMin()` 取不到值（正确是 `1`）。
- 空栈入栈第一个元素时，最小值就是它自己，要单独处理（`if self.stack`）。

**同模式。** LC 716 最大栈、LC 232 用栈实现队列、LC 225 用队列实现栈、LC 146 LRU 缓存。
