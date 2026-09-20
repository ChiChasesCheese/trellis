---
nodes: [python.context-iterators]
url: https://peps.python.org/pep-0343/
---
# PEP 343 – The "with" Statement

值得读：`with` 语句和 `__enter__`/`__exit__` 协议的原始提案，是 `python-context-with-guarantee` 卡
"`with` 保证成对操作"这条不变量的来源——它把 `try/finally` 的资源释放责任从调用方挪到了上下文管理器自己身上，
读它能补上这条协议到底承诺了什么、异常从 `__exit__` 里怎么被吞掉或重新抛出。

%% trellis:begin %%
## Source
[Open the original ↗](https://peps.python.org/pep-0343/)

## Archived copy
![[pep343-with-statement-clip]]
%% trellis:end %%
