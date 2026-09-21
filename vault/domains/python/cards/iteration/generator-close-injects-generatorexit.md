---
id: generator-close-injects-generatorexit
node: iteration.yield-from
type: qa
source: peps
---
## Q
调用生成器的 `.close()` 方法在其内部实际发生了什么？如果生成器在收到 close() 之后又执行了一次 `yield` 会怎样？

## A
`close()` 会在生成器当前挂起的 `yield` 处注入一个 `GeneratorExit` 异常。如果生成器因此正常退出（不捕获、或捕获后不再产出值就结束），或重新抛出 `GeneratorExit`，`close()` 正常返回；如果生成器捕获了 `GeneratorExit` 后又 `yield` 出一个新值，说明它没有真正终止，`close()` 会抛出 `RuntimeError`——「被关闭的生成器还在继续产出值」是不允许的。
