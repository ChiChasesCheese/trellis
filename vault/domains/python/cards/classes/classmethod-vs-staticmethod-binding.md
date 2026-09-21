---
id: classmethod-vs-staticmethod-binding
node: classes.pythonic-object
type: qa
source: python-docs
---
## Q
从「调用时解释器会不会自动传入什么」的角度，`@classmethod` 和 `@staticmethod` 装饰出来的方法本质区别是什么？

## A
`classmethod` 包装出的方法对象在从类或实例上取出时，其 `__self__` 绑定的是类本身，因此不管用 `实例.f(1)` 还是 `类.f(1)` 调用，底层都等价于 `f(类, 1)`——第一个参数永远是类。`staticmethod` 只是把一个普通函数包一层，取出时直接返回被包裹的函数本身，不做任何绑定转换，调用时不会自动插入 `self` 或 `cls`，本质是「挂在类命名空间下的普通函数」。
