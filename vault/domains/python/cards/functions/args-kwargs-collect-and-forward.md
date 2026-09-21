---
id: args-kwargs-collect-and-forward
node: functions.arguments
type: qa
source: python-docs
---
## Q
函数签名里的 `*args` 和 `**kwargs` 在调用时分别把多余参数收集成什么类型？如果只想把收到的参数原样转发给另一个函数，该怎么写？

## A
`*args` 把多出的位置参数收集成一个 tuple，`**kwargs` 把多出的关键字参数收集成一个 dict；两者都没收到值时分别默认为空 tuple 和空 dict。原样转发只需在调用另一个函数时再次用 `*`/`**` 解包，例如 `def f(x, *args, **kwargs): g(x, *args, **kwargs)`，位置参数和关键字参数会分别按原顺序、原键值还原传给 `g`。
