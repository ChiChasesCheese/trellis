---
id: python-context-class-vs-generator
node: python.context-iterators
type: qa
step: 5
tags: [grown]
---
## Q
什么时候一个惰性序列必须写成带 `__iter__` 的类，而不能只写一个生成器函数？

## A
当这个对象需要**支持多次独立遍历**时——一个生成器**函数**每调用一次返回一个新的生成器对象（可以重新遍历），但生成器**对象**本身只能被消费一次（遍历完就耗尽，`StopIteration` 之后不会重置）。如果把生成器对象本身当成“容器”反复 `for` 它，第二次会直接得到空结果。要让容器可以被反复 `for ... in container` 遍历，`__iter__` 必须**每次都返回一个新的生成器**，这也是很多容器类仍然要写一个 `__iter__` 方法、而不是直接把自己实现成生成器的原因。
