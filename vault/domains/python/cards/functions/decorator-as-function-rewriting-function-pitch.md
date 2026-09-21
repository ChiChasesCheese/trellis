---
id: decorator-as-function-rewriting-function-pitch
node: functions.decorators
type: qa
source: python-docs
---
## Q
60 秒内讲清楚：为什么说装饰器（decorator）本质上「只是用函数改写函数的语法糖」？

## A
`@d def f(): ...` 只是 `f = d(f)` 的另一种写法：装饰器 `d` 接收原函数、返回一个新的可调用对象（通常是个包装函数），再把这个新对象重新绑定回原来的名字。这一步在 `def` 语句执行时（模块导入阶段）就已经跑完，之后每次调用的其实是 `d` 返回的那个对象，不是最初写的函数体本身；`functools.wraps` 的作用就是让这个新对象在外表上尽量还原成原函数的样子。
