---
id: yield-from-delegates-send-throw-close
node: iteration.yield-from
type: qa
source: peps
---
## Q
`yield from sub_gen` 和手写的 `for v in sub_gen: yield v` 在功能上有什么本质区别？

## A
后者只把 sub_gen 产出的值转发给调用者；如果调用者对外层生成器调用 `send()`、`throw()` 或 `close()`，这些都不会传给 sub_gen。`yield from` 会把三者透明地委托（delegate）给 sub_gen：外层收到的 `send(value)` 转给 sub_gen 的 `send()`（value 为 None 时改用 `next()`），外层被 `throw()` 的异常转给 sub_gen 的 `throw()`，外层被 `close()` 时也会先调用 sub_gen 的 `close()`。这样被拆出去的一段代码行为和没拆之前完全一样。
