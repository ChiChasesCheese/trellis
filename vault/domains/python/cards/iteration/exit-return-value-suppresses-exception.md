---
id: exit-return-value-suppresses-exception
node: iteration.context-managers
type: qa
source: python-docs
---
## Q
`__exit__(exc_type, exc, tb)` 的返回值对 `with` 块里抛出的异常有什么影响？

## A
如果 SUITE 是因异常退出的，`__exit__` 返回真值会让 `with` 语句吞掉这个异常，执行紧跟在 `with` 块后面的语句，就像异常没发生过；返回假值（包括默认的 None）则异常会被重新抛出、继续往外传播。SUITE 正常结束（没有异常）时，`__exit__` 的返回值会被直接忽略，不影响执行流程。
