---
id: zero-arg-super-needs-classcell
node: classes.metaprogramming
type: qa
source: python-docs
---
## Q
方法体里写 `super()`（不带参数）为什么能自动知道『当前是哪个类』？这跟元类创建类对象这一步有什么关系？

## A
如果类体里的任何方法引用了 `super` 或 `__class__`，编译器会自动生成一个隐式闭包引用，在类创建完成后指向这个新造出来的类对象本身——这个引用在 CPython 里以 `__classcell__` 的名字暂存在类命名空间里，随后被传给 `type.__new__()`，由它负责把这个占位的 cell 正确关联回真正的类对象。也就是说零参数 `super()` 之所以『知道自己在哪个类里』，靠的不是运行时反查，而是类对象创建这一步埋下的编译期闭包；如果自定义元类没把 `__classcell__` 正确转发给 `type.__new__`，会导致运行时报 `RuntimeError`。
