---
id: positional-only-vs-keyword-only-params
node: functions.arguments
type: qa
source: python-docs
---
## Q
函数签名 `def f(a, b, /, c, *, d):` 里，`/` 和 `*` 分别把参数划成了哪几类？为什么要限制某些参数只能按位置传、只能按关键字传？

## A
`/` 前面的 `a`、`b` 是仅限位置参数（positional-only），调用时不能写成 `a=1`；`/` 和 `*` 之间的 `c` 既能按位置也能按关键字传；`*` 后面的 `d` 是仅限关键字参数（keyword-only），调用时必须写成 `d=值`。这样划分让库作者可以自由重命名仅限位置参数的名字（因为它不算公开 API 的一部分），同时强制调用方对容易搞混的参数（如布尔开关）显式写出参数名，提升可读性。
