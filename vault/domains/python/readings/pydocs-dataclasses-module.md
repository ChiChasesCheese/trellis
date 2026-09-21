---
nodes:
- classes.dataclasses
title: dataclasses 模块：数据类完整参考
corpus: python-docs
section: 47-dataclasses
url: https://docs.python.org/3/library/dataclasses.html
tags:
- canonical
---

# dataclasses 模块：数据类完整参考

dataclasses 是 Python 官方给只用来装数据的类提供的样板代码生成器，@dataclass 装饰器会自动生成 __init__、__repr__、__eq__（默认基于所有字段逐一比较）。文档的重点在几个容易用错的地方：字段默认值如果是可变对象（如列表）不能直接写等号加方括号，必须用 field(default_factory=list)，否则所有实例会共享同一个列表，这是可变默认参数陷阱在 dataclass 里的变体；frozen=True 让实例变成不可变（赋值会抛异常）同时自动获得基于字段值的 __hash__，适合用作字典键；__post_init__ 是在自动生成的 __init__ 跑完之后执行的钩子，常用来做字段合法性校验或计算派生字段。文档还讲了继承时字段顺序如何合并、以及关键字专属字段可以打乱默认值必须靠后排列的传统限制。
