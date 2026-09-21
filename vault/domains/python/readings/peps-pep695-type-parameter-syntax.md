---
nodes:
- types.protocols-generics
title: PEP 695：3.12 类型参数新语法
corpus: peps
section: 17-pep-0695
url: https://peps.python.org/pep-0695/
tags:
- canonical
---

# PEP 695：3.12 类型参数新语法

把此前必须 T = TypeVar("T") 全局声明、再作为 Generic[T] 基类使用的老写法，收口成 class Box[T]:、def func[T](...)、type ListOrSet[T] = ... 这种就地声明。Motivation 部分点出老写法的三个真实困惑点：TypeVar 明明定义在模块全局作用域，语义却只在某个具体的泛型上下文里成立，同一个变量在不同上下文含义还可能不同；协变/逆变（variance）这种类型论概念，用户定义第一个泛型类就得面对；多个类型参数时的排序规则会被 Generic[V, K] 悄悄改变顺序，容易踩坑。新语法把作用域收紧到声明处、去掉了大部分场景下对 variance 的显式声明负担、排序也变得显式。这是回答“为什么 3.12 之后不用再手写 TypeVar”的直接依据。

%% trellis:begin %%
## Source
[Open the original ↗](https://peps.python.org/pep-0695/)

## Archived copy
![[peps-pep695-type-parameter-syntax-clip]]
%% trellis:end %%
