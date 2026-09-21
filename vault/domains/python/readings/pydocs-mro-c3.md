---
nodes:
- classes.inheritance-mro
title: 方法解析顺序（MRO）：C3 算法
corpus: python-docs
section: 08-mro
url: https://docs.python.org/3/howto/mro.html
tags:
- canonical
---

# 方法解析顺序（MRO）：C3 算法

这篇历史文档由 Python 之父 Guido 亲自撰写附录，解释了 Python 2.3 起为什么改用 C3 线性化算法来决定 super() 到底调用哪个父类的方法。核心结论：C3 保证了两条直觉性质，子类永远排在父类之前，且多个父类之间的声明顺序会被保留，不会因为继承关系而颠倒。文中给出了坏的 MRO 的具体例子：如果继承关系本身自相矛盾（比如两个基类的声明顺序和它们各自的继承链冲突），Python 会直接抛出 TypeError 拒绝创建类，而不是给出一个不一致的顺序。读完能准确解释 super() 调的到底是父类还是 MRO 里的下一个（是后者），以及为什么 mixin 类要设计成能被安全插入到 MRO 任意位置。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/howto/mro.html)

## Archived copy
![[pydocs-mro-c3-clip]]
%% trellis:end %%
