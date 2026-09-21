---
id: for-loop-delegation-leaks-close-chain
node: iteration.yield-from
type: qa
source: peps
---
## Q
用 `for v in sub_gen: yield v` 代替 `yield from sub_gen` 委托子生成器，当外层生成器被 `.close()` 时有什么隐患？

## A
for 循环包装时，外层收到 `close()` 只会在自己的挂起点注入 `GeneratorExit`，不会主动调用 sub_gen 的 `close()`；如果 sub_gen 用 `try/finally` 持有着需要释放的资源（文件、锁等），这些资源可能不会被及时释放，造成泄漏。`yield from` 会把 `close()` 显式转发给 sub_gen（如果它有 `close()` 方法），保证委托链从最内层的子生成器开始逐层终结。
