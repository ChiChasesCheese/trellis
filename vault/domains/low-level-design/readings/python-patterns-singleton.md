---
nodes: [patterns.creational]
url: https://python-patterns.guide/gang-of-four/singleton/
---
# The Singleton Pattern

值得读：Brandon Rhodes 讲清楚"模块本身就是单例"——`import` 只创建一份模块对象，后续导入拿到的都是同一个，这比手写 Singleton
类更 Pythonic，直接对应 `patterns-misuse-singleton`、`patterns-singleton-costs` 两张卡"什么时候该用模块级全局对象而不是硬造
一个 Singleton 类"，读它能补上为什么 GoF 的经典 Singleton 实现在 Python 里大多是多余的。

%% trellis:begin %%
## Source
[Open the original ↗](https://python-patterns.guide/gang-of-four/singleton/)

## Archived copy
![[python-patterns-singleton-clip]]
%% trellis:end %%
