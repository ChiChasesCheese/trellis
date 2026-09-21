---
id: comprehension-in-class-body-skips-class-scope
node: iteration.comprehensions
type: qa
source: python-docs
---
## Q
在类定义体里直接写 `b = list(a + i for i in range(10))`（`a` 是同一个类体里定义的类属性）为什么会报 `NameError`？

## A
推导式和生成器表达式的独立作用域，其父作用域是定义它的函数/模块作用域，会跳过类定义体的命名空间——类体里的名字只在类体本身的代码里直接可见，不会被内部的推导式继承。所以推导式里的 `a` 会被当作自由变量去外层函数/模块作用域查找，找不到就抛 `NameError`，不会取到类属性 `a`。
