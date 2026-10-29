---
id: tlc-design-a-stack-with-increment-operation-4-followup
node: a.design-a-stack-with-increment-operation
type: qa
step: 4
---
## Q
**LC 1381 设计一个支持增量操作的栈**｜追问

面试官接着问：（1）加一个不弹出的 `top()`？（2）`increment` 改成给**栈顶**的 `k` 个元素加 `val`？（3）要支持随机读取第 `i` 个元素？

## A
1. **`top()`**：栈顶 `i` 的真实值是 `stack[i] + add[i]`（它上面没有元素了），直接返回，不改任何状态。
2. **栈顶 `k` 个**：区间是 `[len-k, len-1]`，上边界就是栈顶。在栈顶格加 `val`，在区间下边界的下一格 `len-k-1` 减 `val`；弹出时照常把欠账往下传，传到 `len-k-1` 时正负抵消。

```python
def increment_top(self, k: int, val: int) -> None:
    if self.stack:
        self.add[len(self.stack) - 1] += val
        if (lo := len(self.stack) - k - 1) >= 0:   # 区间之下的那一格抵消
            self.add[lo] -= val
```

3. **随机读取**：真实值是 `add` 的一段后缀和，用树状数组（Fenwick tree）维护 `add`，`increment` 与读取都是 `O(log n)`。

**Python 提醒**：`[0] * n` 复制不可变的 `int` 没问题，但 `[[]] * n` 里 `n` 个元素是**同一个**列表，改一个全变；二维结构要写 `[[] for _ in range(n)]`。
