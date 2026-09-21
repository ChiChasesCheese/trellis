---
id: init-subclass-vs-class-decorator-scope
node: classes.metaprogramming
type: qa
source: python-docs
---
## Q
`__init_subclass__()` 和类装饰器（class decorator）都能在类创建时介入做点什么，两者的作用范围有什么本质区别？

## A
类装饰器（如 `@dataclass`）只作用于它直接装饰的那一个类，不会自动传播给这个类以后的子类。`__init_subclass__()` 定义在父类上，只要有人继承这个父类（不管继承多少层、多久以后），子类被创建时都会自动调用它——它管的是『这个类以及它未来所有子类的创建过程』，而不是某一次装饰。因此想要『每个继承我的子类都要自动做某件事』（比如自动注册到一个插件表），`__init_subclass__` 比类装饰器更合适，因为装饰器不会追着子类走。
