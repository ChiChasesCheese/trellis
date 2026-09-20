---
nodes: [python.context-iterators]
url: https://peps.python.org/pep-0255/
---
# PEP 255 – Simple Generators

值得读：`yield` 与生成器函数最早的提案，是 `python-context-generator-iterator`、`python-context-class-vs-generator`
两张卡的源头——用一个函数体替代手写 `__iter__`/`__next__` 状态机，惰性求值靠解释器暂停/恢复帧来实现，读它能补上生成器和
"手写迭代器类"到底是同一件事的两种写法，还是有本质不同。

%% trellis:begin %%
## Source
[Open the original ↗](https://peps.python.org/pep-0255/)
%% trellis:end %%
