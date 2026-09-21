---
id: robust-assert-internal-invariant-only
node: engineering.robustness
type: qa
source: python-docs
---
## Q
为什么不能用 `assert` 来校验函数的外部输入（比如校验用户传入的参数合法性），而只能用来检查「内部假设」？

## A
Python 解释器以 `-O`（优化）模式启动时，`__debug__` 会变成 `False`，所有 `assert` 语句会被直接跳过、连条件表达式都不会求值——用 `assert` 做的校验在生产环境可能整体消失。因此 `assert` 只适合用来在开发调试阶段检查「代码逻辑上不应该发生」的内部假设（比如某个私有辅助函数的前置条件），真正需要在任何运行模式下都生效的输入校验，必须显式用 `if` 判断后 `raise` 对应的异常。
