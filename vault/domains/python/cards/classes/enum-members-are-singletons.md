---
id: enum-members-are-singletons
node: classes.enums
type: qa
source: python-docs
---
## Q
`Color.RED` 这样的枚举（enum）成员，每次访问拿到的是不是同一个对象？这是怎么保证的？

## A
是同一个对象：枚举成员是单例（singleton）。负责构造枚举类的元类 `EnumType` 会在创建枚举类本身的同时，把类体里声明的每个成员都实例化出来，并给类装上一个自定义的 `__new__()`，之后任何『再构造一个这个成员』的尝试（比如 `Color(1)` 再查一次）都只会返回已经存在的那个实例，而不会创建新对象。所以 `Color.RED is Color.RED` 恒为 `True`，枚举成员之间的比较也天然可以用 `is`。
