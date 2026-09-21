---
id: class-decorator-loses-self-binding
node: functions.decorator-patterns
type: qa
tags: [grown]
---
## Q
用一个实现了 `__call__` 但没有实现 `__get__` 的类去装饰一个实例方法，调用 `obj.method(x)` 时，`self` 还会像普通方法一样被自动传进去吗？

## A
不会。普通函数能被自动绑定为方法，是因为函数对象实现了描述符协议（`__get__`），实例属性查找时会把它转成绑定方法、自动把 `obj` 作为第一个参数传入。类装饰器产生的是一个「类实例」，如果这个类没有实现 `__get__`，它就只是一个普通的类属性，`obj.method` 拿到的是这个装饰器实例本身，调用它执行的其实是 `装饰器实例.__call__(x)`，不会自动带上 `self`。要正确装饰方法，要么让装饰器类也实现 `__get__`，要么改用基于闭包的函数式装饰器。
