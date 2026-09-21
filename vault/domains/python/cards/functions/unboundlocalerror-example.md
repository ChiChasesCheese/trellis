---
id: unboundlocalerror-example
node: functions.scope-closure
type: qa
source: python-docs
---
## Q
已知模块级 `x = 10`；函数 `def foo(): print(x); x += 1` 被调用时会抛出什么异常？根本原因是什么？

## A
抛出 `UnboundLocalError`（是 `NameError` 的子类）。原因是 `foo` 函数体内有 `x += 1` 这一次赋值，编译期就把 `x` 判定为局部变量；执行到 `print(x)` 时这个局部变量还没被赋值，于是报错，而不会去外层作用域找模块级的 `x = 10`。
