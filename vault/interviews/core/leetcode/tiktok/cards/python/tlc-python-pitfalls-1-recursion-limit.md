---
id: tlc-python-pitfalls-1-recursion-limit
node: python.pitfalls
type: qa
step: 1
---
## Q
**Python 陷阱｜递归深度上限**

对一棵退化成链的二叉树（深度 `10^5`）做递归 DFS，Python 会发生什么？`sys.setrecursionlimit` 能解决吗，更稳妥的做法是什么？

## A
CPython 默认递归深度上限是 `1000`，超过就抛 `RecursionError: maximum recursion depth exceeded`。

```python
import sys
print(sys.getrecursionlimit())        # 1000
def depth(n: int) -> int:
    return 0 if n == 0 else 1 + depth(n - 1)
try:
    depth(5000)
except RecursionError as e:
    print("RecursionError", e)        # RecursionError maximum recursion depth exceeded
sys.setrecursionlimit(10**5)
print(depth(5000))                    # 5000
```

- `setrecursionlimit` 只是调大这个数字，**不会增加栈空间**；设得远超实际栈容量时，进程可能直接崩溃而不是抛异常，且每层递归的内存开销大，`10^5` 层仍然危险。
- 递归深度由数据决定：树高、链表长度、网格 DFS 的连通块大小。LC 200 在 `300 x 300` 的全陆地网格上，DFS 深度最坏接近 `9 * 10^4`，递归版必然爆栈。
- 稳妥做法：**改成显式栈**（`stack = [start]`，手动 `append` / `pop`）或 BFS；树的前、中、后序遍历都有迭代写法（见递归与记忆化一组）。
- 面试里写递归是被接受的，但要主动说：「如果树可能退化成链，我会改迭代，否则 Python 会爆栈」。
- 记忆化递归（`@cache`）同样吃递归深度：`n = 10^4` 的线性 DP 要改自底向上。

**坑**：只在小样例里跑通，提交后在最长的测试用例上 `RecursionError`；上限出现在题目数据范围里 `n >= 1000` 的任何递归。
