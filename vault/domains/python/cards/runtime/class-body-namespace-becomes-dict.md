---
id: class-body-namespace-becomes-dict
node: runtime.namespaces-execution
type: qa
source: python-docs
---
## Q
类定义体（class body）执行时是什么样的代码块？它执行时建立的名字最终变成了什么？

## A
类定义本身是一条可执行语句，在类创建时被执行一次——它是一个独立的代码块（code block），拥有自己的命名空间。这个命名空间执行完之后直接变成这个类的属性字典（`__dict__`）。但类体命名空间的作用域仅限于类体自身，不会延伸到方法体内部：方法要访问类体里定义的名字，必须通过 `self.xxx` 或 `ClassName.xxx`，不能像闭包那样直接引用。
