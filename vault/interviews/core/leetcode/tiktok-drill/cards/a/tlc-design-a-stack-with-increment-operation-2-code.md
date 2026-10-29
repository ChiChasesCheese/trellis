---
id: tlc-design-a-stack-with-increment-operation-2-code
node: a.design-a-stack-with-increment-operation
type: qa
step: 2
---
## Q
**LC 1381 设计一个支持增量操作的栈**｜写出 Python 实现

实现 `CustomStack(maxSize)`、`push(x)`（满则忽略）、`pop()`（空返回 `-1`）、`increment(k, val)`（栈底 `k` 个加 `val`，不足则全加）。`1 <= maxSize, x, k <= 1000`，`0 <= val <= 100`，每种操作至多 `1000` 次。要求三种操作都是 `O(1)`。

## A
**思路。** 用 `add[i]` 记「下标 `0..i` 都欠着的增量」。`increment` 只改 `add[min(k, len) - 1]`；`pop` 返回 `stack[i] + add[i]`，并把 `add[i]` 传给 `add[i-1]` 后清零。

```python
class CustomStack:
    def __init__(self, maxSize: int) -> None:
        self.cap = maxSize
        self.stack: list[int] = []
        self.add: list[int] = [0] * maxSize   # add[i]：下标 0..i 的元素都还欠着这笔增量

    def push(self, x: int) -> None:
        if len(self.stack) < self.cap:
            self.stack.append(x)

    def pop(self) -> int:
        if not self.stack:
            return -1
        i = len(self.stack) - 1
        inc, self.add[i] = self.add[i], 0     # 取走栈顶的欠账，并把这一格清零
        if i:
            self.add[i - 1] += inc            # 欠账往下传给新的栈顶
        return self.stack.pop() + inc

    def increment(self, k: int, val: int) -> None:
        if self.stack:
            self.add[min(k, len(self.stack)) - 1] += val   # 只记在第 k 个（或栈顶）上
```

运行：上面的操作序列，五次 `pop()` 依次返回 `2`、`103`、`202`、`201`、`-1`；容量 3，`push(1)`、`increment(1, 10)`、`pop()` → `11`，再 `push(5)`、`pop()` → `5`。

**复杂度。** 时间：三种操作都是 `O(1)`；空间 `O(maxSize)`：`add` 数组。

**写法要点。** `inc, self.add[i] = self.add[i], 0` 用元组赋值同时「取出旧值」和「清零」，不需要临时变量；`[0] * maxSize` 一次开好，元素是不可变的 `int`，可以安全地用乘法复制；`min(k, len(self.stack)) - 1` 一步处理「元素不足 `k` 个」的情况；构造参数沿用 `maxSize` 这个接口名。
