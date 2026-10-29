---
id: tlc-design-a-stack-with-increment-operation-3-why
node: b.design-a-stack-with-increment-operation
type: qa
step: 3
---
## Q
**LC 1381 设计一个支持增量操作的栈**｜正确性

懒标记解法要保持什么不变量？`pop` 时为什么既要把 `add[i]` 传给 `add[i-1]`，又要把 `add[i]` 清零？给一个漏掉清零会出错的操作序列。

## A
**不变量。** 对栈里任意下标 `j`，它的真实值 = `stack[j] + add[j] + add[j+1] + ... + add[top]`，即从它往上到栈顶所有格子的欠账之和。

**为什么成立。** `increment(k, val)` 让下标 `0..k-1` 都加 `val`，记在 `add[k-1]`，正好被下标 `<= k-1` 的元素算进去，更高的不算。弹出栈顶 `i` 时，它的真实值是 `stack[i] + add[i]`。`add[i]` 对下面的元素同样有效，所以要加到 `add[i-1]`，否则它们丢掉这笔增量。`add[i]` 这一格之后会被新压入的元素重用，新元素从未被那次 `increment` 影响，所以要清零。

**反例（漏清零）。** 容量 3：`push(1)`、`increment(1, 10)`、`pop()` → `11`。再 `push(5)`、`pop()`：漏清零时 `add[0]` 还是 `10`，返回 `15`；正确是 `5`。
