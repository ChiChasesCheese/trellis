---
id: pl-functional-recursion-tco-foundation-python-recursion-limit
node: functional.recursion-tco
type: qa
step: 3
---
## Q
Python 的递归限制是什么？为什么默认是 1000，能不能随便调大？

## A
CPython 有一个解释器级的**最大递归深度**，默认 1000（`sys.getrecursionlimit()`）。超过时抛出可以捕获的 `RecursionError`，而不是让整个进程崩溃：

```python
def f(n): return 0 if n == 0 else 1 + f(n - 1)
f(5000)
# RecursionError: maximum recursion depth exceeded
sys.setrecursionlimit(1_000_000)
f(100_000)          # 100000：调大限制就能跑（Python 3.14 实测）
```

这个限制本来是为了保护真正的 C 栈：早期 CPython 每一层 Python 调用都会在 C 栈上递归调用解释器函数，调用太深会让 C 栈溢出、进程直接崩（段错误）。限制一个较保守的数字，把它变成异常。

3.11 起，纯 Python 函数之间的调用不再占用 C 栈（解释器内部用循环处理），所以上面把限制调到 100 万、实际深度 10 万也能跑。但这个限制仍然存在，且仍可能被触发：经过 C 代码的递归（比如 `json.loads` 解析嵌套结构、`pickle`、通过 `__repr__` 递归）依然占用 C 栈，调得过高仍可能让进程崩溃。

所以 `setrecursionlimit` 是一把双刃剑：对纯 Python 的递归，调高相对安全；对要经过 C 的递归，调得太高相当于关掉安全网。更好的做法是把深递归改成显式栈（`list` 当栈）的循环。
