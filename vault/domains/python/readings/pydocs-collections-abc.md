---
nodes:
- classes.abc-protocols
title: collections.abc：容器的抽象基类
corpus: python-docs
section: 49-collections-abc
url: https://docs.python.org/3/library/collections.abc.html
tags:
- canonical
---

# collections.abc：容器的抽象基类

collections.abc 定义了一整套容器相关的抽象基类（Iterable、Iterator、Sequence、Mapping、Hashable 等），是鸭子类型和显式接口约束之间的桥梁。核心机制是虚拟子类（virtual subclass）：一个类不需要真的继承某个 ABC，只要通过 ABC.register(MyClass) 注册，或者恰好实现了该 ABC 要求的全部方法，isinstance(obj, ABC) 就会返回 True，这让第三方类型也能被判定为符合某个协议而不需要修改其继承关系。文档给出了每个 ABC 要求实现哪些抽象方法、哪些方法是自动获得的混入（mixin）方法的详细表格，比如只要实现了 __len__ 和 __getitem__，Sequence 就能自动提供 __contains__、__iter__、index()、count() 等一整套方法。这是判断我的自定义容器类该继承哪个 ABC 才能少写代码的权威依据。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/collections.abc.html)

## Archived copy
![[pydocs-collections-abc-clip]]
%% trellis:end %%
