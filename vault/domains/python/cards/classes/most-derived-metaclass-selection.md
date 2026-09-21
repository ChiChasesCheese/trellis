---
id: most-derived-metaclass-selection
node: classes.metaprogramming
type: qa
source: python-docs
---
## Q
一个类同时继承了带不同元类（metaclass）的多个基类时，Python 怎么决定最终用哪个元类？选不出来会怎样？

## A
Python 会在『显式指定的元类（如果有）』和『每个基类各自的元类（即 `type(base)`）』这些候选里，挑出一个同时是所有候选元类子类型的那个，称为「最派生的元类（most derived metaclass）」——它必然兼容所有基类的元类要求。如果这些候选元类互相之间没有这种父子关系（谁也不是谁的子类型），挑不出这样一个『最派生』的元类，类定义直接失败，抛出 `TypeError`，这就是常说的「元类冲突（metaclass conflict）」。
