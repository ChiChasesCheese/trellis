---
nodes:
- runtime.frames-eval
- memory.interning-immortal
- memory.object-size
- runtime.import-system
title: sys 模块：解释器内部状态入口
corpus: python-docs
section: 42-sys
url: https://docs.python.org/3/library/sys.html
tags:
- canonical
---

# sys 模块：解释器内部状态入口

sys 模块是查看和调整解释器内部状态的官方入口，几个高频用到的点：sys.getrecursionlimit()/setrecursionlimit() 控制 Python 调用栈的最大深度，超过会抛 RecursionError（本质是为了防止无限递归撑爆底层 C 栈）；sys.intern() 可以手动把字符串加入驻留池，强制让相同内容的字符串复用同一个对象，从而让 == 判断退化成更快的 is 判断，适合大量重复短字符串（如字典的固定键名）的场景；sys.getsizeof() 返回一个对象自身占用的字节数（不含它引用的其他对象），是排查内存占用问题的基本工具；sys.modules 是所有已加载模块的缓存字典，直接操作它可以强制重新加载模块（不推荐但有时用于调试）。这几个函数分散在不同主题下，但都是深入理解 Python 运行时绕不开的基础工具箱。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/sys.html)

## Archived copy
![[pydocs-sys-module-clip]]
%% trellis:end %%
