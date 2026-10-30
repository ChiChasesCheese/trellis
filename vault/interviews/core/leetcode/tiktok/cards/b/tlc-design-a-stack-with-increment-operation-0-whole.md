---
id: tlc-design-a-stack-with-increment-operation-0-whole
node: b.design-a-stack-with-increment-operation
type: qa
---
## Q
**LC 1381 设计一个支持增量操作的栈**｜Medium · CodeTop 国内累计 2 次 · 最近 2026-04-10（国内 CodeTop）

实现 `CustomStack`：`CustomStack(maxSize)` 设定栈的容量；`push(x)`：栈未满时把 `x` 压到栈顶，满了就忽略；`pop()`：弹出并返回栈顶，栈空返回 `-1`；`increment(k, val)`：**栈底**的 `k` 个元素都加 `val`，元素不足 `k` 个时全部加 `val`。`1 <= maxSize, x, k <= 1000`，`0 <= val <= 100`，三种操作各最多调用 `1000` 次。例：容量 3，`push(1)`、`push(2)`、`pop()` → `2`，`push(2)`、`push(3)`、`push(4)`（已满，忽略），`increment(5, 100)`、`increment(2, 100)`，之后四次 `pop()` → `103`、`202`、`201`、`-1`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 增量不立即加到元素上，而是记在被影响区间的**最上面一格** `add[k-1]`；弹出栈顶时把这格的欠账加到返回值上，并把它**传给下面一格**。三种操作都是 `O(1)`。

**识别。** `increment` 改的是「栈底的一段前缀」，而读取只发生在栈顶，这是**懒标记**（lazy propagation，把更新先记下来，等到读取时再结算）的信号；它也是差分数组（difference array）的思路：只在区间边界记一笔，读取时累加。约束只有 `1000` 次操作，`O(k)` 的直接循环也能过，面试官要的是 `O(1)`。

**推导。** 直接写法：`increment` 循环 `min(k, len)` 个元素逐个加，`O(k)`。浪费在于栈底的元素要很久之后才会被弹出读取，提前加没有意义。由于只有栈顶会被读，可以把「`0..k-1` 都加 `val`」记成 `add[k-1] += val`：它表示下标 `0..k-1` 都欠着这笔增量。当下标 `i` 成为栈顶并被弹出时，它欠的全部增量就是 `add[i]`；它下面的元素同样欠着这笔，所以把 `add[i]` 加到 `add[i-1]`，再清零 `add[i]`。

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

**复杂度。** 三种操作都是 `O(1)`；空间 `O(maxSize)`。

**易错点。**
- 弹出时不把 `add[i]` 清零：这一格下次被新元素占用时会带着旧欠账。容量 3，`push(1)`、`increment(1, 10)`、`pop()` 得 `11`；再 `push(5)`、`pop()` 会错成 `15`（正确 `5`）。
- 弹出时忘了把欠账传给 `add[i-1]`：下面的元素会丢掉本该有的增量。
- 栈空时 `increment` 下标是 `min(k, 0) - 1 = -1`，会写到列表末尾；要先判空。

**追问。**
- 加一个 `top()`：返回 `stack[-1] + add[len(stack) - 1]`，不弹出。
- 改成给**栈顶**的 `k` 个元素加 `val`：栈顶格 `+val`，第 `len-k-1` 格 `-val`（若存在），弹出时照样往下传，抵消正好发生在区间下边界。
- 任意位置随机读取：改用树状数组（Fenwick tree）维护差分，读写都是 `O(log n)`。

**同模式。** LC 370 区间加法、LC 1109 航班预订统计、LC 155 最小栈、LC 716 最大栈。
