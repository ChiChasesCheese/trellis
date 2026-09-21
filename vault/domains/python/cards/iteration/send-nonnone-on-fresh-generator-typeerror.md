---
id: send-nonnone-on-fresh-generator-typeerror
node: iteration.yield-from
type: qa
source: peps
---
## Q
对一个刚创建、还没执行过 `next()` 的生成器直接调用 `.send(1)`（非 None 值），会发生什么，为什么？

## A
会抛出 `TypeError`。生成器刚创建时执行还没走到任何 `yield` 表达式，没有地方可以接收 `send()` 送进来的值。必须先用 `next()`（等价于 `send(None)`）把它推进到第一个 `yield` 处，之后再调用 `send(非 None 值)` 才有意义——那个值会成为「上一个 yield 表达式」的返回值。
