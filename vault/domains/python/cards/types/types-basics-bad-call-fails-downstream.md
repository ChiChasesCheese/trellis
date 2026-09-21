---
id: types-basics-bad-call-fails-downstream
node: types.basics
type: qa
source: python-docs
---
## Q
函数签名是 `def total(prices: list[int]) -> int`，调用时传入 `["a", "b"]`，运行时会立刻报错吗？这说明了什么风险？

## A
不会立刻报错。解释器不检查参数类型，`total(["a", "b"])` 会正常进入函数体，直到内部用到对 `str` 非法的操作（比如 `sum()`）才抛出 `TypeError`，报错位置往往远离真正传错类型的调用点，排查成本更高。这正是要在 CI 里跑 mypy/pyright 静态检查的原因——把这类错误挡在运行之前，而不是等运行时报错。
