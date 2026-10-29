---
id: tlc-min-stack-2-code
node: a.min-stack
type: qa
step: 2
---
## Q
**LC 155 最小栈**｜写出 Python 实现

实现 `MinStack` 类：`push(val)` 压入整数（`-2^31..2^31-1`）、`pop()` 删除栈顶、`top()` 返回栈顶、`getMin()` 返回栈中最小元素；后三个操作总在非空栈上调用；每个操作都要 `O(1)`。

## A
**思路。** 栈里存 `(值, 压入它之后的最小值)` 二元组。`push` 时新的最小值是 `min(val, 旧栈顶的最小值)`；`pop` 直接弹出，最小值随二元组一起消失；`top` 取第一个分量，`getMin` 取第二个分量。

```python
class MinStack:
    def __init__(self) -> None:
        self.stack: list[tuple[int, int]] = []    # 每项 (值, 压入它时栈内的最小值)

    def push(self, val: int) -> None:
        low = min(val, self.stack[-1][1]) if self.stack else val
        self.stack.append((val, low))             # 最小值跟着元素一起入栈，随它一起出栈

    def pop(self) -> None:
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1][0]

    def getMin(self) -> int:
        return self.stack[-1][1]
```

**运行。** `push(-2)`、`push(0)`、`push(-3)` 后 `getMin()` → `-3`；`pop()` 后 `top()` → `0`、`getMin()` → `-2`；`push(-2147483648)`、`push(2147483647)` 后 `getMin()` → `-2147483648`、`top()` → `2147483647`。

**复杂度。** 四个操作均为 `O(1)`（`list.append` 与 `pop()` 是摊还 `O(1)`）；空间 `O(n)`。

**写法要点。** 用 `list` 当栈，`append` / `pop()` 在尾部操作；二元组 `(值, 最小值)` 比维护两个并行列表少一个同步错误的机会；`min(val, self.stack[-1][1]) if self.stack else val` 把空栈特判压成一行；方法名保持 LeetCode 要求的驼峰 `getMin`，不要改成下划线风格；类型注解写成 `list[tuple[int, int]]`，`__init__` 返回 `None`。
