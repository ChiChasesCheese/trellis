---
id: dunder-protocol-vs-inherit-builtin
node: model.dunder-protocols
type: qa
source: python-docs
---
## Q
为什么说 Python 里「支持 `len()`、`for`、`in`、函数调用」这些语法能力是靠实现特殊方法（dunder methods）组成的「协议」获得的，而不是靠继承内建类型获得的？

## A
解释器遇到 `len(x)`、`for i in x`、`x in y`、`f(x)` 这些语法时，实际是查找并调用对象类型上对应的特殊方法（`__len__`、`__iter__`、`__contains__`、`__call__` 等），并不检查这个类型是不是某个内建类型的子类。任何普通类只要实现了对应方法就能接入这些语法，不需要继承 `list`、`dict` 这类内建容器——这样既避免了继承内建类型带来的额外开销和意料之外的方法，又能让自定义类型精确选择要支持哪些协议。
