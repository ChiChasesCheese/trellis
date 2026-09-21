---
id: yield-from-result-is-stopiteration-value
node: iteration.yield-from
type: qa
source: peps
---
## Q
子生成器里写 `return 42` 结束，外层 `result = yield from sub_gen()` 中的 `result` 会拿到什么？这是怎么实现的？

## A
`result` 是 42。生成器里的 `return expr` 在语言层面等价于 `raise StopIteration(expr)`；`yield from` 表达式的值就是子迭代器耗尽时抛出的这个 `StopIteration` 异常的第一个参数（即 `StopIteration.value`）。`yield from` 内部会捕获子迭代器抛出的 `StopIteration`，取出它的 value 作为整个表达式的结果，不会让这个异常继续往外传播。
