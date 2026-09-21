---
nodes:
- runtime.compile-bytecode
title: dis 模块：字节码反汇编
corpus: python-docs
section: 61-dis
url: https://docs.python.org/3/library/dis.html
tags:
- canonical
---

# dis 模块：字节码反汇编

dis 模块能把一个函数、模块或代码对象反汇编成人类可读的字节码指令序列，是理解这两种写法到底哪个更快、为什么的终极手段，与其靠直觉猜测，不如直接调用 dis.dis(func) 看编译出来的指令数量和种类。文档给出了完整的字节码指令参考（每条指令的作用、操作数含义），以及命令行用法。这是解释性能差异问题时最有说服力的工具，比如对比用局部变量缓存频繁访问的属性前后字节码指令数量的差异，直接看到属性加载指令是否被消除。日常写业务代码几乎不需要直接用它，但在面试被问你怎么验证某个优化确实有效或者需要向团队解释某个性能建议的依据时，dis 输出比我觉得会更快有说服力得多。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/dis.html)

## Archived copy
![[pydocs-dis-module-clip]]
%% trellis:end %%
