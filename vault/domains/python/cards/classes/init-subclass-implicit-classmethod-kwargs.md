---
id: init-subclass-implicit-classmethod-kwargs
node: classes.metaprogramming
type: qa
source: python-docs
---
## Q
定义 `__init_subclass__(cls, ...)` 时需不需要手动加 `@classmethod`？子类声明里的额外关键字参数（如 `class Foo(Base, x=1)`）是怎么传到它手上的？

## A
不需要手动加：哪怕写成普通实例方法的形式，`__init_subclass__` 也会被隐式转换成类方法，第一个参数自动是新创建的子类 `cls`。子类声明行里给的额外关键字参数（`class Foo(Base, x=1)` 里的 `x=1`）会被当作调用参数传给基类的 `__init_subclass__`；如果多层基类都定义了这个钩子，习惯做法是自己留下需要的参数、把其余的通过 `super().__init_subclass__(**kwargs)` 继续往上传，保证兼容性。默认的 `object.__init_subclass__` 什么都不做，但只要被传入了任何参数就会报错。
