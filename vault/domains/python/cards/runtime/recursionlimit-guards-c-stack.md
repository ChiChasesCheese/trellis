---
id: recursionlimit-guards-c-stack
node: runtime.frames-eval
type: qa
source: cpython-internals
---
## Q
`sys.setrecursionlimit()` 限制的到底是什么？如果调用当前已经比新设的上限更深，调低它会发生什么？

## A
它设置 Python 解释器栈允许的最大调用深度，目的是在无限递归耗尽真实 C 调用栈、导致进程崩溃之前，先主动抛出可捕获的 `RecursionError`。可设的最高上限本身是平台相关的，调得太高有实际崩溃风险。若当前调用深度已经超过要设的新上限，`setrecursionlimit()` 会立刻抛出 `RecursionError`，而不是静默生效到下一次调用才发作。
