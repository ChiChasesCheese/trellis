---
id: set-name-when-called
node: classes.properties-descriptors
type: qa
source: python-docs
---
## Q
描述符的 `__set_name__(self, owner, name)` 是谁在什么时候调用的？如果描述符是类创建完之后才动态加上去的，会发生什么？

## A
是 `type` 元类（metaclass）在新建类时调用的：类体执行完、`type.__new__()` 构造类对象的那一刻，元类会扫描类的命名空间，对每个定义了 `__set_name__()` 的描述符调用它一次，传入 `owner`（这个描述符所属的类）和 `name`（它被赋给的类变量名）。因为这个通知只发生在类创建时刻，如果之后才用 `SomeClass.attr = SomeDescriptor()` 动态挂上去，`__set_name__()` 不会自动被调用，需要手动调。
