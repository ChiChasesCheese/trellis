---
nodes:
- types.basics
- types.gradual-typing
- types.protocols-generics
- types.typeddict-literal
title: typing 模块：类型提示完整参考
corpus: python-docs
section: 51-typing
url: https://docs.python.org/3/library/typing.html
tags:
- canonical
---

# typing 模块：类型提示完整参考

typing 模块是 Python 类型系统的核心，这篇长文档覆盖了从基础到进阶的完整体系：类型别名让复杂类型有个好记的名字；NewType 在运行时其实什么都不做，纯粹是给类型检查器看的标签，能区分底层类型相同但语义不同的两个概念（比如同样是 int 的 UserId 和普通整数不能互相误传）；泛型（TypeVar、3.12 起的 class Box[T] 简化语法）让容器和函数能对元素类型做参数化约束，协变（covariant）/逆变（contravariant）决定了子类型关系在泛型场景下如何传递；Protocol 提供了结构化子类型，不需要显式继承，只要具备相同方法签名就算实现了该协议；ParamSpec 专门解决装饰器场景下包装函数要保留原函数完整参数签名的类型标注难题；Any 则是类型系统里的万能钥匙，和所有类型双向兼容，但用多了等于放弃了类型检查的价值。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/typing.html)

## Archived copy
![[pydocs-typing-module-clip]]
%% trellis:end %%
