---
id: with-statement-desugars-to-try-finally
node: iteration.context-managers
type: qa
source: python-docs
---
## Q
`with EXPRESSION as TARGET: SUITE` 在解释器里被展开成怎样一套逻辑？这套展开保证了什么？

## A
大致等价于：先求值拿到 manager，取出它的 `__enter__`/`__exit__`；调用 `__enter__()` 把返回值赋给 TARGET；执行 SUITE；SUITE 正常结束就调用 `exit(None, None, None)`，SUITE 因异常退出就把异常的 type/value/traceback 传给 `exit(...)`。只要 `__enter__()` 没有报错，就保证 `__exit__()` 一定会被调用一次——这样资源清理代码即使在异常路径上也不会被跳过。
