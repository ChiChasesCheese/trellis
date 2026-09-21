---
nodes:
- types.protocols-generics
- classes.abc-protocols
title: PEP 544：Protocol 与结构化子类型
corpus: peps
section: 14-pep-0544
url: https://peps.python.org/pep-0544/
tags:
- canonical
---

# PEP 544：Protocol 与结构化子类型

解答“鸭子类型明明是运行时的事，为什么还需要静态检查”。在这之前 typing 只支持名义子类型（nominal subtyping）——要被识别成 Iterable 就必须显式继承或注册，这和 Python 惯常的动态风格格格不入。Protocol 引入结构化子类型（structural subtyping）：只要类实现了 __len__ 和 __iter__，静态检查器就认它是 Sized 和 Iterable，不需要显式声明。文档系统梳理了此前各路方案的取舍——zope.interface 需要显式声明实现、纯 ABC 需要显式 register、collections.abc 靠 __subclasshook__ 做到部分运行时结构化检查但没有静态支持；Protocol 补上的正是“静态 + 无侵入”这一块。明确声明这是对 PEP 484 名义子类型的补充而非替代，@runtime_checkable 只是为了兼容已有的 ABC 使用习惯，并非本意。
