---
id: call-protocol-no-base-class-needed
node: model.dunder-protocols
type: qa
source: python-docs
---
## Q
一个普通类的实例想要支持 `obj(1, 2)` 这样的函数调用语法，需要做什么？是否必须继承某个特殊基类？

## A
只需要在类里定义 `__call__(self, ...)` 方法，Python 就会把 `obj(1, 2)` 翻译成 `obj.__call__(1, 2)`；不需要继承任何特殊基类——「可调用」是通过实现这一个特殊方法获得的能力（协议），而不是通过类型继承关系获得的。
