---
id: contextmanager-decorator-yield-splits-enter-exit
node: iteration.context-managers
type: qa
source: python-docs
---
## Q
用 `@contextlib.contextmanager` 装饰的生成器函数，yield 前后的代码分别对应 `with` 语句的哪个阶段？为什么必须写成 `try: ...; yield ...; finally: ...`？

## A
yield 之前的代码在 `__enter__()` 阶段执行，`yield` 出的值绑定给 `as` 子句的变量；`with` 块跑完（或抛异常）后，控制权回到生成器、从 yield 之后继续执行，这部分对应 `__exit__()` 阶段。用 `try/finally` 包住 `yield` 是因为 `with` 块内未捕获的异常会在 `yield` 表达式处重新抛入生成器；只有 `finally` 里的清理代码才能保证无论是否有异常都会执行。
