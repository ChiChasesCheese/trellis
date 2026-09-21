---
id: class-creation-order-setname-then-initsubclass
node: classes.metaprogramming
type: cloze
source: python-docs
---
用默认元类 `type` 创建一个类时，类体执行完、类对象造出来之后，还会按顺序做两件事：先对类命名空间里所有定义了 `__set_name__()` 的属性依次调用它（传入新类和属性名），{{c1::然后才在新类的直接父类（按 MRO 顺序）上调用 `__init_subclass__()` 这个钩子}}——顺序不能反，因为 `__init_subclass__` 里的逻辑可能需要用到已经被 `__set_name__` 处理过的属性状态。
