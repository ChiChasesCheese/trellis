---
id: super-dispatches-to-mro-next-not-parent
node: classes.inheritance-mro
type: qa
source: python-docs
---
## Q
`super().method()` 调用的到底是「当前类在源码里写的父类」的方法，还是别的什么？

## A
不是源码字面上的父类，而是当前实例的 MRO（method resolution order）列表里、紧跟在发起调用的那个类之后的下一个类。具体来说，`super(A, obj).m` 会在 `obj.__class__.__mro__` 里找到紧跟在 `A` 后面的类 `B`，返回 `B.__dict__['m'].__get__(obj, A)`。在多重继承、尤其是菱形继承（diamond inheritance）下，这个「下一个」可能是一个跟 `A` 毫无直接父子关系的兄弟类——这正是 `super()` 支持协作式多继承（cooperative multiple inheritance）的关键，而不是「调用父类」这么简单。
