---
id: override-getattribute-recursion-risk
node: classes.attribute-lookup
type: qa
source: python-docs
---
## Q
重写 `__getattribute__()` 时最容易踩的坑是什么？该怎么避免？

## A
最容易踩的坑是无限递归：在方法体内直接写 `self.name`（比如打日志时读 `self.__class__`）会再次触发 `self.__getattribute__()`，从而死循环。避免方法是：方法体内需要访问任何属性时，一律通过基类实现读取，例如 `object.__getattribute__(self, name)`，而不是直接用点号访问 `self` 上的属性。另外要注意：`__getattribute__()` 拦截的是「一切」属性访问，写不好会让类里其它依赖属性查找的逻辑（包括描述符、`__getattr__` 本身）全部变慢或出错。
