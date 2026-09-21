---
nodes:
- model.copy
title: copy 模块：浅拷贝与深拷贝
corpus: python-docs
section: 41-copy
url: https://docs.python.org/3/library/copy.html
tags:
- canonical
---

# copy 模块：浅拷贝与深拷贝

copy 模块提供了 copy.copy()（浅拷贝，只复制最外层容器，内部元素仍是同一对象的引用）和 copy.deepcopy()（深拷贝，递归复制所有层级）两个函数。文档明确说明 deepcopy() 内部维护了一个已复制对象的记忆表（memo），专门用来正确处理循环引用，如果对象 A 引用了 B、B 又引用回 A，deepcopy 不会陷入无限递归，而是复用已经复制好的对象。文档还讲了如何通过 __copy__() 和 __deepcopy__() 自定义类的拷贝行为，以及 __deepcopy__ 优先级高于 __reduce__。这是判断该用切片、list()、copy.copy() 还是 copy.deepcopy() 的权威依据：前三者都只做一层复制，遇到嵌套的可变对象（如列表的列表）仍会共享内部引用，必须用 deepcopy 才能真正互不影响。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/copy.html)

## Archived copy
![[pydocs-copy-module-clip]]
%% trellis:end %%
