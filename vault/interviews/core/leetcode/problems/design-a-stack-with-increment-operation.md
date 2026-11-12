---
slug: design-a-stack-with-increment-operation
---
## Q
**LC 1381 设计一个支持增量操作的栈**｜Medium

实现容量为 `maxSize` 的栈：`push`（满了忽略）、`pop`（空返回 `-1`）、`increment(k, val)`（栈底的 `k` 个元素都加 `val`）。

## A
**一句话。** 懒标记：增量先记在第 `k` 格上，`pop` 时才加到返回值并传给下面一格，三种操作都 `O(1)`。

```python
class CustomStack:
    def __init__(self, maxSize):
        self.cap = maxSize
        self.stack = []
        self.add = [0] * maxSize  # add[i]：0..i 都还欠这笔增量

    def push(self, x):
        if len(self.stack) < self.cap:
            self.stack.append(x)

    def pop(self):
        if not self.stack:
            return -1
        i = len(self.stack) - 1
        inc, self.add[i] = self.add[i], 0   # 取走并清零
        if i:
            self.add[i - 1] += inc          # 欠账往下传
        return self.stack.pop() + inc

    def increment(self, k, val):
        if self.stack:
            self.add[min(k, len(self.stack)) - 1] += val
```

**复杂度。** 时间 每个操作 `O(1)`，空间 `O(maxSize)`。

**易错点。**
- `pop` 不清零 `add[i]`：下个占用这格的元素带着旧欠账，`push(1)`、`increment(1,10)`、`pop()`、`push(5)`、`pop()` 得 `15`，应为 `5`。
- `pop` 忘了把欠账传给 `add[i-1]`：下面的元素丢掉本该有的增量。
- 栈空时不判空：`min(k,0)-1 = -1` 会写到列表末尾。

**追问。**
- 改成给栈顶的 `k` 个加 `val`？：栈顶格 `+val`，第 `len-k-1` 格 `-val`，`pop` 时照样往下传。
- 要随机读任意位置呢？：用树状数组维护差分，读写 `O(log n)`。

**同模式。** LC 155 最小栈、LC 716 最大栈、LC 1109 航班预订统计、LC 370 区间加法
